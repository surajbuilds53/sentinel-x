"""LSTM World Model for defensive network attack risk and state forecasting.

SIH26153 B.Tech Minor Project.
Combines a 2-layer recurrent sequence backbone with three specialized forecasting heads
and autoregressive multi-step prediction (T+1, T+2, T+3).
"""

from typing import Dict, Tuple, Optional
import torch
import torch.nn as nn
import torch.nn.functional as F

from sentinel_x.models.forecasting_heads import RiskHead, StageHead, NetworkStateHead


class LSTMWorldModel(nn.Module):
    """Deep Recurrent World Model with Multi-Head Autoregressive Forecasting."""

    def __init__(
        self,
        input_dim: int = 16,
        hidden_size: int = 128,
        num_layers: int = 2,
        dropout: float = 0.3,
        num_stages: int = 5,
    ):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_stages = num_stages

        # 2-layer recurrent backbone
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        
        # Latent representation projection & dropout
        self.dropout = nn.Dropout(dropout)

        # Three dedicated forecasting heads
        self.risk_head = RiskHead(hidden_size=hidden_size)
        self.stage_head = StageHead(hidden_size=hidden_size, num_classes=num_stages)
        self.state_head = NetworkStateHead(hidden_size=hidden_size, state_dim=input_dim)

    def forward_step(
        self,
        x: torch.Tensor,
        hidden: Optional[Tuple[torch.Tensor, torch.Tensor]] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """Perform a single recurrent forward step.
        
        Args:
            x: Input tensor of shape (batch, seq_len, input_dim) or (batch, 1, input_dim).
            hidden: Optional (h_n, c_n) recurrent state tuple.
            
        Returns:
            (pred_risk, stage_logits, pred_state, (h_n, c_n))
        """
        lstm_out, hidden = self.lstm(x, hidden)
        latent = lstm_out[:, -1, :]  # Take final time step latent representation
        latent = self.dropout(latent)

        pred_risk = self.risk_head(latent)             # (batch, 1) in [0, 1]
        stage_logits = self.stage_head(latent)         # (batch, num_stages)
        pred_state = self.state_head(latent)           # (batch, input_dim)

        return pred_risk, stage_logits, pred_state, hidden

    def forward(
        self,
        historical_sequence: torch.Tensor,
        horizon: int = 3,
    ) -> Dict[str, torch.Tensor]:
        """Autoregressive multi-step rollout for horizon H (T+1, T+2, T+3).
        
        Given history [T-N...T]:
        At step 1: inputs history -> predicts T+1 (risk_1, stage_1, state_1).
        At step 2: inputs state_1 -> predicts T+2 (risk_2, stage_2, state_2).
        At step 3: inputs state_2 -> predicts T+3 (risk_3, stage_3, state_3).
        
        Args:
            historical_sequence: (batch, seq_len, input_dim).
            horizon: Number of future forecast time steps.
            
        Returns:
            Dict containing:
            - 'risk_preds': (batch, horizon)
            - 'stage_logits': (batch, horizon, num_stages)
            - 'state_preds': (batch, horizon, input_dim)
        """
        batch_size = historical_sequence.size(0)
        device = historical_sequence.device

        risk_list = []
        stage_logits_list = []
        state_list = []

        # Step 1: Process full historical sequence T-N ... T
        pred_risk, stage_logits, pred_state, hidden = self.forward_step(
            historical_sequence, hidden=None
        )
        risk_list.append(pred_risk)
        stage_logits_list.append(stage_logits.unsqueeze(1))
        state_list.append(pred_state.unsqueeze(1))

        current_state = pred_state.unsqueeze(1)  # (batch, 1, input_dim)

        # Autoregressive rollout for subsequent steps (T+2, T+3, ...)
        for _ in range(1, horizon):
            pred_risk, stage_logits, pred_state, hidden = self.forward_step(
                current_state, hidden=hidden
            )
            risk_list.append(pred_risk)
            stage_logits_list.append(stage_logits.unsqueeze(1))
            state_list.append(pred_state.unsqueeze(1))
            current_state = pred_state.unsqueeze(1)

        # Concatenate multi-step predictions
        risk_preds = torch.cat(risk_list, dim=1)                 # (batch, horizon)
        stage_logits_all = torch.cat(stage_logits_list, dim=1)   # (batch, horizon, num_stages)
        state_preds_all = torch.cat(state_list, dim=1)           # (batch, horizon, input_dim)

        return {
            "risk_preds": risk_preds,
            "stage_logits": stage_logits_all,
            "state_preds": state_preds_all,
        }

    @torch.no_grad()
    def forecast_inference(
        self,
        historical_sequence: torch.Tensor,
        horizon: int = 3,
    ) -> Dict[str, torch.Tensor]:
        """Inference mode method producing probabilities and discrete class predictions."""
        self.eval()
        outputs = self.forward(historical_sequence, horizon=horizon)
        stage_probs = F.softmax(outputs["stage_logits"], dim=-1)
        predicted_stages = torch.argmax(stage_probs, dim=-1)

        return {
            "risk_probabilities": outputs["risk_preds"],
            "stage_probabilities": stage_probs,
            "predicted_stages": predicted_stages,
            "predicted_states": outputs["state_preds"],
        }
