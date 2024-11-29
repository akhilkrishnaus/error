from pyrogram import Client, filters
import random
import time

def generate_wish_code() -> str:
    random.seed(time.time())
    code = ''.join(str(random.randint(0, 9)) for _ in range(6))
    return code

@Client.on_message(filters.command("wish"))
def wish(client, message):
    wish_code = generate_wish_code()
    message.reply_text(f'Your wish code is: {wish_code}')
