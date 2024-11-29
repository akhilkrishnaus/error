import requests
from pyrogram import *

@Client.on_message(filters.command("truth"))
async def truth_say(client, message):
  url = "https://api.safone.dev/truth?category=mixed"
  response = requests.get(url)
  res = response.json()
  truth = res['truth']
  await message.reply_text(truth)
