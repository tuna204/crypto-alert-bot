import asyncio
import aiohttp
from telegram import Bot

# --- Configuration ---
BOT_TOKEN = "7893461428:AAFLhyyKn1WpXvFzsKAhp28oXZZmNW_gnJQ"
CHAT_ID = 1219995305  # Replace with your Telegram user ID
TARGET_PRICE = 0.12
CHECK_INTERVAL = 60  # in seconds
COIN_ID = "dogecoin"

bot = Bot(token=BOT_TOKEN)

async def get_current_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
                return data[coin_id]["usd"]
    except Exception as e:
        print("Error getting price:", e)
        return None

async def send_alert(price):
    message = f"🚨 {COIN_ID.upper()} hit ${price} USD!\nTarget was ${TARGET_PRICE}."
    await bot.send_message(chat_id=CHAT_ID, text=message)

async def main():
    print(f"📈 Tracking {COIN_ID.upper()}... Target: ${TARGET_PRICE}")
    while True:
        price = await get_current_price(COIN_ID)
        if price is not None:
            print(f"Current price: ${price}")
            if price <= TARGET_PRICE:
                await send_alert(price)
                break
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
