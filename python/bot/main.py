from threading import Thread

from telegram.ext import CommandHandler, Updater

from app.config import CHAT_ID, TOKEN
from app.watcher import start_watch_thread, stop_watch_thread, watch

T = Thread(target=watch)


def start_callback(bot, update):
    print("[+] start-callback")

    chat_id = update.message.chat_id

    if str(chat_id) != str(CHAT_ID):
        message = (
            "I don't know your chat-id, you should set it "
            "with the physical esp module first !"
            "\nYou can also contact the developer @sanixdarker to know more !"
            "\n\nYou can hit /help to get the help !"
        )
    else:
        message = (
            "Starting from now i will send you photo of "
            'your "boite aux lettres" when i '
            "will detect it may be a change in the content itself !"
            "\nYou can hit /stop to let me know i should "
            "stop sending you notifications !"
            "\n\nYou can hit /help to get the help !"
        )
        # We start the thread of the watcher
        start_watch_thread(T)

    bot.send_message(chat_id=chat_id, text="Hello there, \n" + message)


def stop_callback(bot, update):
    print("[+] stop-callback")

    chat_id = update.message.chat_id

    if str(chat_id) != str(CHAT_ID):
        message = (
            "I don't know your chat-id, you should set it "
            "with the physical esp module first !"
            "\nYou can also contact the developer @sanixdarker to know more !"
            "\n\nYou can hit /help to get the help !"
        )
    else:
        message = (
            "Because you asked that, i will stop sending you notifications "
            "if i detect there is something new in your mail box"
            "\n\nYou can hit /help to get the help !"
        )
        # We stop the thread of the watcher
        stop_watch_thread(T)

    bot.send_message(chat_id=chat_id, text="Hello there, \n" + message)


def no_callback(bot, update):
    print("[+] help-callback")
    # TODO: the AI/ML/Learning service will be done for this callback in part 2
    chat_id = update.message.chat_id

    message = (
        "'No' triggered, that means i should avoid next time "
        "sending you notifications for something looking like that photo ! "
    )

    bot.send_message(chat_id=chat_id, text=message)


def help_callback(bot, update):
    print("[+] help-callback")

    chat_id = update.message.chat_id

    message = (
        "This is the main list of commands you will need: "
        "\n/start : That will start the bot who will "
        "fetch continuously to see change on the mailbox"
        "\n/stop : That will stop the bot job as well"
        "\n/help :  TO give you the list of commands"
        "\n\nYou can hit /help to get the help !"
    )

    bot.send_message(chat_id=chat_id, text="Hello there, \n" + message)


start_handler = CommandHandler("start", start_callback)
stop_handler = CommandHandler("stop", stop_callback)
help_handler = CommandHandler("help", help_callback)
no_handler = CommandHandler("no", no_callback)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(start_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(no_handler)

if __name__ == "__main__":
    updater.start_polling()
    updater.idle()
