import torch

# command for Intel Arc: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/xpu

# I have a Intel Arc GPU. 
if not torch.xpu.is_available() and torch.xpu.device_count() >= 1:
    raise Exception("run the command: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/xpu")
device = torch.device("xpu")
