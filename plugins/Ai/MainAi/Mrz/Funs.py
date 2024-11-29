from pyrogram import filters
from pyrogram import Client
import requests 
from HorridAPI import api

@Client.on_message(filters.command("dare"))
async def dare(client, g):
  api = requests.get("https://horrid-api.onrender.com/dare").json()
  text = api["dare"]               
  await g.reply_text(text)
         

@Client.on_message(filters.command("truth"))
async def truth(client, g):
  api = requests.get("https://horrid-api.onrender.com/truth").json()
  text = api["truth"]               
  await g.reply_text(text)



@Client.on_message(filters.command("joke"))
async def jokeda(client, g):
  api = requests.get("https://horrid-api.onrender.com/joke").json()
  text = api["joke"]               
  await g.reply_text(text)
