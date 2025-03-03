import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from youtube_dl import YoutubeDL
from pydub import AudioSegment

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram bot token (replace with your token)
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Function to download audio from YouTube
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio.%(ext)s',  # Output file name
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        base, _ = os.path.splitext(filename)
        audio_file = f"{base}.mp3"
    return audio_file

# Command to start the bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Send me a YouTube link, and I'll send you the audio.")

# Handle YouTube links
def handle_message(update: Update, context: CallbackContext):
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        update.message.reply_text("Downloading audio... Please wait.")
        try:
            audio_file = download_audio(url)
            update.message.reply_audio(audio=open(audio_file, 'rb'))
            os.remove(audio_file)  # Clean up the file
        except Exception as e:
            logger.error(f"Error downloading audio: {e}")
            update.message.reply_text("Sorry, something went wrong. Please try again.")
    else:
        update.message.reply_text("Please send a valid YouTube link.")

# Error handler
def error(update: Update, context: CallbackContext):
    logger.warning(f'Update {update} caused error {context.error}')

# Main function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command and message handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
