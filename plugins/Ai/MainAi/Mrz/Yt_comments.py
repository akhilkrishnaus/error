import re
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from googleapiclient.discovery import build

# YouTube API Key
YOUTUBE_API_KEY = "AIzaSyCBARPV7-YwVs1EtAjabk10zBXf70kHv9Q"
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Function to extract video ID from YouTube URL
def extract_video_id(url):
    patterns = [
        r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)",   # Normal YouTube URL
        r"(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]+)",              # Shortened YouTube URL
        r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([a-zA-Z0-9_-]+)",    # YouTube Shorts
        r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]+)"      # Embed URL
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# Function to get YouTube video comments along with user details
def get_video_comments(video_id):
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100
        )
        response = request.execute()

        while request is not None and len(comments) < 5000:  # Limit to 5000 comments
            # Collect comments and user details
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                comment_info = {"author": author, "comment": comment}
                comments.append(comment_info)

            # Pagination for more comments if available
            if "nextPageToken" in response and len(comments) < 5000:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100,
                    pageToken=response["nextPageToken"]
                )
                response = request.execute()
            else:
                request = None
                
        return comments[:5000]  # Return only up to 5000 comments
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to get video statistics like total likes
def get_video_statistics(video_id):
    try:
        video_response = youtube.videos().list(
            part="statistics",
            id=video_id
        ).execute()

        if video_response and "items" in video_response and video_response["items"]:
            video_stats = video_response["items"][0]["statistics"]
            likes = video_stats.get("likeCount", "0")
            return {"likes": likes}
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Pyrogram command to pick comments
@Client.on_message(filters.command("pickcomments"))
async def pickcomments(client, message):
    try:
        # Check if a URL was provided
        if len(message.text.split()) < 2:
            await message.reply("Please provide a valid YouTube link.")
            return

        video_url = message.text.split(' ')[1]  # Get YouTube URL from command

        # Extract video ID
        video_id = extract_video_id(video_url)
        if not video_id:
            await message.reply("Invalid YouTube link. Please provide a correct URL.")
            return

        # Fetch comments from the YouTube video
        comments = get_video_comments(video_id)
        if not comments:
            await message.reply("No comments found on this video.")
            return
        
        # Fetch video statistics
        video_stats = get_video_statistics(video_id)
        likes = video_stats["likes"] if video_stats else "N/A"

        # Display total comments and total likes
        await message.reply(f"Total comments loaded: {len(comments)}\nTotal likes: {likes}", 
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("Pick Winner 🎊", callback_data=f"pickwinner_{video_id}")]]
                            ))

    except Exception as e:
        await message.reply(f"An error occurred: {e}")

# Callback function to pick a random winner and show user details
@Client.on_callback_query(filters.regex(r"pickwinner_"))
async def pick_winner(client, callback_query):
    try:
        video_id = callback_query.data.split("_")[1]

        # Fetch comments again with user details
        comments = get_video_comments(video_id)
        
        if not comments:
            await callback_query.message.edit_text("No comments found on this video.")
            return
        
        # Select a random winner
        winner = random.choice(comments)
        winner_author = winner["author"]
        winner_comment = winner["comment"]
        
        # Send winner message with 🎊 reaction
        await callback_query.message.edit_text(
            f"The winner is:\n\n🎊 **{winner_author}** 🎊\n\nComment:\n\"{winner_comment}\"",
        )

    except Exception as e:
        await callback_query.message.edit_text(f"An error occurred: {e}")
