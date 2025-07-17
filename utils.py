from pathlib import Path
import matplotlib.pyplot as plt
import os

def savePlot(path: str) -> None:
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def check_asset_exists(path: str) -> bool:
    return Path(path).exists()

def new_dir(path: str) -> None:
    if not check_asset_exists(path):
        os.makedirs(path, exist_ok=True)
    return