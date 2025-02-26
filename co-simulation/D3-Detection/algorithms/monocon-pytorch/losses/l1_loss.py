import os
import sys
import torch
import torch.nn as nn

from typing import Optional

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from losses.utils import weighted_loss

# TODO changed
@weighted_loss
def l1_loss(pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    if target.numel() == 0:
        print("Target tensor is empty")
        # Handle the case when the target tensor is empty
        return torch.tensor(0.0, device=pred.device, dtype=pred.dtype)
    else:
        assert pred.size() == target.size(), "Prediction and target must have the same size."
        loss = torch.abs(pred - target)
        return loss


class L1Loss(nn.Module):
    def __init__(self, 
                 reduction: str = 'mean', 
                 loss_weight: float = 1.0):
        
        super().__init__()
        
        self.reduction = reduction
        self.loss_weight = loss_weight

    def forward(self,
                pred: torch.Tensor,
                target: torch.Tensor,
                weight: Optional[torch.Tensor] = None,
                avg_factor: Optional[int] = None,
                reduction_override: Optional[str] = None) -> torch.Tensor:
        
        assert reduction_override in (None, 'none', 'mean', 'sum')
        reduction = (reduction_override if reduction_override else self.reduction)
        return self.loss_weight * l1_loss(pred, target, weight, reduction=reduction, avg_factor=avg_factor)
