import json
import os


def get_question_answer(file_path, quiz):

    with open(file_path, "r", encoding='KOI8-R') as my_file:
        file_content = my_file.read()

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

            quiz[question] = answer


def save_quiz_to_json(quiz, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(quiz, file, ensure_ascii=False, indent=4)


def main() -> None:

    quiz = {}

    folder_path = 'files'

    files = os.listdir(folder_path)

    for file in files:
        file_path = os.path.join(folder_path, file)
        get_question_answer(file_path, quiz)

    converted_file_path = 'quiz.json'
    save_quiz_to_json(quiz, converted_file_path)

    print(f"Вопросы и ответы записаны в файл {converted_file_path}")


if __name__ == '__main__':
    main()
