from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests

# Safone API endpoint for playlist search
API_URL = "https://api.safone.dev/playlist"

# Command handler for /playlist command
@Client.on_message(filters.command("playlist"))
async def playlist_search(client, message):
    # Extract query from command arguments
    query = message.text.split(" ", 1)[1].strip() if len(message.text.split(" ")) > 1 else ""

    if query:
        # Make GET request to Safone API
        response = requests.get(API_URL, params={"query": query, "limit": 10})

        if response.status_code == 200:
            playlists = response.json()["results"]

            # Generate and send message with results
            for playlist in playlists:
                keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Watch Playlist", url=playlist["link"])]])
                message_text = f"Title: {playlist['title']}\nChannel: {playlist['channel']['name']}\nVideos: {playlist['videoCount']}"
                await client.send_photo(message.chat.id, playlist["thumbnails"][0]["url"], caption=message_text, reply_markup=keyboard)
        else:
            await client.send_message(message.chat.id, "Failed to fetch playlists. Please try again later.")
