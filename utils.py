from pathlib import Path
import matplotlib.pyplot as plt
import os
import requests

def savePlot(path: str) -> None:
    """Saves the current matplotlib figure to a file and closes the plot.

    Args:
        path (str): Output file path (e.g., 'plot.png').
                   Supported formats: PNG, JPG, PDF, SVG, etc.
    """
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close('all')
    return


def check_asset_exists(path: str) -> bool:
    """ Checks if the provided asset exits.
    
    Args:
        path (str): Path to file 
    
    Output:
        bool depending on if it found the asset or not
    """
    return Path(path).exists()

def new_dir(path: str) -> None:
    if not check_asset_exists(path):
        os.makedirs(path, exist_ok=True)
    return

def download(url: str, path:str) -> None:
    """Downloads a file from a URL and saves it locally.

    Args:
        url (str): The URL of the file to download.
        path (str): Local filesystem path where the file will be saved.

    Raises:
        requests.exceptions.RequestException: If the download fails (e.g., network error).
    """
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)
    return 
