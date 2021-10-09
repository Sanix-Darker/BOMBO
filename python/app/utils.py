import time

import requests
from skimage.metrics import structural_similarity

try:
    import cv2
except ImportError:
    import cv2.cv2 as cv2

from app.config import AFTER, BEFORE, BOMBO_IP


def capture():
    """
    THis function will contact the camera ip address
    module and ask it to take a picture
    :return:
    """
    print("[-] taking capture...")

    # let's take a picture...
    requests.get(f"{BOMBO_IP}/capture")
    # then we wait 5 second
    time.sleep(5)


def save_photo(path: str):
    """
    THis small method will just perform a GET request
     to the esp to get the saved photo

    :param path:
    :return:
    """
    capture()

    print(f"[-] Saving the photo {path}...")

    # We request the picture
    req = requests.get(f"{BOMBO_IP}/photo")
    # and save it
    with open(f"./data/{path}", "wb") as f:
        f.write(req.content)


def compute_similarity():
    """
    This main function will compute/caluculate the
    similarity percent of two image and return the score

    :return:
    """
    before_bin = cv2.imread(f"./data/{BEFORE}")
    after_bin = cv2.imread(f"./data/{AFTER}")
    # then we try to compare those
    # Convert images to grayscale
    before_gray = cv2.cvtColor(before_bin, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(after_bin, cv2.COLOR_BGR2GRAY)

    # Compute Structural similarity between two images
    return structural_similarity(before_gray, after_gray, full=True)
