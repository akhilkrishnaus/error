import requests
from pyrogram import Client, filters
from pyrogram.types import Message
import time

# Privatix Temp Mail API details
TEMP_MAIL_API_HOST = "privatix-temp-mail-v1.p.rapidapi.com"
TEMP_MAIL_API_KEY = "b8e82898bfmshe2e5e54251fbd68p17b17ajsn1eb75ed8304a"

# Store user emails and their corresponding email IDs
user_emails = {}

# Command to generate a temporary email for the user
@Client.on_message(filters.command("generatemail"))
async def generate_email(client: Client, message: Message):
    user_id = message.from_user.id
    
    # Generate a temporary email
    url = f"https://{TEMP_MAIL_API_HOST}/request/domains/"
    
    headers = {
        "x-rapidapi-key": TEMP_MAIL_API_KEY,
        "x-rapidapi-host": TEMP_MAIL_API_HOST
    }
    
    # Fetch available domains
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        domains = response.json()
        if domains:
            # Construct a random email (username+domain)
            email_username = f"user{user_id}"
            temp_email = f"{email_username}@{domains[0]}"  # Using the first domain
            
            # Store email for the user
            user_emails[user_id] = temp_email
            
            await message.reply(f"Your temporary email is: {temp_email}\n"
                                "You can now receive messages on this email. I'll notify you when an email arrives.")
        else:
            await message.reply("No available domains for temporary email. Try again later.")
    else:
        await message.reply("Failed to generate a temporary email. Please try again later.")

# Command to check for new emails
@Client.on_message(filters.command("checkemail"))
async def check_email(client: Client, message: Message):
    user_id = message.from_user.id
    
    if user_id not in user_emails:
        await message.reply("You haven't generated a temporary email yet. Use /generate_email first.")
        return
    
    temp_email = user_emails[user_id]
    
    # Check inbox for the temporary email
    url = f"https://{TEMP_MAIL_API_HOST}/request/mail/id/{temp_email}"
    
    headers = {
        "x-rapidapi-key": TEMP_MAIL_API_KEY,
        "x-rapidapi-host": TEMP_MAIL_API_HOST
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        emails = response.json()
        
        if emails:
            for email in emails:
                from_address = email.get("from", "Unknown Sender")
                subject = email.get("subject", "No Subject")
                body = email.get("body", "No Body")
                
                await message.reply(f"📧 New email received\n"
                                    f"From: {from_address}\n"
                                    f"Subject: {subject}\n"
                                    f"Body:\n{body}")
        else:
            await message.reply("No new emails.")
    else:
        await message.reply("Failed to fetch emails. Please try again later.")

# Periodic email check function (you can set this up as a scheduled job if required)
async def check_inbox_periodically():
    while True:
        for user_id, temp_email in user_emails.items():
            # Similar email checking logic here
            url = f"https://{TEMP_MAIL_API_HOST}/request/mail/id/{temp_email}"
            headers = {
                "x-rapidapi-key": TEMP_MAIL_API_KEY,
                "x-rapidapi-host": TEMP_MAIL_API_HOST
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                emails = response.json()
                
                if emails:
                    for email in emails:
                        from_address = email.get("from", "Unknown Sender")
