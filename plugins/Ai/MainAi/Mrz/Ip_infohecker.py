import requests
from pyrogram import Client, filters
import asyncio
from datetime import datetime
import pytz

# Command to get IP information
@Client.on_message(filters.command("ipinfo"))
async def ip_info(client, message):
    try:
        # Extract the IP address from the message
        ip_address = message.text.split(" ", 1)[1]
        
        # Send the sticker first
        sticker_message = await message.reply_sticker("CAACAgQAAxkBAAIav2aJXr9WgCsyzWEVNPfs1352ByujAAJuDwAC4eqxUNoxB5joJxGiHgQ")
        
        # Simulate delay time for fetching data
        await asyncio.sleep(3)  # Adjust delay time as necessary

        # Send a request to the IP-API
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        
        if response.status_code == 200:
            ip_info = response.json()
            if ip_info['status'] == 'fail':
                info_text = f"Error: {ip_info['message']}"
            else:
                # Get the current date and time in IST
                ist = pytz.timezone('Asia/Kolkata')
                current_datetime = datetime.now(ist)

                # Format the response
                info_text = (
                    f"ʜᴇʏ: {message.from_user.mention}\n\n"
                    f"ϙᴜᴇʀʏ: {ip_address}\n\n"
                    f"ʀᴇsᴜʟᴛ:\n\n"
                    f"**IP Address:** {ip_info.get('query')}\n"
                    f"**Country:** {ip_info.get('country')}\n"
                    f"**Region:** {ip_info.get('regionName')}\n"
                    f"**City:** {ip_info.get('city')}\n"
                    f"**ZIP:** {ip_info.get('zip')}\n"
                    f"**Latitude:** {ip_info.get('lat')}\n"
                    f"**Longitude:** {ip_info.get('lon')}\n"
                    f"**ISP:** {ip_info.get('isp')}\n"
                    f"**Organization:** {ip_info.get('org')}\n"
                    f"**AS:** {ip_info.get('as')}\n\n"
                    f"Date and Time (IST): {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    f"Provided by @Mrz_bots"
                )
        else:
            info_text = "Unable to fetch information. Please try again later."
        
    except IndexError:
        info_text = "Please provide an IP address after the command. Example: /ipinfo 8.8.8.8"
    except Exception as e:
        info_text = f"An error occurred: {str(e)}"
    
    # Delete the sticker message
    await sticker_message.delete()
    
    # Send the information message
    await message.reply_text(info_text)
