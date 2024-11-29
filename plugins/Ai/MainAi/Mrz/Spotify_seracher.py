import requests
from pyrogram import Client, filters

# Define the API endpoint and bot token
api_url = "https://api.safone.dev/spotify"

# Define the search command handler
@Client.on_message(filters.command("spotify"))
async def search_spotify(client, message):
    query = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    limit = 5

    if not query:
        await message.reply_text("Please provide a search query.")
        return

    response = requests.get(api_url, params={"query": query, "limit": limit})

    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])

        if not results:
            await message.reply_text("No results found.")
            return

        for result in results:
            reply_text = (
                f"**Title:** {result['title']}\n"
                f"**Album:** {result['album']}\n"
                f"**Artist:** {', '.join(result['artist'])}\n"
                f"**Duration:** {result['duration']}\n"
                f"**Genres:** {', '.join(result['genres'])}\n"
                f"**Popularity:** {result['popularity']}\n"
                f"**Release Date:** {result['releaseDate']}\n"
                f"[Song URL]({result['songUrl']})\n"
                f"[Album URL]({result['albumUrl']})\n"
                f"[Artist URL]({result['artistUrl']})\n"
                f"[Image URL]({result['imageUrl']})"
            )
            await message.reply_text(reply_text, disable_web_page_preview=True)
    else:
        await message.reply_text(f"Failed to fetch data from API. Status code: {response.status_code}")
