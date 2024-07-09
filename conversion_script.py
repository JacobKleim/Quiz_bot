import json
import os

import argparse


def get_question_answer(file_path):
    question_answer = {}

    with open(file_path, "r", encoding='KOI8-R') as file:
        file_content = file.read()

    parsed_file_content = file_content.split('\n\n\n')

    for content in parsed_file_content:
        if 'Вопрос' in content and 'Ответ' in content:
            splited_question = content.split('Вопрос')
            if len(splited_question) > 1:
                question_content = splited_question[1].split('Ответ:')[0]
                question_parts = question_content.split(':', 1)
                if len(question_parts) > 1:
                    question = question_parts[1].strip()
                else:
                    continue

            splited_answer = content.split('Ответ:')
            if len(splited_answer) > 1:
                answer = splited_answer[1].split(
                    'Автор:')[0].split('Источник')[0].strip()
            else:
                continue

            question_answer[question] = answer

    return question_answer


def save_quiz_to_json(quiz, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(quiz, file, ensure_ascii=False, indent=4)


def load_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def main() -> None:

    parser = argparse.ArgumentParser(
        description='A script to extract questions and answers from text files'
                    'and save them in JSON format.')
    parser.add_argument('-f', '--folder_path', default='files',
                        help='Path to folder with .txt files')
    args = parser.parse_args()

    quiz = {}

    folder_path = args.folder_path

    files = os.listdir(folder_path)

    for file in files:
        file_path = os.path.join(folder_path, file)
        question_answer = get_question_answer(file_path)
        quiz.update(question_answer)

    converted_file_path = 'quiz.json'
    save_quiz_to_json(quiz, converted_file_path)

    print(f"Вопросы и ответы записаны в файл {converted_file_path}")


if __name__ == '__main__':
    main()
