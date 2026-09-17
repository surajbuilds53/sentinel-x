"""Training engine for the Sentinel-X LSTM World Model."""

from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
import logging
import copy
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

from sentinel_x.models.lstm_world_model import LSTMWorldModel
from sentinel_x.models.losses import MultiTaskForecastingLoss
from sentinel_x.config import get_device

logger = logging.getLogger(__name__)


class WorldModelTrainer:
    """Orchestrates multi-task training, validation, early stopping, and checkpointing."""

    def __init__(
        self,
        model: LSTMWorldModel,
        loss_fn: MultiTaskForecastingLoss,
        learning_rate: float = 0.001,
        weight_decay: float = 1e-4,
        device: str = "auto",
    ):
        self.device = torch.device(get_device(device))
        self.model = model.to(self.device)
        self.loss_fn = loss_fn.to(self.device)
        self.optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr=float(learning_rate),
            weight_decay=float(weight_decay),
        )
        self.history: List[Dict[str, float]] = []

    def _compute_multi_step_loss(
        self,
        outputs: Dict[str, torch.Tensor],
        targets_risk: torch.Tensor,
        targets_stage: torch.Tensor,
        targets_state: torch.Tensor,
        horizon: int,
    ) -> Tuple[torch.Tensor, Dict[str, float]]:
        total_loss = torch.tensor(0.0, device=self.device)
        agg_breakdown = {"total_loss": 0.0, "risk_loss": 0.0, "stage_loss": 0.0, "state_loss": 0.0}

        for h in range(horizon):
            pred_risk_h = outputs["risk_preds"][:, h]
            pred_stage_h = outputs["stage_logits"][:, h, :]
            pred_state_h = outputs["state_preds"][:, h, :]

            tgt_risk_h = targets_risk[:, h]
            tgt_stage_h = targets_stage[:, h]
            tgt_state_h = targets_state[:, h, :]

            loss_h, breakdown_h = self.loss_fn(
                pred_risk_h,
                pred_stage_h,
                pred_state_h,
                tgt_risk_h,
                tgt_stage_h,
                tgt_state_h,
            )
            total_loss = total_loss + loss_h
            for k in agg_breakdown:
                agg_breakdown[k] += breakdown_h[k] / horizon

        total_loss = total_loss / horizon
        return total_loss, agg_breakdown

    def fit(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader,
        epochs: int = 25,
        horizon: int = 3,
        patience: int = 5,
        checkpoint_path: Optional[Path | str] = None,
    ) -> Dict[str, Any]:
        """Train model with validation and early stopping."""
        best_val_loss = float("inf")
        best_model_state = None
        epochs_no_improve = 0
        best_epoch = 0

        logger.info(f"Starting training on device: {self.device} for {epochs} epochs...")

        for epoch in range(1, epochs + 1):
            # --- Training Loop ---
            self.model.train()
            train_losses = []
            for batch_x, batch_y_risk, batch_y_stage, batch_y_state in train_loader:
                batch_x = batch_x.to(self.device)
                batch_y_risk = batch_y_risk.to(self.device)
                batch_y_stage = batch_y_stage.to(self.device)
                batch_y_state = batch_y_state.to(self.device)

                self.optimizer.zero_grad()
                outputs = self.model(batch_x, horizon=horizon)
                loss, _ = self._compute_multi_step_loss(
                    outputs, batch_y_risk, batch_y_stage, batch_y_state, horizon
                )
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                self.optimizer.step()
                train_losses.append(loss.item())

            avg_train_loss = float(np.mean(train_losses))

            # --- Validation Loop ---
            self.model.eval()
            val_losses = []
            val_breakdowns = []
            with torch.no_grad():
                for val_x, val_y_risk, val_y_stage, val_y_state in val_loader:
                    val_x = val_x.to(self.device)
                    val_y_risk = val_y_risk.to(self.device)
                    val_y_stage = val_y_stage.to(self.device)
                    val_y_state = val_y_state.to(self.device)

                    outputs = self.model(val_x, horizon=horizon)
                    val_loss, b_down = self._compute_multi_step_loss(
                        outputs, val_y_risk, val_y_stage, val_y_state, horizon
                    )
                    val_losses.append(val_loss.item())
                    val_breakdowns.append(b_down)

            avg_val_loss = float(np.mean(val_losses))

            epoch_record = {
                "epoch": epoch,
                "train_loss": avg_train_loss,
                "val_loss": avg_val_loss,
            }
            self.history.append(epoch_record)

            if epoch % 5 == 0 or epoch == 1 or epoch == epochs:
                logger.info(
                    f"Epoch {epoch:02d}/{epochs:02d} | "
                    f"Train Loss: {avg_train_loss:.4f} | "
                    f"Val Loss: {avg_val_loss:.4f}"
                )

            # Checkpoint on improvement
            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                best_epoch = epoch
                epochs_no_improve = 0
                best_model_state = copy.deepcopy(self.model.state_dict())
                if checkpoint_path:
                    p = Path(checkpoint_path)
                    p.parent.mkdir(parents=True, exist_ok=True)
                    torch.save(
                        {
                            "epoch": epoch,
                            "model_state_dict": self.model.state_dict(),
                            "optimizer_state_dict": self.optimizer.state_dict(),
                            "val_loss": best_val_loss,
                        },
                        p,
                    )
            else:
                epochs_no_improve += 1
                if epochs_no_improve >= patience:
                    logger.info(f"Early stopping triggered at epoch {epoch} (best epoch {best_epoch}).")
                    break

        # Restore best model weights
        if best_model_state is not None:
            self.model.load_state_dict(best_model_state)
            logger.info(f"Restored best weights from epoch {best_epoch} with val_loss={best_val_loss:.4f}")

        return {
            "best_epoch": best_epoch,
            "best_val_loss": best_val_loss,
            "history": self.history,
        }
