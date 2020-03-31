import re
import requests
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Hi! I am Amiel\'s sexbot, type /doge or /cat for a surprise')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def get_dog_url():
    # Get random dog url from json
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def get_dog_image_url():
    # Get random dog image url
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_dog_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


@run_async
def doge(update, context):
    # Send random dog image
    url = get_dog_image_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)


def get_cat_url():
    # Get random cat url from json
    contents = requests.get(
        'https://api.thecatapi.com/v1/images/search').json()
    contents = contents[0]
    url = contents['url']
    return url


def get_cat_image_url():
    # Get random cat image url
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_cat_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


@run_async
def cat(update, context):
    # Send random cat image
    url = get_cat_image_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        "1012535764:AAHvhJ5sJy-bU7kpR9Fr3YNEaSNHFSXm0ao", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("doge", doge))
    dp.add_handler(CommandHandler("cat", cat))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()