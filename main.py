import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import os

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from src.model import FantasyMLP
from src.scrape import insert_data
from src.dataset import get_predicted_data_name
from src.device import get_best_device

def predict():
    name = input("Name of player")
    year = int(input("What year did your season start in?"))
    week = int(input("What week are you in to predict next week?"))
    insert_data(year, week)
    
    device = get_best_device()
    X, y = get_predicted_data_name(name)
    X = X.to(device)
    y = y.to(device)
    
    # Path to model file
    model_path = os.path.join(os.path.dirname(__file__), "fantasy_model.pth")
    
    # Load model with correct input size
    model = FantasyMLP(input_size=X.shape[1])
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()  # Set to evaluation mode
    
    # Make predictions
    with torch.no_grad():
        predictions = model(X)
        print(predictions)
        loss = torch.nn.L1Loss()(predictions, y)
        print(f"Test loss: {loss.item()}")
    
    return model, predictions

if __name__ == "__main__":
    predict()
