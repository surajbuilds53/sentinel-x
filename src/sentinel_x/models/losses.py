"""Multi-task loss module for Sentinel-X LSTM World Model."""

from typing import Dict, Tuple
import torch
import torch.nn as nn


class MultiTaskForecastingLoss(nn.Module):
    """Weighted multi-task loss combining Risk, Stage, and State forecasting objectives.
    
    Total Loss = w_risk * BCE + w_stage * CE + w_state * MSE
    """

    def __init__(
        self,
        risk_weight: float = 1.0,
        stage_weight: float = 1.0,
        state_weight: float = 0.5,
    ):
        super().__init__()
        self.risk_weight = risk_weight
        self.stage_weight = stage_weight
        self.state_weight = state_weight
        
        self.bce = nn.BCELoss()
        self.ce = nn.CrossEntropyLoss()
        self.mse = nn.MSELoss()

    def forward(
        self,
        pred_risk: torch.Tensor,
        pred_stage_logits: torch.Tensor,
        pred_state: torch.Tensor,
        target_risk: torch.Tensor,
        target_stage: torch.Tensor,
        target_state: torch.Tensor,
    ) -> Tuple[torch.Tensor, Dict[str, float]]:
        """Compute multi-task loss over the forecast step.
        
        Args:
            pred_risk: (batch, 1) or (batch,) in [0, 1].
            pred_stage_logits: (batch, num_classes).
            pred_state: (batch, state_dim).
            target_risk: (batch, 1) or (batch,).
            target_stage: (batch,) integer stage labels.
            target_state: (batch, state_dim).
            
        Returns:
            (total_loss, loss_breakdown_dict)
        """
        # Ensure proper shape for BCE
        p_risk = pred_risk.view(-1)
        t_risk = target_risk.view(-1).float()
        loss_risk = self.bce(p_risk, t_risk)
        
        # Cross-Entropy for stage
        t_stage = target_stage.view(-1).long()
        loss_stage = self.ce(pred_stage_logits, t_stage)
        
        # MSE for network state vector
        loss_state = self.mse(pred_state, target_state)
        
        total_loss = (
            self.risk_weight * loss_risk
            + self.stage_weight * loss_stage
            + self.state_weight * loss_state
        )
        
        breakdown = {
            "total_loss": float(total_loss.item()),
            "risk_loss": float(loss_risk.item()),
            "stage_loss": float(loss_stage.item()),
            "state_loss": float(loss_state.item()),
        }
        
        return total_loss, breakdown
