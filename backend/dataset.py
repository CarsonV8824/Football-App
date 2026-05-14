from database import Database
import torch
from sklearn.preprocessing import StandardScaler
import pickle
import os


def get_scaler_path():
    """Get path to saved scaler file"""
    return os.path.join(os.path.dirname(__file__), "scaler_X.pkl")


def get_tensor_data(fit_scaler=None):
    """
    Load and normalize data.
    
    Args:
        fit_scaler (bool or None): If None, auto-detect based on scaler file existence.
                                  If True, force fit new scaler. If False, force load existing.
    """
    X = []
    y = []

    for inputs, output in Database.get_data():
        print(inputs, output)
        X.append(inputs)
        y.append([output])

    scaler_path = get_scaler_path()
    
    # Auto-detect if fit_scaler not specified
    if fit_scaler is None:
        fit_scaler = not os.path.exists(scaler_path)
    
    if fit_scaler:
        # Training: fit new scaler and save it
        scaler_X = StandardScaler()
        X = scaler_X.fit_transform(X)
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler_X, f)
        print(f"Scaler fitted and saved to {scaler_path}")
    else:
        # Prediction: load existing scaler and use it
        with open(scaler_path, 'rb') as f:
            scaler_X = pickle.load(f)
        X = scaler_X.transform(X)
        print(f"Scaler loaded from {scaler_path}")
    
    X = torch.tensor(X, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.float32)
    return X, y

if __name__ == "__main__":
    get_tensor_data()
