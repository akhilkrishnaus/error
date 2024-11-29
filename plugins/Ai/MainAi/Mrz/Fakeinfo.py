import os
import requests
import asyncio
from pyrogram import Client, filters
from datetime import datetime
import pytz

# Get the Safone API token from environment variables
SAFONE_API_TOKEN = os.getenv("SAFONE_API_TOKEN")

# Function to fetch fake information by country from Safone API
def get_fake_info_by_country(country):
    url = f"https://api.safone.dev/fakeinfo?country={country}"
    headers = {
        "Authorization": f"Bearer {SAFONE_API_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    
    print(f"Request URL: {url}")
    print(f"Request Headers: {headers}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch fake info for {country} from Safone API: {response.text}"}

# Command handler for /fakeinfo command
@Client.on_message(filters.command("fakeinfo"))
async def fakeinfo_command(client, message):
    # Extract country from command arguments
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Please specify a country. Example: /fakeinfo India")
        return
    
    country = args[1]
    
    # Send the animation sticker
    sticker_message = await message.reply_sticker("CAACAgQAAxkBAAIav2aJXr9WgCsyzWEVNPfs1352ByujAAJuDwAC4eqxUNoxB5joJxGiHgQ")
    
    # Introduce a delay to simulate processing time
    await asyncio.sleep(2)  # Adjust the delay time as needed
    
    fake_info = get_fake_info_by_country(country)
    
    if "error" in fake_info:
        await message.reply_text(fake_info["error"])
    else:
        try:
            # Construct the formatted message with selected fields
            result = (
                f"👤 Name: {fake_info['name']['title']} {fake_info['name']['first']} {fake_info['name']['last']}\n"
                f"📧 Email: {fake_info['email']}\n"
                f"🚻 Gender: {fake_info['gender']}\n"
                f"📞 Phone: {fake_info['phone']}\n"
                f"📅 Date of Birth: {fake_info['dob']['date']} (Age: {fake_info['dob']['age']})\n"
                f"🌍 Location: {fake_info['location']['city']}, {fake_info['location']['country']} ({fake_info['location']['coordinates']['latitude']}, {fake_info['location']['coordinates']['longitude']})\n"
                f"🏢 Street: {fake_info['location']['street']['name']} {fake_info['location']['street']['number']}\n"
                f"🔑 Login: {fake_info['login']['username']} ({fake_info['login']['md5']})\n"
                f"📱 User Agent: {fake_info['useragent']}\n"
                f"🌐 Nationality: {fake_info['nat']}\n"
                f"🆔 UUID: {fake_info['login']['uuid']}\n"
                f"⏰ Timezone: {fake_info['location']['timezone']['description']} (Offset: {fake_info['location']['timezone']['offset']})\n"
                f"🖼️ Profile Picture: {fake_info['picture']['large']}\n"
            )
            
            # Get the user's full name
            user_full_name = message.from_user.first_name + (f" {message.from_user.last_name}" if message.from_user.last_name else "")
            
            # Get current date and time in IST
            ist = pytz.timezone('Asia/Kolkata')
            current_datetime = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')
            
            # Construct the final message
            final_message = (
                f"ʜᴇʏ: {user_full_name}\n\n"
                f"ϙᴜᴇʀʏ: {country}\n\n"
                f"ʀᴇsᴜʟᴛ:\n\n{result}\n\n"
                f"Date and Time (IST): {current_datetime}\n\n"
                f"Provided by @Mrz_bots"
            )
            
            # Delete the sticker message
            await client.delete_messages(chat_id=message.chat.id, message_ids=sticker_message.message_id)
            
            await message.reply_text(final_message)
        
        except KeyError as e:
            await message.reply_text(f"Failed to parse response: KeyError - {e}")
