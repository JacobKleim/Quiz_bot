import json
import logging
import os
from random import choice

import redis
import vk_api as vk
from dotenv import load_dotenv
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id


logger = logging.getLogger('VK_BOT')


def load_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


quiz_file_path = "quiz.json"
quiz = load_from_json(quiz_file_path)


def main() -> None:

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

    vk_group_token = os.environ['VK_GROUP_TOKEN']

    logger.info('Bot started')
    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)

    keyboard.add_line()
    keyboard.add_button('Сдаться', color=VkKeyboardColor.POSITIVE)

    keyboard.add_line()
    keyboard.add_button('Мой счет', color=VkKeyboardColor.NEGATIVE)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id

            if event.text == 'Новый вопрос':
                question = choice(list(quiz.keys()))
                redis_db.set(user_id, question)
                answer = quiz.get(question)
                correct_answer = answer.split(
                    '.')[0].split('(')[0].strip().lower()

                vk_api.messages.send(
                    user_id=user_id,
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard(),
                    message=f'Вопрос: {question}'
                )

            elif event.text == 'Сдаться':
                question = redis_db.get(user_id)
                answer = quiz.get(question, 'Неизвестный вопрос.')
                vk_api.messages.send(
                    user_id=user_id,
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard(),
                    message=f'Ответ: {answer}'
                )
            else:
                question = redis_db.get(user_id)
                if question:
                    answer = quiz.get(question)

                    correct_answer = answer.split(
                        '.')[0].split('(')[0].strip().lower()

                    user_answer = event.text.strip().lower()

                    if user_answer == correct_answer:
                        vk_api.messages.send(
                            user_id=user_id,
                            random_id=get_random_id(),
                            keyboard=keyboard.get_keyboard(),
                            message='Правильно! Поздравляю!'
                            'Для следующего вопроса нажми «Новый вопрос»'
                        )
                    else:
                        vk_api.messages.send(
                            user_id=user_id,
                            random_id=get_random_id(),
                            keyboard=keyboard.get_keyboard(),
                            message='Неправильно… Попробуешь ещё раз?'
                        )


if __name__ == '__main__':
    main()
