import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import os

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from model import FantasyMLP
from paths import MODEL_PATH
from dataset import get_tensor_data
from device import get_best_device

# Training hyperparameters
BATCH_SIZE = 64
LEARNING_RATE = 0.001
LEARNING_DECAY = 1e-5
NUM_EPOCHS = 121
CHECKPOINT_INTERVAL = 15
VALIDATION_SPLIT = 0.2
 
def train():
    device = get_best_device()
    X, y = get_tensor_data(True)
    X = X.to(device)
    y = y.to(device)

    # Create DataLoader for mini-batch training
    dataset = TensorDataset(X, y)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    model = FantasyMLP(input_size=X.shape[1]).to(device)
    loss_fn = nn.L1Loss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=LEARNING_DECAY)


    scores = dict()
    scores["epchos"] = []
    scores["loss"] = []

    for epoch in range(NUM_EPOCHS):
        for X_batch, y_batch in dataloader:
            predictions = model(X_batch)
            loss = loss_fn(predictions, y_batch)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if epoch % CHECKPOINT_INTERVAL == 0:
            # Calculate loss on full dataset for monitoring
            with torch.no_grad():
                full_predictions = model(X)
                full_loss = loss_fn(full_predictions, y)
            print(f"epoch {epoch}, loss = {full_loss.item()}")
            scores["epchos"].append(epoch)
            scores["loss"].append(full_loss.item())
        print(epoch)

    torch.save(model.state_dict(), MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    temp = pd.DataFrame(scores)
    sns.regplot(data=temp, x="epchos", y="loss")
    plt.title("The effect of the amount of epchos on data loss in the model")
    plt.xticks(range(int(temp["epchos"].min()), int(temp["epchos"].max()) + 1, CHECKPOINT_INTERVAL))
    plt.show()
    
def load_and_test():
    device = get_best_device()
    
    # Get test data first to determine input size
    X, y = get_tensor_data()
    X = X.to(device)
    y = y.to(device)
    
    # Path to model file
    # Load model with correct input size
    model = FantasyMLP(input_size=X.shape[1])
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
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
    train()
    load_and_test()
