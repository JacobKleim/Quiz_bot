# Quiz_bot

This bot allows you to take a quiz in vk bot and tg bot. interactive keyboard is used for interaction. the code contains a script to     extract the question-answer from a text file and convert it to a jason format file.

## Redis configuration

The bot uses [Redis](https://redis.io/) to store state and progress information about the test execution for each user. Redis is an in-memory data structure store used as a distributed key-value database, cache, and message broker. To use [Redis](https://redis.io/), you need to register and retrieve your database data.


## conversion_script.py script
This script is designed to extract questions and answers from text files and save them in JSON format. It can be useful for creating quizzes, questionnaires or a knowledge base. Below are instructions on how to use the script.

Text files should have the following structure:
  ```
  Question: What color is the sky?
  Answer: Blue
  Author: Unknown
  Source: Folk Observations
  ```
Arguments:
  -f, --folder_path: The path to the folder containing text files. The files folder is used by default.

### Run script:
  ```
  python conversion_script.py -f /path/to/folder
  ```

## Links to bots(example)
  ```
  https://t.me/assistant_peoples_bot
  ```
  ```
  https://vk.com/invite/Z4uEmZX
  ```


## Environment variables
  Create a .env file with parameters:
   ```
   TELEGRAM_BOT_TOKEN=secret token
   ```
   ```
   VK_GROUP_TOKEN=secret token
   ```
   ```
   REDIS_HOST=db host
   ```
   ```
   REDIS_PORT=db port
   ```
   ```
   REDIS_PASSWORD=db password
   ```
   ```
   REDIS_DB=db number
   ```

## Environment      
  Сreate and activate a virtual environment
   ```
   python -m venv venv
   ```
   For Windows:
   ```bash
   source venv/Scripts/activate
   ```
   For Linux:
   ```bash
   source venv/bin/activate
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