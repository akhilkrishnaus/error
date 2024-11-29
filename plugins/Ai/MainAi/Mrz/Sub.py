from pyrogram import Client, filters
import aiohttp

@Client.on_message(filters.command("sts", prefixes=["/"]))
async def search_subtitle(client, message):
    # Extract the query from the message
    query = message.text[len("/sts "):]
    
    if not query:
        await message.reply_text("Please provide a search query.")
        return

    # Encode the query for the URL
    encoded_query = query.replace(" ", "%20")

    # Make the request to the subtitle API
    url = f"https://api.safone.dev/subtitle?query={encoded_query}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                
                if data["results"]:
                    results = data["results"]
                    # Use a conditional to check if 'link' exists in result
                    reply_text = "\n\n".join([
                        f"Title: {result['title']}\nLink: {result['link']}" 
                        if 'link' in result else f"Title: {result['title']}\nLink: Not available"
                        for result in results
                    ])
                else:
                    reply_text = "No subtitles found for your query."
            else:
                reply_text = "Failed to fetch subtitles. Please try again later."

    await message.reply_text(reply_text)
