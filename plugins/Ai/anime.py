from pyrogram import *
import asyncio
import requests
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton , CallbackQuery , Message


def shorten(description):
    msg = ""
    if len(description) > 200:
        description = description[0:200] + "..."
        msg += f"{description}"
    else:
        msg += f"{description}"
    return msg


@Client.on_message(filters.command("anime"))
async def genshin_character(_: Client, message: Message):
    text = "".join(message.text.split(" ")[1:])
    if len(text) == 0:
        return await message.reply_text(
            "Cannot reply to empty message.", parse_mode=ParseMode.MARKDOWN
        )

    m = await message.reply_text("Gathering Infromation....", parse_mode=ParseMode.MARKDOWN)
    response = requests.get("https://api.safone.dev/anime/search?query=" + text)
    if response.status_code == 200:
        data = response.json()
        data_end = response.json()['endDate']
        data_st = response.json()['startDate']
        data_t = response.json()['title']
        imx = data ['imageUrl']
        desc = data ['description']
        mxg = shorten(desc)
        avg = data ['averageScore']
        ep = data ['episodes']
        sea = data ['season']
        studios = data ['studios']
        eday = data_end ['day']
        emonth = data_end ['month']  
        eyear = data_end ['year']
        sday = data_st ['day']
        smonth = data_st ['month']  
        syear = data_st ['year']
        status = data ['status']
        title =  data_t ['english']
        photo_sr = imx
        genres = data ['genres']
        sr_char = f"""

**Title:** {title}
**Total Episodes:** {ep}
**End Date:** {eday}/{emonth}/{eyear}
**Start Date:** {sday}/{smonth}/{syear}
**Status:** {status}
**Season:** {sea}
**Studio:** `{studios}`
**Avg Score:** {avg}      
**Description :**{mxg}
**Genres:** `{genres}` 

"""

    await message.reply_photo(photo=photo_sr, caption= sr_char, parse_mode=ParseMode.MARKDOWN )
    await m.delete()
