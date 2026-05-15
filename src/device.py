import torch


def get_best_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")

    xpu = getattr(torch, "xpu", None)
    if xpu is not None and xpu.is_available():
        return torch.device("xpu")

    return torch.device("cpu")
