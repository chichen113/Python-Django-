from llm_test import run_single_evaluation, answer_parsing
import concurrent.futures
import json


def hallu():
    output_data = []
    model_name = "gpt-3.5-turbo"
    question_data = json.load(open(f'all_dataset.json', 'r', encoding='utf-8'))
    model_list = [model_name for x in range(len(question_data))]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        ret_list = executor.map(run_single_evaluation, question_data, model_list)
    for item in ret_list:
        output_data.append(item)
    answer_parsing(output_data)
    with open(f'./res/{model_name}.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)


hallu()