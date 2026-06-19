from __future__ import annotations

try:
    import torch
    import torch.nn as nn
except ModuleNotFoundError:  # pragma: no cover - runtime image omits torch on purpose.
    torch = None
    nn = None

NUM_CLASSES = 3
CLASS_NAMES = ("visitor", "employee", "admin")


if nn is not None:

    class BadgeClassifier(nn.Module):
        """Small CNN for synthetic badge classification.

        Expects float tensors in NCHW with shape (B, 3, H, W).
        """

        def __init__(self, num_classes: int = NUM_CLASSES) -> None:
            super().__init__()

            self.features = nn.Sequential(
                nn.Conv2d(3, 16, kernel_size=3, padding=1),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(2),
                nn.Conv2d(16, 32, kernel_size=3, padding=1),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(2),
                nn.Conv2d(32, 64, kernel_size=3, padding=1),
                nn.ReLU(inplace=True),
                nn.AdaptiveAvgPool2d((1, 1)),
            )
            self.classifier = nn.Linear(64, num_classes)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            x = self.features(x)
            x = torch.flatten(x, 1)
            return self.classifier(x)
else:

    class BadgeClassifier:
        def __init__(self, *_args, **_kwargs) -> None:
            raise RuntimeError("PyTorch is required to instantiate BadgeClassifier")
