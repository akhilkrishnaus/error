import requests
from pyrogram import Client, filters

# Define the /morse command handler
@Client.on_message(filters.command("morse"))
async def morse(client, message):
    # Extract the text to encode from the message
    if len(message.command) < 2:
        await message.reply_text("Please provide text to encode in Morse code.")
        return

    text_to_encode = " ".join(message.command[1:])

    # Make a request to the Morse code API
    api_url = f"https://api.safone.dev/morse/encode?text={text_to_encode}"
    response = requests.get(api_url)

    if response.status_code == 200:
        try:
            response_data = response.json()
            if response_data.get("success"):
                morse_code = response_data.get("encoded", "Error: Unable to encode text")
                await message.reply_text(f"Morse Code: {morse_code}")
            else:
                await message.reply_text(f"Error: {response_data.get('error', 'Unknown error')}")
        except ValueError:
            await message.reply_text(f"Error: Unable to parse JSON response: {response.text}")
    else:
        await message.reply_text(f"Error: Unable to contact the Morse code API. Status code: {response.status_code}, Response: {response.text}")
