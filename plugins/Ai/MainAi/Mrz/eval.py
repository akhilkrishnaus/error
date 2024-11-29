from pyrogram import Client, filters
from pyrogram.errors import MessageTooLong
import sys, os
import traceback
from io import StringIO
from info import ADMINS

@Client.on_message(filters.command("eval") & filters.user(ADMINS))
async def executor(client, message):
    try:
        code = message.text.split(" ", 1)[1]
    except IndexError:
        return await message.reply('Command Incomplete!\nUsage: /eval your_python_code')
    
    # Capture the input code
    formatted_code = code

    # Redirect stdout and stderr to capture output
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    
    try:
        await aexec(code, client, message)
    except Exception:
        exc = traceback.format_exc()
    
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    # Format the output based on the result of execution
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success!"

    # Format the output for reply in HTML
    formatted_output = f"𝗘𝗩𝗔𝗟:\n\n𝗜𝗡𝗣𝗨𝗧:```python\n<code>{formatted_code}</code>\n\n```𝗢𝗨𝗧𝗣𝗨𝗧:```\n<code>{evaluation}</code>```"

    try:
        await message.reply(formatted_output)
    except MessageTooLong:
        with open('eval.txt', 'w+') as outfile:
            outfile.write(formatted_output)
        await message.reply_document('eval.txt')
        os.remove('eval.txt')

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)
