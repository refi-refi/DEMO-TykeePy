from os import path, makedirs
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from tykee import logger
from tykee.config import ML_MODELS_DIR
from tykee.data.models.history_data import HistoryData
from tykee.data.utils.features import datetime_sin, datetime_cos
from tykee.data.utils.scalers import normalizer
from tykee.machine_learning.classification import micro_macro_label
from tykee.machine_learning.models.log_regression import LogisticRegression
from tykee.machine_learning.models.supervised_data import SupervisedHistoryData
from tykee.machine_learning.models.torch_dataset import SupervisedDataset


class TrainTestModel:
    def __init__(
        self,
        learning_rate: float = 0.001,
        batch_size: int = 32,
        num_epochs: int = 10,
        window_size: int = 50,
        input_dim: int = 450,
        output_dim: int = 2,
    ):
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.num_epochs = num_epochs
        self.window_size = window_size
        self.input_dim = input_dim
        self.output_dim = output_dim

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.train_loader = None
        self.test_loader = None
        self.model = LogisticRegression(input_dim, output_dim).to(self.device)
        self.loss_fn = torch.nn.CrossEntropyLoss()
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=self.learning_rate)

    def train_test(self):
        """
        Train and test the model
        Returns
        -------
        None
        """
        for _ in tqdm(range(self.num_epochs)):
            self.train_loop()
            self.test_loop()
        logger.info("Finished Training")

    def train_loop(self):
        """
        Train the model on train data
        Returns
        -------
        None
        """
        for batch, (inputs, labels) in enumerate(self.train_loader):
            inputs = inputs.view(-1, self.input_dim).requires_grad_().to(self.device)
            labels = labels.to(self.device)

            # Prediction and loss
            prediction = self.model(inputs)
            loss = self.loss_fn(prediction, labels)

            # Backpropagation
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            if batch % 100 == 0:
                logger.info(f"Batch: {batch}, Loss: {loss.item()}")

    def test_loop(self):
        """
        Test the model on test data
        Returns
        -------
        None
        """
        test_loss, correct = 0, 0

        with torch.no_grad():
            for inputs, labels in self.test_loader:
                inputs = (
                    inputs.view(-1, self.input_dim).requires_grad_().to(self.device)
                )
                labels = labels.to(self.device)

                prediction = self.model(inputs)
                test_loss += self.loss_fn(prediction, labels).item()
                correct += (
                    (prediction.argmax(1) == labels).type(torch.float).sum().item()
                )

        test_loss /= self.num_epochs
        correct /= int(len(self.test_loader.dataset) - self.window_size)
        logger.info(
            f"Test Error: Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n"
        )

    def save_model(self, name: str):
        """
        Save the model weights.

        Parameters
        ----------
        name: str
            Name of the model.
        Returns
        -------
        None
        """
        model_path = path.join(ML_MODELS_DIR, name)
        torch.save(self.model.state_dict(), model_path)
        logger.info(f"Model saved at {model_path}")

    def load_data(self, symbol, period, date_from, date_to):
        """
        Load data from database and sets train and test DataLoaders
        Parameters
        ----------
        symbol
        period
        date_from
        date_to

        Returns
        -------
        None
        """
        hist_data = HistoryData(symbol, period, date_from, date_to)
        features = [
            dict(func=datetime_sin, kwargs=dict(data_col="end_ts_utc", period="day")),
            dict(func=datetime_cos, kwargs=dict(data_col="end_ts_utc", period="day")),
            dict(func=datetime_sin, kwargs=dict(data_col="end_ts_utc", period="week")),
            dict(func=datetime_cos, kwargs=dict(data_col="end_ts_utc", period="week")),
        ]
        scaler = dict(func=normalizer, kwargs=dict(min_max=(-1, 1)))
        label = dict(
            func=micro_macro_label,
            kwargs=dict(macro_period="H4", threshold_percentile=0.95),
        )

        data = SupervisedHistoryData(hist_data, features, label, scaler)
        train_dataset = SupervisedDataset(data.train_data, scaler, self.window_size)
        test_dataset = SupervisedDataset(data.test_data, scaler, self.window_size)

        self.train_loader = DataLoader(
            train_dataset, batch_size=self.batch_size, shuffle=False
        )
        self.test_loader = DataLoader(
            test_dataset, batch_size=self.batch_size, shuffle=False
        )
        logger.info(f"Data loaded: {symbol} {period} {date_from} {date_to}")


if __name__ == "__main__":
    train_test_model = TrainTestModel(num_epochs=2)
    train_test_model.load_data("EURUSD", "M5", "2022-01-01", "2022-06-30")
    train_test_model.train_test()
    train_test_model.save_model("model_weights.pth")
