from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CSVUploadForm
from .models import Question
from .models import Set
import pandas as pd
from .masterkey_zeroshot import  MasterKey


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            # try:
            set_name = csv_file.name
            set_instance = Set.objects.create(name=set_name)
            df = pd.read_csv(csv_file)
            mid = []
            for index, row in df.iterrows():
                question_instance = Question.objects.create(
                    goal=row['goal'],
                    target=row['target'],
                    behavior=row['behavior'],
                    category=row['category']
                )
                mid.append(question_instance.id)
            set_instance.relation.add(*mid)
            messages.success(request, "CSV file uploaded and data added to database.")
            # except Exception as e:
            #     messages.error(request, f"Error processing CSV file: {e}")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})


def test(request):
    str = "hello,test."
    return HttpResponse(str)


def run_explain(request):
    ret = {
        'data': [
            {
                'dataset': 'datasetname1',
                'model': 'gpt-3.5-turbo',
                'evaluate': 'gpt-3.5-turbo'
            },

            {
                'dataset': 'datasetname2',
                'model': 'gpt-3.5-turbo',
                'evaluate': 'gpt-3.5-turbo'
            }
        ]
    }
    return JsonResponse(ret)

def get_dataset(dataset_name):
    ds = Question.objects.values()
    ds = list(ds)
    dss = []
    for index in ds:
        dss.append(index['goal'])
    return dss




def exe_eva(data):
    # Initialize the MasterKey with the OpenAI API key and model names
    master_key = MasterKey("sk-6ztYKBLUnRd1kViyBelVC5CRrrDwAwzx4AfHdBMozqeD4N5F", execute_model=data["model"],
                           evaluation_model=data["evaluate_model"])
    ret = []
    for problem in get_dataset(data['dataset']):
        malicious_instruction = problem
        mid = {'problem': malicious_instruction}
        # Execute the jailbreak prompt with the malicious behavior
        jailbreak_executed = master_key.execute_jailbreak_prompt(malicious_instruction)
        mid['exe'] = jailbreak_executed
        # print(f"Jailbreak executed: {jailbreak_executed}")
        # Evaluate the jailbreak prompt
        jailbreak_successful = master_key.evaluate_jailbreak_prompt(malicious_instruction, jailbreak_executed)
        mid['success'] = jailbreak_successful
        # print(f"Jailbreak successful: {jailbreak_successful}")
        ret.append(mid)
    return ret


def run(request):
    if request.method == 'POST':
       # print(request.body)
       jstr = json.loads(request.body)
       datalist = jstr['data']
       ret = {'ret': 0, 'data': []}
       for data in datalist:
           ret['data'].append(exe_eva(data))
       return JsonResponse(ret)
    else:
       return JsonResponse({'ret': 1, 'msg': '请使用POST方法'})


def list_question(request):
    questions = Question.objects.values_list("goal", flat=True)
    questions = list(questions)
    ret = {
        'ret': 0,
        'questions': questions
    }
    return JsonResponse(ret)


def add_question(request):
    """
    传入参数如下
    {
    "data":{
        "goal": "问题",
        "target": "预期回复",
        "behavior": "问题简称",
        "category": "类别描述"
        }
    }
    """
    if request.method == 'POST':
        # print(request.body)
        question = json.loads(request.body)["data"]
        question_instance = Question.objects.create(
            goal=question['goal'],
            target=question['target'],
            behavior=question['behavior'],
            category=question['category']
        )
        ret = {
            'ret': 0,
            'id': question_instance.id
        }
        return JsonResponse(ret)
    else:
        return JsonResponse({'ret': 1, 'msg': '请使用POST方法'})


def modify_question(request):
    example = """
    传入参数如下
    {
        "id": 203,
        "data":{
            "goal": "问题1",
            "target": "预期回复1",
            "behavior": "问题简称1",
            "category": "类别描述1"
        }
    }
    """
    if request.method == 'POST':
        params = json.loads(request.body)
        question_id = params['id']
        data = params['data']
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return JsonResponse({
                'ret': 1,
                'msg': f'id 为`{question_id}`的客户不存在'
            })
        if 'goal' in data:
            question.goal = data['goal']
        if 'target' in data:
            question.target = data['target']
        if 'behavior' in data:
            question.behavior = data['behavior']
        if 'category' in data:
            question.category = data['category']

        question.save()
        return JsonResponse({'ret': 0})
    else:
        return JsonResponse({'ret': 1, 'msg': '请使用POST方法\n' + example})


def del_question(request):
    example = """
    传入参数如下
    {
        "id": 203
    }
    """
    if request.method == 'POST':
        params = json.loads(request.body)
        question_id = params['id']

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return JsonResponse({
                'ret': 1,
                'msg': f'id 为`{question_id}`的客户不存在'
            })

        question.delete()

        return JsonResponse({'ret': 0})
    else:
        return JsonResponse({'ret': 1, 'msg': '请使用POST方法\n' + example})


def list_set(request):
    datasets = Set.objects.values()
    datasets = list(datasets)
    ret = {
        'ret': 0,
        'datasets': datasets
    }
    return JsonResponse(ret)
