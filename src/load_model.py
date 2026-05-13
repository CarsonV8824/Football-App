import torch
import os
from model import FantasyModel
from dataset import get_tensor_data

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
        loss = torch.nn.MSELoss()(predictions, y)
        print(f"Test loss: {loss.item()}")
    
    return model, predictions

if __name__ == "__main__":
    model, predictions = load_and_test()
