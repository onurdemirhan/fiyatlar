#     bot = telegram.Bot("5635065917:AAH3Bx2UCVOCwoCrvvdDwLsHiRdy1pz3bvo")
import asyncio
import telegram


# async def main():
#     bot = telegram.Bot("5635065917:AAH3Bx2UCVOCwoCrvvdDwLsHiRdy1pz3bvo")
#     async with bot:
#         print(await bot.get_me())


# async def main():
#     bot = telegram.Bot("5635065917:AAH3Bx2UCVOCwoCrvvdDwLsHiRdy1pz3bvo")
#     async with bot:
#         print((await bot.get_updates())[0])

async def main():
    bot = telegram.Bot("5635065917:AAH3Bx2UCVOCwoCrvvdDwLsHiRdy1pz3bvo")
    async with bot:
        await bot.send_message(text='Hi Onur!', chat_id=531598315)


if __name__ == '__main__':
    asyncio.run(main())