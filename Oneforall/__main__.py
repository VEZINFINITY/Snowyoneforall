import asyncio
import importlib
import openai

from pyrogram import idle, filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS, OPENAI_API_KEY
from Oneforall import LOGGER, app, userbot
from Oneforall.core.call import Hotty
from Oneforall.misc import sudo
from Oneforall.plugins import ALL_MODULES
from Oneforall.utils.database import get_banned_users, get_gbanned

# GPT API
openai.api_key = OPENAI_API_KEY

# Chat toggles stored per chat ID
CHATBOT_CHATS = set()
MUSICCLONE_CHATS = set()
CLONED_BOTS = []

# Start and Help Commands
@app.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    await message.reply(
        "👋 Welcome! I'm alive.\nUse /help to see commands.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Support", url="https://t.me/YourSupportGroup")]]
        )
    )

@app.on_message(filters.private & filters.command("help"))
async def help_cmd(client, message):
    await message.reply(
        "<u>ᴄʜᴀᴛʙᴏᴛ ᴍᴏᴅᴇ :</u> [ᴡᴏʀᴋs ɪɴ ᴅᴍs & ɢʀᴏᴜᴘs]\n\n"
        "⬤ /chatbot on ➥ ᴇɴᴀʙʟᴇs ᴄʜᴀᴛʙᴏᴛ ʀᴇᴘʟɪᴇs ɪɴ ᴛʜᴇ ᴄʜᴀᴛ.\n"
        "⬤ /chatbot off ➥ ᴅɪsᴀʙʟᴇs ᴄʜᴀᴛʙᴏᴛ ʀᴇᴘʟɪᴇs.\n\n"
        "> ʙᴏᴛ ᴀᴅᴍɪɴ ʀᴇQᴜɪʀᴇᴅ ɪɴ ɢʀᴏᴜᴘꜱ."
    )

# Chatbot Toggle
@app.on_message(filters.command("chatbot") & filters.user(config.SUDO_USERS))
async def toggle_chatbot(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /chatbot on or off")
    arg = message.command[1].lower()
    chat_id = message.chat.id

    if arg == "on":
        CHATBOT_CHATS.add(chat_id)
        MUSICCLONE_CHATS.discard(chat_id)
        await message.reply("🤖 Chatbot enabled here.")
    elif arg == "off":
        CHATBOT_CHATS.discard(chat_id)
        await message.reply("🛑 Chatbot disabled here.")

# MusicClone Toggle
@app.on_message(filters.command("musicclone") & filters.user(config.SUDO_USERS))
async def toggle_musicclone(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /musicclone on or off")
    arg = message.command[1].lower()
    chat_id = message.chat.id

    if arg == "on":
        MUSICCLONE_CHATS.add(chat_id)
        CHATBOT_CHATS.discard(chat_id)
        await message.reply("🎵 Music clone mode enabled.")
    elif arg == "off":
        MUSICCLONE_CHATS.discard(chat_id)
        await message.reply("🔇 Music clone mode disabled.")

# Chatbot / MusicClone reply
@app.on_message(filters.text & (filters.private | filters.group))
async def chatbot_reply(_, message: Message):
    chat_id = message.chat.id
    if chat_id in CHATBOT_CHATS:
        try:
            await message.reply_chat_action("typing")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message.text}]
            )
            await message.reply(response.choices[0].message.content)
        except Exception as e:
            await message.reply("Error: " + str(e))
    elif chat_id in MUSICCLONE_CHATS:
        await message.reply_chat_action("typing")
        await asyncio.sleep(1.5)
        await message.reply("✅ Done! [Simulated Music Bot Response]")

# Clone Bot
@app.on_message(filters.command("clone") & filters.user(config.SUDO_USERS))
async def clone_bot(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /clone <BOT_TOKEN>")
    token = message.command[1]
    try:
        cloned = Client(
            name=f"clone_bot_{len(CLONED_BOTS)+1}",
            bot_token=token
        )
        await cloned.start()

        @cloned.on_message(filters.text & filters.private)
        async def reply_clone(_, msg: Message):
            await msg.reply("🤖 I'm a clone of the main bot!")

        CLONED_BOTS.append(cloned)
        await message.reply("✅ Clone bot started successfully!")
    except Exception as e:
        await message.reply(f"❌ Failed to start clone bot:\n{e}")

# Bot Init
async def init():
    if (
        not config.STRING1 and not config.STRING2 and
        not config.STRING3 and not config.STRING4 and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()

    await sudo()
    try:
        for user_id in await get_gbanned():
            BANNED_USERS.add(user_id)
        for user_id in await get_banned_users():
            BANNED_USERS.add(user_id)
    except:
        pass

    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("Oneforall.plugins." + all_module)
    LOGGER("Oneforall.plugins").info("Successfully Imported Modules...")

    await userbot.start()
    await Hotty.start()
    try:
        await Hotty.stream_call("https://graph.org/file/e999c40cb700e7c684b75.mp4")
    except NoActiveGroupCall:
        LOGGER("Oneforall").error("Start a video chat in your log group/channel. Exiting...")
        exit()
    except:
        pass

    await Hotty.decorators()
    LOGGER("Oneforall").info("Bot is up and running!")
    await idle()

    await app.stop()
    await userbot.stop()
    LOGGER("Oneforall").info("Bot stopped.")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
