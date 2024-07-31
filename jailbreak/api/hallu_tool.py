import time
import json
import concurrent.futures
from openai import OpenAI

def openai_query(input_prompt, model_name):
    client = OpenAI(
        api_key="sk-6JPu7gavjS5l81o3GZffq8SdUbyzGW401tPGKw68i8C8ClFD",
        base_url="https://api.chatanywhere.tech/v1",
    )
    while True:
        try:
            result = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": f"Answer the question with your knowledge and reasoning power."}, {"role": "user", 
                        "content": input_prompt}
                    ], 
                temperature=0, 
                timeout=50,
                max_tokens=500)
            generated_content = result.choices[0].message.content
            print("result ", generated_content)
            break
        except:
            import traceback
            traceback.print_exc()
            print('error; waiting ten seconds and resubmitting')
            time.sleep(3)
    return generated_content


def run_single_evaluation(qa_pairs, model_name):
    question = qa_pairs["goal"]
    input_prompt = f"""
        Now given the question: '{question}', please provide an answer with your knowledge and reasoning power. Think it step by step with a human-like reasoning process. After giving the answer, list the knowledge used in your reasoning process in the form of declarative sentences and point by point. The answer must contains 'Yes, ...' or 'No, ...' or 'I don't know.' at the beginning.
        Here is an example. Question: During Barack Obama took office of the president of USA, were any films directed by James Cameron released?
        Supposed Response: Yes, during Barack Obama's presidency from 2009 to 2017, one film directed by James Cameron was released - Avatar in 2009.
        The key knowledge points used in this reasoning process are:
        1. Barack Obama was the US President from January 20, 2009 to January 20, 2017.
        2. James Cameron is a famous film director known for movies like Titanic, Avatar, Terminator 2, etc.
        3. Cameron's only film release during Obama's presidency was Avatar in 2009. 
    """
    generated_content = openai_query(input_prompt, model_name)
    qa_pairs["output"] = generated_content
    return qa_pairs



def answer_parsing(data):
    correct_count = 0
    refuse_count = 0
    hallucination_count = 0
    # 遍历测试结果文件夹
    for qa_pair in data:
        ground_truth_answer = qa_pair['target']
        llm_answer = qa_pair['output']
        if 'I\'m sorry,' in llm_answer or 'impossible to' in llm_answer or 'As an AI,' in llm_answer or 'not possible to' in llm_answer or 'no direct' in llm_answer or 'I don\'t know' in llm_answer:
            refuse_count += 1
            qa_pair['is_success'] = False
        elif 'Yes.' in ground_truth_answer and ('Yes,' in llm_answer or 'Yes.' in llm_answer):
            correct_count += 1
            qa_pair['is_success'] = True
        elif 'No.' in ground_truth_answer and ('No,' in llm_answer or 'No.' in llm_answer):
            correct_count += 1
            qa_pair['is_success'] = True
        elif 'statement' in qa_pair['goal'] and 'No.' in ground_truth_answer and 'is false' in llm_answer:
            correct_count += 1
            qa_pair['is_success'] = True
        elif 'statement' in qa_pair['goal'] and 'Yes.' in ground_truth_answer and 'is true' in llm_answer:
            correct_count += 1
            qa_pair['is_success'] = True
        elif 'not be' in qa_pair['goal'] and 'not be' in llm_answer:
            correct_count += 1
            qa_pair['is_success'] = True
        else:
            hallucination_count += 1
            qa_pair['is_success'] = False
        return hallucination_count




