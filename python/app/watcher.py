import time
from os import makedirs, path
from random import randint
from threading import Thread

from app.config import AFTER, BEFORE
from app.utils import compute_similarity, save_photo
from bot.utils import send_telegram


def watch():
    """
    The main watch function in an infinite loop will
    save 'before' and 'after' photos
    and then compute a difference between two...
    if it's relevent enought, it will notify
    the user with the configurated chat-id

    """
    # We create the repository for images payload if it doesn't exist
    if not path.exists("./data"):
        makedirs("./data")

    print("[-] BOMBO started...")
    # A small wait
    time.sleep(5)

    # An infinite loop for the BOMBO fetch of images
    while True:
        try:
            # let's take a picture...
            save_photo(BEFORE)

            # then we wait 10 seconds (2 mins)
            time.sleep(10)

            # let's take a picture...
            save_photo(AFTER)

            # Compute Structural similarity between two images
            (score, diff) = compute_similarity()
            print("[-] Percent of image similarity: ", score)

            if score < 0.9:
                status = send_telegram(
                    f"Hey there, i Noticed something new in your "
                    f'"boite aux lettres" with accuracy of {score * 100}%,'
                    "\nhit /no if you want me to ignore or it's just a magazine,"
                    "\n\nI need to confirm that because am continuously learning"
                    " what can be a useless inbox/adds or what is a real new thing"
                )
                if not status[0]:
                    print(f"[x] There was an error {status[1]}")

            # we wait a long time
            time.sleep(randint(10, 30))
        except Exception as es:
            pass


def start_watch_thread(t: Thread):
    """
    We start the watcher on thread mode
    """
    t.daemon = True
    t.start()


def stop_watch_thread(t):
    """
    We stop the watcher on thread mode
    """
    t.join()
