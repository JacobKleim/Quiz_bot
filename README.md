# Quiz_bot

This bot allows you to take a quiz in vk bot and tg bot. interactive keyboard is used for interaction. the code contains a script to     extract the question-answer from a text file and convert it to a jason format file.

## Environment variables
  Create a .env file with parameters:
   ```
   TELEGRAM_BOT_TOKEN=your secret token
   ```

## Environment      
  Сreate and activate a virtual environment
   ```
   python -m venv venv
   ```
   ```bash
   source venv/Scripts/activate
   ```

## Requirements
  Install dependencies:
   ```
   python -m pip install --upgrade pip
   ```
   ```
   pip install -r requirements.txt
   ```

## Run
   ```
   python tg_bot.py
   ```
   ```
   python vk_bot.py
   ```