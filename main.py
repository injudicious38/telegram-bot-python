
import os
import time
import telebot
from dotenv import load_dotenv
from commands import register_commands

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

try:
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is missing")

    bot = telebot.TeleBot(TOKEN)
    register_commands(bot)

    @bot.message_handler(commands=["start", "hello"])
    def send_welcome(message):
        bot.reply_to(
            message,
            "Hello! 👋 Welcome to my bot.\n\n"
            "I'm here to help. Send /help to see my commands!"
        )

    # Automatically welcome new members in groups
    @bot.message_handler(
        content_types=["new_chat_members"]
    )
    def welcome_new_members(message):
        for member in message.new_chat_members:
            if member.is_bot:
                continue

            welcome_text = (
                f"👋 Welcome to the group, {member.first_name}!\n\n"
                "We're glad you're here! 🎉\n"
                "Please read the group rules and enjoy your stay."
            )

            bot.send_message(
                message.chat.id,
                welcome_text
            )

    # Echo text messages in private chats only
    @bot.message_handler(
        func=lambda msg: msg.chat.type == "private",
        content_types=["text"]
    )
    def echo_all(message):
        bot.reply_to(message, message.text)

    # Remove webhook to avoid conflicts with polling
    bot.delete_webhook(drop_pending_updates=True)
    print("Bot is running!")
    bot.infinity_polling()

except Exception as e:
    print(f"Bot error: {e}")
    raise
