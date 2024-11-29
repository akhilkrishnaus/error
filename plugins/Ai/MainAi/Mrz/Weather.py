import requests
from pyrogram import Client, filters

# Define a function to get weather emoji based on description
def get_weather_emoji(description):
    description = description.lower()
    if "sunny" in description or "clear" in description:
        return "☀️"
    elif "cloud" in description:
        return "☁️"
    elif "rain" in description:
        return "🌧️"
    elif "thunderstorm" in description:
        return "⛈️"
    elif "snow" in description:
        return "❄️"
    elif "fog" in description or "mist" in description:
        return "🌫️"
    else:
        return "🌈"

# Define a command handler
@Client.on_message(filters.command("weather", prefixes="/"))
async def weather(bot, update):
    try:
        # Extract the city from the command message
        city = update.text.split(maxsplit=1)[1].strip()
    except IndexError:
        # If there's an IndexError (e.g., no city provided), handle it gracefully
        await update.reply_text("Please provide a city name after the /weather command.")
        return

    # Construct the API URL
    url = f"https://api.safone.dev/weather?city={city}"

    # Make a GET request to the API
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        try:
            data = response.json()
            # Print or log the actual response for debugging purposes
            print(f"API Response: {data}")

            # Extract current weather details
            description = data.get('description', 'No description available')
            current_temperature = data.get('temperature', 'N/A')
            current_wind = data.get('wind', 'N/A')
            emoji = get_weather_emoji(description)

            # Extract forecast details
            forecast = data.get('forecast', [])
            forecast_message = ""
            for day_forecast in forecast:
                day = day_forecast.get('day', 'N/A')
                temp = day_forecast.get('temperature', 'N/A')
                wind = day_forecast.get('wind', 'N/A')
                forecast_message += (
                    f"{emoji} Day: {day}\n"
                    f"Temperature: {temp}°C\n"
                    f"Wind: {wind}\n\n"
                )

            # Format the weather information with summary and forecast
            message = (
                f"{emoji} Weather Description: {description}\n\n"
                f"Current Temperature: {current_temperature}°C\n"
                f"Current Wind: {current_wind}\n\n"
                f"Forecast:\n{forecast_message}"
            )
        except ValueError:
            message = "Error decoding JSON response from the API."
            # Print or log the actual response text for debugging purposes
            print(f"Error decoding JSON response: {response.text}")
    else:
        message = "Error fetching weather data. Please try again later."

    # Send the message back to the user
    await update.reply_text(message)
