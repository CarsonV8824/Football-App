import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import os

from model import FantasyModel
from dataset import get_tensor_data
 
def train():
    if not torch.xpu.is_available() or torch.xpu.device_count() < 1:
        raise Exception("run the command: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/xpu")
    
    device = torch.device("xpu")
    X, y = get_tensor_data()
    X = X.to(device)
    y = y.to(device)

    # Create DataLoader for mini-batch training
    dataset = TensorDataset(X, y)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    model = FantasyModel(input_size=X.shape[1]).to(device)
    loss_fn = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    for epoch in range(1000):
        for X_batch, y_batch in dataloader:
            predictions = model(X_batch)
            loss = loss_fn(predictions, y_batch)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if epoch % 100 == 0:
            # Calculate loss on full dataset for monitoring
            with torch.no_grad():
                full_predictions = model(X)
                full_loss = loss_fn(full_predictions, y)
            print(f"epoch {epoch}, loss = {full_loss.item()}")
        print(epoch)

    model_path = os.path.join(os.path.dirname(__file__), "fantasy_model.pth")
    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")

def load_and_test():
    device = torch.device("xpu")
    
    # Get test data first to determine input size
    X, y = get_tensor_data()
    X = X.to(device)
    y = y.to(device)
    
    # Path to model file
    model_path = os.path.join(os.path.dirname(__file__), "fantasy_model.pth")
    
    # Load model with correct input size
    model = FantasyModel(input_size=X.shape[1])
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()  # Set to evaluation mode
    
    # Make predictions
    with torch.no_grad():
        predictions = model(X)
        print(predictions)
        loss = torch.nn.MSELoss()(predictions, y)
        print(f"Test loss: {loss.item()}")
    
    return model, predictions

if __name__ == "__main__":
    train()
    load_and_test()
