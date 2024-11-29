import img2pdf
from pyrogram import Client, filters
from pyrogram.types import Message
import os

# Temporary storage for user images
user_temp = {}

# Help text
help_text = """
*Commands*:

- /pdf:
  For adding images to data for conversion.

- /getpdf:
  After all images are added, use this command to get the PDF file.
  Note: Once you get the PDF file, the previous data will be cleared.
"""

@Client.on_message(filters.command("getpdf"))
async def getimg2pdf(client: Client, message: Message):
    user = message.from_user
    
    # Check if user has added any images
    if user.id not in user_temp or not user_temp[user.id].get('images'):
        return await message.reply_text(
            "🙋 It seems you haven't added any images to convert to PDF. "
            "Please use /pdf to add images."
        )
    
    images = user_temp[user.id]['images']
    
    # Set DPI for the PDF layout
    dpix = 300
    layout_fun = img2pdf.get_fixed_dpi_layout_fun((dpix, dpix))
    file_name = f"user_{user.first_name}.pdf"
    dir_path = os.path.join(os.getcwd(), "pdf_files")
    
    # Create directory if it doesn't exist
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    file_path = os.path.join(dir_path, file_name)
    
    try:
        # Convert images to PDF and send the file
        with open(file_path, "wb") as f:
            f.write(img2pdf.convert(images, layout_fun=layout_fun))
        
        await client.send_document(
            chat_id=message.chat.id,
            document=file_path,
            caption=f"*By {client.me.username} ⚡*",
        )
        
        # Clear user image data after sending the PDF
        del user_temp[user.id]
        
        # Remove the PDF file after sending
        os.remove(file_path)
    
    except Exception as e:
        return await message.reply_text(f"❌ Error: {str(e)}")


@Client.on_message(filters.command("pdf"))
async def img2pdf_handler(client: Client, message: Message):
    reply = message.reply_to_message
    user = message.from_user

    # Check if the user is replying to a photo
    if not reply or not reply.photo:
        return await message.reply_text("Please reply to a photo to add it for PDF conversion.")

    # Initialize user data if not already present
    if user.id not in user_temp:
        user_temp[user.id] = {'images': []}

    # Get the file_id of the largest size of the image
    photo_id = reply.photo.file_id
    
    # Download the image
    try:
        file = await client.download_media(photo_id)
        user_temp[user.id]['images'].append(file)
        images = user_temp[user.id]['images']
        
        await message.reply_text(
            f"⚡ Successfully added image {len(images)} to the list. "
            "Use /img2pdf to add more, and after you're done, use /getimg2pdf to get the PDF file."
        )
    
    except Exception as e:
        return await message.reply_text(f"❌ Error: {str(e)}")
