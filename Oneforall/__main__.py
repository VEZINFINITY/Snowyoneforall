import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from Oneforall import LOGGER, app, userbot
from Oneforall.core.call import Hotty
from Oneforall.misc import sudo
from Oneforall.plugins import ALL_MODULES
from Oneforall.utils.database import get_banned_users, get_gbanned

# --- NEW GPT/Chatbot Features --- #
from pyrogram import filters
import openai
from pyrogram.types import Message

# In-memory chatbot toggle (simple, per-user)
chatbot_status = {}

openai.api_key = config.OPENAI_API_KEY

@app.on_message(filters.command("chatbot") & filters.private)
async def toggle_chatbot(client, message: Message):
    user_id = message.from_user.id
    if len(message.command) < 2:
        return await message.reply("Use /chatbot on or /chatbot off")

    mode = message.command[1].lower()
    if mode == "on":
        chatbot_status[user_id] = True
        await message.reply("✅ Chatbot is now ON")
    elif mode == "off":
        chatbot_status[user_id] = False
        await message.reply("❌ Chatbot is now OFF")
    else:
        await message.reply("Invalid option. Use /chatbot on or /chatbot off")

@app.on_message(filters.text & filters.private)
async def gpt_chat(client, message: Message):
    user_id = message.from_user.id
    if not chatbot_status.get(user_id, False):
        return  # Chatbot is off

    try:
        user_input = message.text
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}],
            temperature=0.8,
        )
        reply = response['choices'][0]['message']['content']
        await message.reply(reply)
    except Exception as e:
        await message.reply(f"Error: {e}")

# --- END GPT Feature --- #

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("Oneforall.plugins" + all_module)
    LOGGER("Oneforall.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Hotty.start()
    try:
        await Hotty.stream_call("https://graph.org/file/e999c40cb700e7c684b75.mp4")
    except NoActiveGroupCall:
        LOGGER("Oneforall").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await Hotty.decorators()
    LOGGER("Oneforall ").info(
        "ᴅʀᴏᴘ ʏᴏᴜʀ ɢɪʀʟꜰʀɪᴇɴᴅ'ꜱ ɴᴜᴍʙᴇʀ ᴀᴛ  ᴊᴏɪɴ https://t.me/PiratesMainchat ꜰᴏʀ ᴀɴʏ ɪꜱꜱᴜᴇꜱ"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("Oneforall").info("Stopping One for all Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
