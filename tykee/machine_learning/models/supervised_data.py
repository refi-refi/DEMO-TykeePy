from typing import Dict, List

import pandas as pd

from tykee.data.models.history_data import HistoryData


class SupervisedHistoryData:
    def __init__(
        self,
        history_data: HistoryData,
        features: List,
        label: Dict,
        scaler: Dict,
        train_split: float = 0.8,
    ):
        self.history_data = history_data
        self.features = features
        self.scaler = scaler
        self.label = label

        self.__data__ = self.__build__()
        self.train_data = self.__data__[
            : int(len(self.__data__) * train_split)
        ].reset_index(drop=True)
        self.test_data = self.__data__[
            int(len(self.__data__) * train_split) :
        ].reset_index(drop=True)

    def __build__(self) -> pd.DataFrame:
        data = self.history_data.data_frame.copy()

        for feature in self.features:
            feature_func = feature.get("func")
            col_name = feature.get("kwargs").pop("data_col")
            feature_kwargs = feature.get("kwargs")
            data = pd.concat(
                [data, feature_func(data[col_name], **feature_kwargs)], axis=1
            )

        label_func = self.label.get("func")
        label_kwargs = self.label.get("kwargs")
        data["label"] = label_func(self.history_data, **label_kwargs)
        if data.isnull().values.any():
            data = data.dropna()
        data.label = data.label.astype(int)

        return data

    def __repr__(self):
        return f"""
        SupervisedHistoryData(
            history_data(
                symbol={self.history_data.symbol},
                period={self.history_data.period},
                start_dt={self.history_data.start_dt},
                end_dt={self.history_data.end_dt},
            ),
            features={self.features},
            label_func={self.label},
            scaler={self.scaler},
        )
        """
