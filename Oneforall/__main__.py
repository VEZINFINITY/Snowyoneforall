import asyncio
import importlib

from pyrogram import idle, filters, Client
from pyrogram.types import Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS, OPENAI_API_KEY
from Oneforall import LOGGER, app, userbot
from Oneforall.core.call import Hotty
from Oneforall.misc import sudo
from Oneforall.plugins import ALL_MODULES
from Oneforall.utils.database import get_banned_users, get_gbanned

# In-memory toggle store
CHATBOT_USERS = set()
MUSICCLONE_USERS = set()

# GPT chat
import openai
openai.api_key = OPENAI_API_KEY

CLONED_BOTS = []

@app.on_message(filters.command("chatbot") & filters.user(config.SUDO_USERS))
async def toggle_chatbot(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /chatbot on or off")
    arg = message.command[1].lower()
    user_id = message.from_user.id
    if arg == "on":
        CHATBOT_USERS.add(user_id)
        MUSICCLONE_USERS.discard(user_id)
        await message.reply("🤖 Chatbot enabled.")
    elif arg == "off":
        CHATBOT_USERS.discard(user_id)
        await message.reply("🛑 Chatbot disabled.")


@app.on_message(filters.command("musicclone") & filters.user(config.SUDO_USERS))
async def toggle_musicclone(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /musicclone on or off")
    arg = message.command[1].lower()
    user_id = message.from_user.id
    if arg == "on":
        MUSICCLONE_USERS.add(user_id)
        CHATBOT_USERS.discard(user_id)
        await message.reply("🎵 Music clone mode enabled.")
    elif arg == "off":
        MUSICCLONE_USERS.discard(user_id)
        await message.reply("🔇 Music clone mode disabled.")


@app.on_message(filters.private & ~filters.command(["chatbot", "musicclone", "clone"]))
async def chatbot_reply(_, message: Message):
    user_id = message.from_user.id
    if user_id in CHATBOT_USERS:
        try:
            await message.reply_chat_action("typing")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": message.text},
                ]
            )
            await message.reply(response.choices[0].message.content)
        except Exception as e:
            await message.reply("Error: " + str(e))
    elif user_id in MUSICCLONE_USERS:
        await message.reply_chat_action("typing")
        await asyncio.sleep(1.5)
        await message.reply("✅ Done! [Simulated Music Bot Response]")


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
