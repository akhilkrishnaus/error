import requests
from pyrogram import Client, filters

@Client.on_message(filters.command("madmax"))
async def llama_ai(client, message):
    # Extract query and handle empty input
    query = message.text.split()[1:]
    if not query:
        await message.reply_text("Give An Input!")
        return

    # Combine query parts for a clean string
    query_text = " ".join(query)

    # Handle special cases (owner info) more efficiently
    if query_text.lower() in ("who is your owner", "what is your owner name"):
        await message.reply_text(f"My owner is @MRXSUPPORTS")
        return

    # Construct API URL with formatted query
    url = f"https://api.safone.dev/llama?query={query_text}"

    # Send API request and handle potential errors
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-200 status codes

        # Extract and return answer
        llma_data = response.json()
        llama_answer = llma_data['answer']
        await message.reply_text(llama_answer)
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")  # Log the error for debugging
        await message.reply_text("An error occurred. Please try again later.")
