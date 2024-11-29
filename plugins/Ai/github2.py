from pyrogram import Client, filters
import aiohttp
from pyrogram.types import Message

@Client.on_message(filters.command(["infogit"]) & filters.private)
async def github(_, message: Message):
    if len(message.command) < 2:
        p = await message.reply_text("**Usage:**\n /infogit [username]")
        await p.delete(600)
        return

    username = message.text.split(None, 1)[1]
    URL = f"https://api.github.com/users/{username}"
    px = await message.reply_text("🔎 **Searching...**")
    await px.delete()

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(URL) as response:
                response.raise_for_status()
                data = await response.json()

                name = data.get("name", "No Name")
                username = data.get("login", "No Username")
                link = data.get("html_url", "")
                followers = data.get("followers", 0)
                following = data.get("following", 0)
                public_repos = data.get("public_repos", 0)
                avatar_url = data.get("avatar_url", "")
                created_at = data.get("created_at", "").split("T")[0]
                bio = data.get("bio", "No Bio.")

                text = f"""
**GitHub User Info:**

**Name:** [{name}]({link})
**Username:** {username}
**Bio:** {bio}
**Followers:** {followers}
**Following:** {following}
**Public Repos:** {public_repos}
**Account Created:** {created_at}
                """
                await message.reply_photo(photo=avatar_url, caption=text)
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                await message.reply_text("❌ User Not Found.\nPlease Check The Username Correctly.")
            else:
                await message.reply_text("❌ An error occurred while fetching the data.")
        except Exception as e:
            print(str(e))
            await message.reply_text("❌ An unexpected error occurred.")
