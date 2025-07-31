import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import router
from database import create_table
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Bot token
API_TOKEN = os.getenv('BOT_TOKEN')

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Register handlers
dp.include_router(router)

async def main():
    # Create database table
    await create_table()
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())