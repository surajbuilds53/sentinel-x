"""Three dedicated forecasting heads for the Sentinel-X World Model.

1. Risk Head: Predicts attack probability in [0, 1] (Sigmoid).
2. Stage Head: Predicts 5-class MITRE ATT&CK stage logits.
3. State Head: Predicts the next continuous network-state vector.
"""

import torch
import torch.nn as nn


class RiskHead(nn.Module):
    """Predicts future network attack risk probability."""

    def __init__(self, hidden_size: int = 128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),
        )

    def forward(self, latent: torch.Tensor) -> torch.Tensor:
        """Args:
            latent: Latent representation from backbone (batch, hidden_size).
        Returns:
            Probability of attack risk (batch, 1).
        """
        return self.net(latent)


class StageHead(nn.Module):
    """Predicts future behavioral attack stage class logits."""

    def __init__(self, hidden_size: int = 128, num_classes: int = 5):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes),
        )

    def forward(self, latent: torch.Tensor) -> torch.Tensor:
        """Args:
            latent: Latent representation from backbone (batch, hidden_size).
        Returns:
            Raw class logits (batch, num_classes).
        """
        return self.net(latent)


class NetworkStateHead(nn.Module):
    """Reconstructs and predicts future continuous network-state vector."""

    def __init__(self, hidden_size: int = 128, state_dim: int = 16):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, state_dim),
        )

    def forward(self, latent: torch.Tensor) -> torch.Tensor:
        """Args:
            latent: Latent representation from backbone (batch, hidden_size).
        Returns:
            Predicted network state vector (batch, state_dim).
        """
        return self.net(latent)
