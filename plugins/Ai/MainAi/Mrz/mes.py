from pyrogram import Client, filters
from datetime import datetime

# List to store scheduled events
events = []

@Client.on_message(filters.command("schedule"))
async def schedule_event(client, message):
    try:
        # Example command: /schedule event_name yyyy-mm-dd hh:mm
        command = message.text.split()
        if len(command) < 4:
            await message.reply("Usage: /schedule <event_name> <yyyy-mm-dd> <hh:mm>")
            return

        event_name = command[1]
        event_time = datetime.strptime(f"{command[2]} {command[3]}", "%Y-%m-%d %H:%M")
        events.append((event_name, event_time))

        await message.reply(f"Event '{event_name}' scheduled for {event_time}.")
    except ValueError:
        await message.reply("Invalid date format. Use yyyy-mm-dd for the date and hh:mm for the time.")

@Client.on_message(filters.command("events"))
async def list_events(client, message):
    if not events:
        await message.reply("No events scheduled.")
        return

    event_list = "\n".join([f"{event[0]} at {event[1]}" for event in events])
    await message.reply(f"Scheduled Events:\n{event_list}")

@Client.on_message(filters.command("delete_event"))
async def delete_event(client, message):
    try:
        # Example command: /delete_event event_name
        command = message.text.split()
        if len(command) != 2:
            await message.reply("Usage: /delete_event <event_name>")
            return

        event_name = command[1]
        global events
        events = [event for event in events if event[0] != event_name]

        await message.reply(f"Event '{event_name}' deleted.")
    except Exception as e:
        await message.reply("An error occurred.")
