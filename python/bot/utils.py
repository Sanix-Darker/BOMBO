import requests

from app.config import AFTER, CHAT_ID, TOKEN


def send_telegram(text: str):
    """
    This method will just send a message to the appropriate client

    text: the input message
    """
    datas = {
        "chat_id": CHAT_ID,
        "caption": text,
    }
    with open(f"./data/{AFTER}", "rb") as image_file:
        res = requests.post(
            url="https://api.telegram.org/bot" + TOKEN + "/sendPhoto",
            data=datas,
            files={"photo": image_file},
        )

    return res.status_code == 200, res.json()
