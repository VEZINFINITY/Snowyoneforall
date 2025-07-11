import time

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from config import BANNED_USERS
from Oneforall import app
from Oneforall.misc import _boot_
from Oneforall.plugins.sudo.sudoers import sudoers_list
from Oneforall.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from Oneforall.utils.decorators.language import LanguageStart
from Oneforall.utils.formatters import get_readable_time
from Oneforall.utils.inline import help_pannel, private_panel, start_panel
from strings import get_string
from Oneforall.misc import SUDOERS

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    await message.react("❤")
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            await message.reply_sticker(
                    "CAACAgUAAx0CYlaJawABBy4vZaieO6T-Ayg3mD-JP-f0yxJngIkAAv0JAALVS_FWQY7kbQSaI-geBA"
             )
            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
    else:
        out = private_panel(_)
        await message.reply_sticker(
            "CAACAgUAAyEFAASOVshSAAIsmWdpHh2gKv710eialDAePRGVS03fAAJEDwACHPRIV-Jt5CoTZx1QNgQ"
        )
        await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=_["start_2"].format(message.from_user.mention, app.mention),
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)

welcome_group = 2

@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(client, message: Message):
    try:
        chat_id = message.chat.id
        for member in message.new_chat_members:
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=member.first_name,  
                            user_id=member.id        
                        )
                    ]
                ]
            )

            if isinstance(config.OWNER_ID, int): 
                if member.id == config.OWNER_ID:
                    owner = f"#BOT_OWNER\n\n 𝙎𝙩𝙖𝙮 𝘼𝙡𝙚𝙧𝙩 ⚠️\n\n{member.mention} 𝙊𝙬𝙣𝙚𝙧 𝗢𝗳 {app.mention} 𝙟𝙪𝙨𝙩 𝙟𝙤𝙞𝙣𝙚𝙙 𝙩𝙝𝙚 𝙜𝙧𝙤𝙪𝙥 <code>{message.chat.title}</code>.\n\n𝗦𝘂𝗽𝗽𝗼𝗿𝘁 𝗠𝗲 𝗛𝗲𝗿𝗲 👇🏻🤭💕\n\n┏━━━━━━━━━━━━┓\n┣★ 𝗨𝗽𝗱𝗮𝘁𝗲 -: @Buyer_infinity \n┣★ 𝗨𝗽𝗱𝗮𝘁𝗲 -: @Destiny_Infinity_Og \n┣★ 𝗦𝘂𝗽𝗽𝗼𝗿𝘁 -: @Bots_Are_Alive \n┣★ 𝗕𝗼𝘁 𝗨𝘀𝗲𝗿𝗡𝗮𝗺𝗲 -: @{app.username}\n┣★ 𝗦𝘂𝗽𝗲𝗿𝗯𝗮𝗻 𝗟𝗼𝗴𝘀 -: @who_cares_qt \n┣★ ᴘᴏꜱɪᴛɪᴠɪᴛʏ ᴋɪ ᴅᴜɴɪʏᴀ -: @positive_thinking135 \n┣★ ᴘᴏꜱɪᴛɪᴠɪᴛʏ ᴋɪ ᴅᴜɴɪʏᴀ 𝗝𝗼𝗶𝗻 𝗛𝗲𝗿𝗲 -:<code>/@Destiny_Infinity_Og  </code>\n┣★ 𝙉𝙤𝙩𝙚  -: 𝗧𝗵𝗶𝘀 𝗜𝘀 𝗢𝗻𝗹𝘆 𝗙𝗼𝗿 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗙𝗼𝗿 𝗠𝘆 𝗢𝘄𝗻𝗲𝗿 {member.mention}."
                    sent_message = await message.reply_text(owner, reply_markup=buttons)
                    await asyncio.sleep(20) 
                    await sent_message.delete()  
                    return

            elif isinstance(config.OWNER_ID, (list, set)): 
                if member.id in config.OWNER_ID:
                    owner = f"#BOT_OWNER\n\n 𝙎𝙩𝙖𝙮 𝘼𝙡𝙚𝙧𝙩 ⚠️\n\n{member.mention} 𝙊𝙬𝙣𝙚𝙧 𝗢𝗳 {app.mention} 𝙟𝙪𝙨𝙩 𝙟𝙤𝙞𝙣𝙚𝙙 𝙩𝙝𝙚 𝙜𝙧𝙤𝙪𝙥 <code>{message.chat.title}</code>.\n\n𝗦𝘂𝗽𝗽𝗼𝗿𝘁 𝗠𝗲 𝗛𝗲𝗿𝗲 👇🏻🤭💕\n\n┏━━━━━━━━━━━━┓\n┣★ 𝗨𝗽𝗱𝗮𝘁𝗲 -: @Buyer_infinity  \n┣★ 𝗨𝗽𝗱𝗮𝘁𝗲 -: @@Destiny_Infinity_Og \n┣★ 𝗦𝘂𝗽𝗽𝗼𝗿𝘁 -: @Bots_Are_Alive \n┣★ 𝗕𝗼𝘁 𝗨𝘀𝗲𝗿𝗡𝗮𝗺𝗲 -: @{app.username}\n┣★ 𝗦𝘂𝗽𝗲𝗿𝗯𝗮𝗻 𝗟𝗼𝗴𝘀 -: @@who_cares_qt\n┣★ 𝙒𝙝𝙤 𝙘𝙖𝙧𝙚𝙨 𝙗𝙖𝙗𝙮 -: @positive_thinking135\n┣★ ᴘᴏꜱɪᴛɪᴠɪᴛʏ ᴋɪ ᴅᴜɴɪʏᴀ 𝗝𝗼𝗶𝗻 𝗛𝗲𝗿𝗲 -:<code> </code>\n┣★ 𝙉𝙤𝙩𝙚  -: 𝗧𝗵𝗶𝘀 𝗜𝘀 𝗢𝗻𝗹𝘆 𝗙𝗼𝗿 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗙𝗼𝗿 𝗠𝘆 𝗢𝘄𝗻𝗲𝗿 {member.mention}."
                    sent_message = await message.reply_text(owner, reply_markup=buttons)
                    await asyncio.sleep(60)
                    await sent_message.delete()  
                    return

            if isinstance(SUDOERS, int): 
                if member.id == SUDOERS:
                    AMBOT = f"#Sudo_User\n\n 𝙎𝙩𝙖𝙮 𝘼𝙡𝙚𝙧𝙩 ⚠️\n\n𝗢𝗙 {app.mention} 𝗦𝗨𝗗𝗢 𝗨𝗦𝗘𝗥 {member.mention} just joined the group <code>{message.chat.title}</code>.\n\n𝗦𝘂𝗽𝗽𝗼𝗿𝘁 𝗠𝗲 𝗛𝗲𝗿𝗲 👇🏻🤭💕\n\n┏━━━━━━━━━━━━┓\n┣★ 𝗨𝗽𝗱𝗮𝘁𝗲 -: @Buyer_infinity  \n┣★ 𝗨𝗽𝗱𝗮𝘁𝗲 -: @Destiny_Infinity_Og \n┣★ 𝗦𝘂𝗽𝗽𝗼𝗿𝘁 -: @Bots_Are_Alive \n┣★ 𝗕𝗼𝘁 𝗨𝗦𝗘𝗥𝗡𝗔𝗠𝗘 -: @{app.username}\n┣★ 𝗦𝘂𝗽𝗲𝗿𝗯𝗮𝗻 𝗟𝗼𝗴𝘀 -: @who_cares_qt\n┣★ 𝙒𝙝𝙤 𝙘𝙖𝙧𝙚𝙨 𝙗𝙖𝙗𝙮 -: @positive_thinking135\n┣★ ᴘᴏꜱɪᴛɪᴠɪᴛʏ ᴋɪ ᴅᴜɴɪʏᴀ 𝗝𝗼𝗶𝗻 𝗛𝗲𝗿𝗲 -:<code> </code>."
                    sent_message = await message.reply_text(AMBOT, reply_markup=buttons)
                    await asyncio.sleep(60)
                    await sent_message.delete()  
                    return

            elif isinstance(SUDOERS, (list, set)):
                if member.id in SUDOERS:
                    AMBOT = f"#Sudo_User\n\n 𝙎𝙩𝙖𝙮 𝘼𝙡𝙚𝙧𝙩 ⚠️\n\n𝗢𝗙 {app.mention} 𝗦𝗨𝗗𝗢 𝗨𝗦𝗘𝗥 {member.mention} just joined the group <code>{message.chat.title}</code>.\n\n𝗦𝘂𝗽𝗽𝗼𝗿𝘁 𝗠𝗲 𝗛𝗘𝗥𝗘 👇🏻🤭💕\n\n┏━━━━━━━━━━━━┓\n┣★ 𝗨𝗽𝗱𝗮𝘁𝗲 -: @Destiny_Infinity_Og  \n┣★ 𝗨𝗽𝗱𝗮𝘁𝗲 -:  \n┣★ 𝗦𝘂𝗽𝗽𝗼𝗿𝘁 -: @Bots_Are_Alive \n┣★ 𝗕𝗢𝗧 𝗨𝗦𝗘𝗥𝗡𝗔𝗠𝗘 -: @{app.username}\n┣★ 𝗦𝘂𝗽𝗲𝗿𝗕𝗮𝗻 𝗟𝗢𝗚𝗦 -: A\n┣★ Infinity_bots -: @positive_thinking135\n┣★ 𝗝𝗼𝗶𝗻 𝗛𝗲𝗿𝗲 -:<code></code>."
                    sent_message = await message.reply_text(AMBOT, reply_markup=buttons)
                    await asyncio.sleep(60)
                    await sent_message.delete()  
                    return

        return
    except Exception as e:
        print(f"Error in welcome handler: {e}")
        return
        


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
