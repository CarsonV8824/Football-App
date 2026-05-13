import torch
import torch.nn as nn
import torch.optim as optim
import os

from model import FantasyModel
from dataset import get_tensor_data
 
def main():
    if not torch.xpu.is_available() or torch.xpu.device_count() < 1:
        raise Exception("run the command: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/xpu")
    
    device = torch.device("xpu")
    X, y = get_tensor_data()
    X = X.to(device)
    y = y.to(device)

    model = FantasyModel(input_size=X.shape[1]).to(device)
    loss_fn = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(100000):
        predictions = model(X)
        loss = loss_fn(predictions, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 100 == 0:
            print(f"epoch {epoch}, loss = {loss.item()}")

    model_path = os.path.join(os.path.dirname(__file__), "fantasy_model.pth")
    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    main()