import requests
from pyrogram import Client, filters
from datetime import datetime
import asyncio

# Define a descriptive constant for the API URL
API_URL = "https://horrid-api.vercel.app/llama"

@Client.on_message(filters.command(["llamaai"]))
async def handle_llama_command(client, message):
    """Processes user queries using the Llama AI API."""

    # Check for missing input with a clear and concise message
    if len(message.command) < 2:
        return await message.reply_text("Hey! Please provide some text for me to analyze.")

    # Extract the user's query and provide initial feedback
    query = " ".join(message.command[1:])
    
    # Check for specific queries and provide predefined responses
    predefined_responses = {
        "what is your name": (
            "I'm called Mr.Tom. I was developed to give you information, complete tasks, and assist you in various manners.\n\n"
            "Provided by @MRXSUPPORTS"
        ),
        "who is cooltech": (
            "MMW BOTZ is an exceptionally skilled developer who serves as my guardian in this realm. "
            "Initially, I wasn't a coder, but I've acquired expertise in AI programming. "
            "When it comes to sports, I admire Rohit Sharma, famously known as 'Hitman,' for his remarkable batting, "
            "and Jasprit Bumrah for his outstanding bowling. Additionally, MMW BOTZ is active on YouTube.\n\n"
            "Provided by @MRXSUPPORTS"
        ),
        "who is your owners": (
            "My proprietor is @altelegram1. I function as an AI assistant programmed to deliver information, execute tasks, and provide multifaceted assistance.\n\n"
            "Provided by @MRXSUPPORTS"
        ),
        "who is your developed": (
            f"You are Mr.Tom, engineered by @MRXSUPPORTS and managed by @aktelegram1. You are operational as of {datetime.now().strftime('%Y-%m-%d')}.\n\n"
            "Provided by @MRXSUPPORTS"
        ),
        "who is your developer": (
            f"You are Mr.Tom, engineered by @MRXSUPPORTS and managed by @aktelegram1. You are operational as of {datetime.now().strftime('%Y-%m-%d')}.\n\n"
            "Provided by @MRXSUPPORTS"
        ),
        "today date": (
            f"Today's date is {datetime.now().strftime('%Y-%m-%d')}.\n\n"
            "Provided by @MRXSUPPORTS"
        )
    }

    if query.lower() in predefined_responses:
        response_message = predefined_responses[query.lower()]
        return await message.reply_text(response_message)

    thinking_message = await message.reply_text("Thinking like a llama...")

    try:
        # Fetch response from Llama AI using f-string formatting
        response = requests.get(f"{API_URL}?query={query}").json()

        # Check if response contains 'response' key
        if 'response' in response:
            user_full_name = message.from_user.first_name
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_response = (
                f"ʜᴇʏ: {message.from_user.mention}\n\n"
                f"ϙᴜᴇʀʏ: {query}\n\n"
                f"ʀᴇsᴜʟᴛ:\n\n{response['response']}\n\n"
                f"Date and Time (IST): {current_datetime}\n\n"
                f"Provided by @MRXSUPPORTS"
            )

            sticker = await message.reply_sticker("CAACAgQAAxkBAAIav2aJXr9WgCsyzWEVNPfs1352ByujAAJuDwAC4eqxUNoxB5joJxGiHgQ")
            await asyncio.sleep(2)  # Adjust the delay as needed
            await sticker.delete()

            await thinking_message.edit(formatted_response)
        else:
            await thinking_message.edit("Hmm, couldn't retrieve a valid response from Llama AI.")

    except requests.exceptions.RequestException as e:
        # Handle requests exceptions
        error_message = f"Hmm, something went wrong with the request: {str(e)}"[:100] + "..."
        await thinking_message.edit(error_message)

    except Exception as e:
        # Handle other exceptions gracefully
        error_message = f"Hmm, something went wrong: {str(e)}"[:100] + "..."
        await thinking_message.edit(error_message)
