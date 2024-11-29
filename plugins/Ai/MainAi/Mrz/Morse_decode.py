import requests
from pyrogram import Client, filters

# Function to decode Morse code using the API
def decode_morse(morse_code):
    response = requests.get(f'https://api.safone.dev/morse/decode?text={morse_code}')
    if response.status_code == 200:
        data = response.json()
        return data.get('decoded', 'Error decoding Morse code')
    else:
        return 'Error decoding Morse code'

# Command handler for /decode
@Client.on_message(filters.command('decode') & filters.private)
async def decode(client, message):
    if len(message.command) < 2:
        await message.reply_text('Please provide the Morse code to decode. Usage: /decode <morse_code>')
        return

    morse_code = message.text.split(' ', 1)[1]
    decoded_text = decode_morse(morse_code)
    await message.reply_text(f'Decoded text: {decoded_text}')
