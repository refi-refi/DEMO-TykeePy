import torch


class LogisticRegression(torch.nn.Module):
    def __init__(self, input_size, num_classes):
        super(LogisticRegression, self).__init__()
        self.linear = torch.nn.Linear(input_size, num_classes)

    def forward(self, x):
        return torch.sigmoid(self.linear(x))
