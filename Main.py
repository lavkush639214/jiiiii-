import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from youtubesearchpython import VideosSearch

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define command handlers
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! I am your music bot. Use /play <song_name> to search for a song.')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Use /play <song_name> to search for a song.')

def play(update: Update, context: CallbackContext) -> None:
    if not context.args:
        update.message.reply_text('Please provide a song name after /play command.')
        return

    song_name = ' '.join(context.args)
    videos_search = VideosSearch(song_name, limit=1)
    results = videos_search.result()

    if results['result']:
        video = results['result'][0]
        title = video['title']
        link = video['link']
        update.message.reply_text(f'Here is the link to the song "{title}": {link}')
    else:
        update.message.reply_text('No results found.')

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("play", play))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
