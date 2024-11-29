from pyrogram import Client, filters
import requests

@Client.on_message(filters.command("lyrics"))
async def get_lyrics(client, message):
    args = message.text.split(" ")
    if len(args) < 2:
        await message.reply_text("**Please provide a song name!** 🔎")
        return

    song_name = " ".join(args[1:])  # Join the rest of the args to handle multi-word song names
    api = f"https://horrid-api.onrender.com/lyrics?song={song_name}"
    
    try:
        response = requests.get(api)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        # Check if the required keys are in the response
        title = data.get('title', 'Title not found')
        artist = data.get('artist', 'Artist not found')
        lyrics = data.get('lyrics', 'Lyrics not found')

        await message.reply_text(f"**Title:** {title}\n**Artist:** {artist}\n\n__Lyrics:__\n{lyrics}")

    except requests.RequestException as e:
        # Handle network-related errors
        await message.reply_text(f"**Error fetching lyrics:** {str(e)}")
    except ValueError:
        # Handle JSON decoding errors
        await message.reply_text("**Error decoding response.**")
