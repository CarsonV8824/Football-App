from database import Database
import torch


def get_tensor_data():
    X = []
    y = []

    for inputs, output in Database.get_data():
        X.append(inputs)
        y.append([output])

    X = torch.tensor(X, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.float32)
    return X, y


