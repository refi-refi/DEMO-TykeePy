from typing import Dict

import pandas as pd
import torch
from torch.utils.data import Dataset

DROP_X_COLS = ["ts", "dt", "open", "label"]


class SupervisedDataset(Dataset):
    def __init__(self, data: pd.DataFrame, scaler: Dict = None, window_size: int = 50):
        self.data = data
        self.window_size = window_size
        self.scaler_func = scaler.get("func") if scaler else None
        self.scaler_kwargs = scaler.get("kwargs") if scaler else None

        self.x_cols = [
            col
            for col in self.data.columns
            if not any(d_col in col for d_col in DROP_X_COLS)
        ]

    def __len__(self):
        return len(self.data) - self.window_size

    def __getitem__(self, idx):
        """
        Returns a tuple of (x, y) where x is a tensor of shape (window_size, num_features)
        Parameters
        ----------
        idx

        Returns
        -------
        x, y: torch.Tensor, torch.Tensor
        """
        if torch.is_tensor(idx):
            idx = idx.tolist()

        x = self.data[self.x_cols].iloc[idx : idx + self.window_size]
        y = self.data.loc[idx + self.window_size, "label"]

        if self.scaler_func:
            x = self.scaler_func(x, **self.scaler_kwargs)

        return torch.tensor(x.values, dtype=torch.float), torch.tensor(y, dtype=torch.long)
