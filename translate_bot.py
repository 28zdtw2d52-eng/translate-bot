import os
from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.environ["BOT_TOKEN"]
TARGET = os.getenv("TARGET_LANG", "ru")


def translate(text: str) -> str:
    return GoogleTranslator(source="auto", target=TARGET).translate(text[:4999])


async def on_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.channel_post
    text = msg.text or msg.caption
    if not text:
        return
    await msg.reply_text(translate(text))


async def on_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg and msg.text:
        await msg.reply_text(translate(msg.text))


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(
        MessageHandler(
            filters.UpdateType.CHANNEL_POST & (filters.TEXT | filters.CAPTION),
            on_channel_post,
        )
    )
    app.add_handler(
        MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, on_private)
    )
    app.run_polling()


if __name__ == "__main__":
    main()
