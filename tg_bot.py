import logging
import os
import time
from random import choice

import redis
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)

from conversion_script import load_from_json


logger = logging.getLogger('TG_BOT')


NEW_QUESTION, ANSWER, MY_SCORE = range(3)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user

    custom_keyboard = [['Новый вопрос', 'Сдаться', 'Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)

    update.message.reply_markdown_v2(
        fr'Привет {user.mention_markdown_v2()}\! Я бот для викторин\!',
        reply_markup=reply_markup
    )

    return NEW_QUESTION


def handle_new_question_request(update: Update,
                                context: CallbackContext,
                                redis_db,
                                quiz) -> None:

    question = choice(list(quiz.keys()))
    chat_id = update.effective_chat.id
    redis_db.set(chat_id, question)

    context.bot.send_message(chat_id=chat_id,
                             text=f"Вопрос: {question}")

    return ANSWER


def handle_solution_attempt(update: Update,
                            context: CallbackContext,
                            redis_db,
                            quiz) -> None:

    text = update.message.text
    chat_id = update.effective_chat.id
    question = redis_db.get(chat_id)
    answer = quiz.get(question)

    correct_answer = answer.split('.')[0].split('(')[0].strip().lower()
    user_answer = text.strip().lower()

    if user_answer == correct_answer:
        context.bot.send_message(
            chat_id=chat_id,
            text='Правильно! Поздравляю!'
            'Для следующего вопроса нажми «Новый вопрос»')

        return NEW_QUESTION

    elif text == 'Новый вопрос':
        return handle_new_question_request(update, context, redis_db)

    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="Неправильно… Попробуешь ещё раз?")

        return ANSWER


def handle_surrender(update: Update,
                     context: CallbackContext,
                     redis_db,
                     quiz) -> int:

    chat_id = update.effective_chat.id
    question = redis_db.get(chat_id)
    answer = quiz.get(question)

    context.bot.send_message(chat_id=chat_id, text=f"Ответ: {answer}")

    return handle_new_question_request(update, context, redis_db)


def cancel(update: Update, context: CallbackContext,):
    update.message.reply_text('Диалог завершён. Если хотите начать сначала,'
                              'нажмите /start.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    load_dotenv()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    redis_host = os.environ['REDIS_HOST']
    redis_port = os.environ['REDIS_PORT']
    redis_password = os.environ['REDIS_PASSWORD']
    redis_db = os.environ['REDIS_DB']

    redis_db = redis.Redis(host=redis_host, port=redis_port,
                           password=redis_password, db=redis_db,
                           decode_responses=True)

    bot_token = os.environ['TELEGRAM_BOT_TOKEN']

    quiz_file_path = "quiz.json"
    quiz = load_from_json(quiz_file_path)

    while True:
        try:
            updater = Updater(bot_token)

            dispatcher = updater.dispatcher

            conv_handler = ConversationHandler(

                entry_points=[CommandHandler('start', start)],

                states={
                    NEW_QUESTION: [
                        MessageHandler(Filters.regex('^(Новый вопрос)$'),
                                       lambda update,
                                       context:
                                       handle_new_question_request(
                                            update,
                                            context,
                                            redis_db,
                                            quiz)),
                        ],
                    ANSWER: [
                        MessageHandler(Filters.regex('^(Сдаться)$'),
                                       lambda update,
                                       context:
                                       handle_surrender(
                                            update,
                                            context,
                                            redis_db,
                                            quiz)),
                        MessageHandler(Filters.text & ~Filters.command,
                                       lambda update,
                                       context:
                                       handle_solution_attempt(
                                            update,
                                            context,
                                            redis_db,
                                            quiz)),
                    ],
                },

                fallbacks=[CommandHandler('cancel', cancel)]
            )

            dispatcher.add_handler(conv_handler)

            updater.start_polling()

            updater.idle()

        except Exception as e:
            logger.error(f'ERROR {e}')
            time.sleep(10)


if __name__ == '__main__':
    main()
