from pyrogram import *
from pyrogram import Client as check
import requests

@check.on_message(filters.command("check"))
async def bin_checker(client, message):
  if len(message.command) < 2:
        return await message.reply_text("Give An 6 number input.")

  num = " ".join(message.command[1:])
  url = f"https://api.safone.dev/bininfo?bin={num}"
  response = requests.get(url)
  res = response.json()
  bank = res['bank']
  bin = res['bin']
  country = res['country']
  flag = res['flag']
  card = res['vendor']
  await message.reply_text(f"𝗕𝗜𝗡 <code>{bin}</code>\n\n𝗕𝗔𝗡𝗞 <code>{bank}</code>\n\n𝗖𝗢𝗨𝗡𝗧𝗥𝗬 <code>{country}</code>{flag}\n\n𝗖𝗔𝗥𝗗 <code>{card}</code>")
  
