import json
import aiohttp
from pyrogram import Client, filters
import urllib.parse

@Client.on_message(filters.command("removebg", prefixes="."))
async def remove_bg(client, message):
    try:
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.reply_text("Please reply to an image to remove its background.")
            return

        # Download the photo
        photo = await message.reply_to_message.download()

        # Upload the photo to a hosting service to get a public URL
        # Here we'll assume you already have the URL for simplicity
        # For actual implementation, you might need to upload the photo first
        photo_url = "https://i.ibb.co/tb2K5J8/download.jpg"  # Replace with the actual URL

        # Encode the photo URL for the GET request
        encoded_url = urllib.parse.quote(photo_url, safe='')

        # Construct the API URL
        api_url = f"https://api.safone.dev/removebg?image={encoded_url}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status != 200:
                    await message.reply_text(f"Failed to remove background: {resp.status}")
                    return
                result = await resp.json()

        # Save the result image
        no_bg_image_path = "no_bg_image.png"
        async with session.get(result["data"]["url"]) as resp:
            with open(no_bg_image_path, 'wb') as f:
                f.write(await resp.read())

        # Send the result image
        await message.reply_photo(no_bg_image_path)

    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
