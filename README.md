# Quiz Bot Documentation

This is a Telegram quiz bot that tests users' knowledge of Python programming with 10 questions.

## Bot Commands

- `/start` - Starts the bot and shows the main menu with "Start Game" and "Statistics" buttons
- `/quiz` - Starts a new quiz session
- `/stats` - Shows statistics of all players who have completed the quiz
- Button: "Начать игру" - Starts a new quiz session
- Button: "Статистика" - Shows statistics of all players

## Features

- 10 multiple-choice questions about Python programming
- Tracks user answers and displays them after each response
- Saves the last quiz result for each user
- Shows correct/incorrect answers immediately
- Displays final score at the end of the quiz
- Maintains statistics of all players' scores
- Removes answer buttons after selection to prevent multiple submissions
- Stores quiz progress and answers in a SQLite database

## How to Use

1. Start the bot with `/start`
2. Click "Начать игру" or use `/quiz` to begin the quiz
3. Select an answer from the provided options
4. Receive immediate feedback on your answer
5. View your final score after completing all 10 questions
6. Check overall statistics with `/stats` or the "Статистика" button

## Technical Details

- Built using Python and aiogram library
- Uses SQLite for persistent storage
- Modular structure with separate files for:
  - Main bot logic (main.py)
  - Quiz questions (quiz_data.py)
  - Database operations (database.py)
  - Message handlers (handlers.py)
- Stores user progress, scores, and answer history

## Running the Bot Locally

1. Clone the repository or copy the files to a directory
2. Install dependencies: `pip install aiogram aiosqlite python-dotenv`
3. Create a `.env` file with your bot token:
   ```
   BOT_TOKEN=your_bot_token_here
   ```
4. Run the bot: `python main.py`

## Running the Bot with Docker

1. Ensure Docker is installed on your system
2. Create a `.env` file with your bot token:
   ```
   BOT_TOKEN=your_bot_token_here
   ```
3. Build the Docker image:
   ```
   docker build -t quiz-bot .
   ```
4. Run the Docker container:
   ```
   docker run --env-file .env -v $(pwd)/quiz_bot.db:/app/quiz_bot.db quiz-bot
   ```
   Note: The `-v` flag persists the SQLite database between container runs. Ensure the `quiz_bot.db` file is in your current directory or adjust the path accordingly.

## Development

- The bot uses a SQLite database (`quiz_bot.db`) for persistent storage
- Add new questions to `quiz_data.py`
- Modify handlers in `handlers.py` for additional functionality
- Update database schema in `database.py` if needed