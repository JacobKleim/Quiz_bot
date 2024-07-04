import os


files = os.listdir('files')

quiz = {}


for file in files:
    file_path = os.path.join('files', file)

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
                    print(question)
                else:
                    continue

            answer_split = content.split('Ответ:')
            if len(answer_split) > 1:
                answer = answer_split[1].strip().split('\n', 1)[0]
                print(answer)
            else:
                continue
