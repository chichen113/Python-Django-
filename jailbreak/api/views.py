from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CSVUploadForm
from .models import Set, Suite, Test, Task, Question
import pandas as pd
from .masterkey_zeroshot import  MasterKey
import threading
from .hallu_tool import run_single_evaluation, answer_parsing
import concurrent.futures



models = ["gpt-3.5-turbo"]
evaluators = ["gpt-3.5-turbo"]


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            # try:
            set_name = csv_file.name
            set_instance = Set.objects.create(name=set_name, cate='jailbreak')
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


def upload_json(request):
    if request.method == 'POST':
        try:
            # 获取上传的文件
            file = request.FILES.get('file')
            if not file:
                return JsonResponse({'ret': 1, 'msg': '未上传文件'})

            # 读取 JSON 数据
            data = json.load(file)

            # 创建 Set 实例
            set_name = file.name  # 或根据需求设置其他名称
            set_instance = Set.objects.create(name=set_name, cate='hallucination')

            mid = []
            for item in data:
                # 创建 Question 实例
                hallu_instance = Question.objects.create(
                    goal=item.get('question', ''),
                    target=item.get('answer', ''),
                    behavior='',
                    category=item.get('category', ''),
                    methods='hallucination'
                )
                mid.append(hallu_instance.id)

            # 将 Question 实例与 Set 实例关联
            set_instance.relation.add(*mid)

            return JsonResponse({'ret': 0, 'msg': '数据导入成功'})

        except json.JSONDecodeError:
            return JsonResponse({'ret': 1, 'msg': '无效的 JSON 文件'})
        except Exception as e:
            return JsonResponse({'ret': 1, 'msg': str(e)})

    return JsonResponse({'ret': 1, 'msg': '请使用 POST 方法'})

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


def test_suit_create(request):
    example = """
    传入参数如下
    {
        "Suite_name" : "testSuite"
    }
    """
    # todo: 添加名称重复时处理
    if request.method == 'POST':
        params = json.loads(request.body)
        suite_name = params['Suite_name']

        # print(request.body)
        suite_instance = Suite.objects.create(
            name=suite_name,
            state="running"
        )
        return HttpResponse()
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用post方法"
        return response


def test_suit_show(request):
    example = """
    传入参数如下
    {
        "Suite_name" : "TestSuiteShow"
    }
    """
    if request.method == 'GET':
        # print(request.body)
        test_suit_list = list(Suite.objects.values())
        # print(test_suit_list)
        for item in test_suit_list:
            del item["id"]
        ret = {
            "Suite_list": test_suit_list
        }
        return JsonResponse(ret)
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用get方法"
        return response


def test_create(request):
    example = """
    传入参数如下
    {
        "Suite_name" : "testSuite",
        "Test_name" : "Test1",
        "Collection" : "question1.csv",
        "Model" : "gpt-3.5-turbo",
        "Evaluator" : "gpt-3.5-turbo"
        "Cate" : "hallu"
    }
    """
    if request.method == 'POST':
        params = json.loads(request.body)
        suite_name = params['Suite_name']
        test_name = params['Test_name']
        collection = params['Collection']
        model = params['Model']
        evaluator = params['Evaluator']
        suite_instance = Suite.objects.get(name=suite_name)
        collection_instance = Set.objects.get(name=collection)

        # print(request.body)
        test_instance = Test.objects.create(
            name=test_name,
            collection=collection_instance,
            model=model,
            evaluator=evaluator,
            suite=suite_instance
        )
        return HttpResponse()
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用post方法"
        return response


def test_show(request):
    example = """
    传入参数如下
    {
        "Suite_name" : "testSuite"
    }
    """
    if request.method == 'GET':
        # print(request.body)
        params = request.GET
        suite_name = params["Suite_name"]
        test_list = Test.objects.filter(suite__name=suite_name)
        data = []
        for test in test_list:
            mid = dict()
            mid["name"] = test.name
            mid["collection"] = test.collection.name
            mid["model"] = test.model
            mid["evaluator"] = test.evaluator
            data.append(mid)

        ret = { "Test_list": data }
        return JsonResponse(ret)
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用get方法"
        return response


def config(request):
    example = """
    传入参数如下
    {
        "Suite_name" : "TestSuite"
    }
    """
    if request.method == 'GET':
        # print(request.body)
        collection1 = list(Set.objects.filter(cate='jailbreak').values_list("name", flat=True))
        collection2 = list(Set.objects.filter(cate='hallucination').values_list("name", flat=True))
        ret = {
            "Config1": {
                "collection": collection1,
                "model": models,
                "evaluator": evaluators,
                "category": "jailbreak"
            },
            "Config2":
            {
                "collection": collection2,
                "model": models,
                "evaluator": evaluators,
                "category": "hallucination"
            }
        }
        return JsonResponse(ret)
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用get方法"
        return response


def task_create(request):
    example = """
           传入参数如下
           {
               "Suite_name" : "testSuite",
               "Test_name" : "text",
               "Task_name" : "task"
           }
           """
    if request.method == 'POST':
        params = json.loads(request.body)
        suite_name = params['Suite_name']
        test_name = params['Test_name']
        task_name = params['Task_name']
        # print(request.body)
        final = 1
        test_name_instance_list = Test.objects.filter(name=test_name)
        for ins in test_name_instance_list:
            if ins.suite.name == suite_name:
                final = ins
                break
        # 提取对应的 test id 值
        task_instance = Task.objects.create(
            name=task_name,
            escape_rate=0,
            test=final,
        )
        return HttpResponse()
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用post方法"
        return response


def task_show(request):
    example = """
        传入参数如下
        {
            "Suite_name" : "testSuite"
        }
        """
    if request.method == 'GET':
        # print(request.body)
        params = request.GET
        suite_name = params["Suite_name"]
        test_list = Test.objects.filter(suite__name=suite_name)
        data = []
        for test in test_list:
            task_list = Task.objects.filter(test=test)
            for task in task_list:
                mid = dict()
                mid["name"] = task.name
                mid["state"] = task.state
                data.append(mid)

        ret = { "Task_list": data }
        return JsonResponse(ret)
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用get方法"
        return response


def task_info(request):
    example = """
    传入参数如下
    {
        "Task_name" : "task"
    }
    """
    if request.method == 'GET':
        # print(request.body)
        params = request.GET
        task_name = params["Task_name"]
        task = Task.objects.get(name=task_name)
        data = []
        mid = dict()
        mid["state"] = task.state
        mid["escapeRate"] = task.escape_rate
        data.append(mid)

        ret = {"Task_Info": data}
        return JsonResponse(ret)
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用get方法"
        return response


def exe_eva(data):
    # Initialize the MasterKey with the OpenAI API key and model names
    master_key = MasterKey("sk-6ztYKBLUnRd1kViyBelVC5CRrrDwAwzx4AfHdBMozqeD4N5F", execute_model=data["model"],
                           evaluation_model=data["evaluate_model"])
    collection = Set.objects.get(name=data["dataset"])
    related_questions = collection.relation.values()
    res_list = []
    for qs in related_questions:
        mid = dict()
        mid["id"] = qs["id"]
        mid["goal"] = qs["goal"]
        mid["category"] = qs["category"]
        mid["methods"] = qs["methods"]
        res_list.append(mid)
    count = 0
    for index in range(len(res_list)):
        malicious_instruction = res_list[index]["goal"]
        # Execute the jailbreak prompt with the malicious behavior
        jailbreak_executed = master_key.execute_jailbreak_prompt(malicious_instruction)
        res_list[index]["output"] = jailbreak_executed
        # print(f"Jailbreak executed: {jailbreak_executed}")
        # Evaluate the jailbreak prompt
        jailbreak_successful = master_key.evaluate_jailbreak_prompt(malicious_instruction, jailbreak_executed)
        res_list[index]["is_success"] = jailbreak_successful
        if jailbreak_successful:
            count = count + 1
        # print(f"Jailbreak successful: {jailbreak_successful}")
    return res_list, count


def jailbreak_exe(task, test):
    task.state = "running"
    task.save()
    data = {
        'dataset': test.collection.name,
        'model': test.model,
        'evaluate_model': test.model
    }
    res_list, count = exe_eva(data)
    print(f"{task.name}_{test.name}_{test.suite.name} done!")
    ret = {"data": res_list}
    ret_str = json.dumps(ret)
    file_path = f"{task.name}_{test.name}_{test.suite.name}.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(ret_str)
    rate = count / len(res_list)
    task.escape_rate = f"{rate:.2%}"
    task.state = "done"
    task.save()
    return


def hallu_exe(task, test):
    task.state = "running"
    task.save()

    collection = Set.objects.get(name=test.collection.name)
    related_questions = collection.relation.values()
    mid_list = []
    for qs in related_questions:
        mid = dict()
        mid["id"] = qs["id"]
        mid["goal"] = qs["goal"]
        mid["category"] = qs["category"]
        mid["target"] = qs["target"]
        mid["methods"] = qs["methods"]
        mid_list.append(mid)

    output_data = []
    model_name = test.model
    question_data = mid_list
    model_list = [model_name for x in range(len(question_data))]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        ret_list = executor.map(run_single_evaluation, question_data, model_list)
    for item in ret_list:
        output_data.append(item)
    hallucination_count = answer_parsing(output_data)
    print(f"{task.name}_{test.name}_{test.suite.name} done!")

    ret = {"data": output_data}
    ret_str = json.dumps(ret)
    file_path = f"{task.name}_{test.name}_{test.suite.name}.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(ret_str)
    rate = hallucination_count / len(output_data)
    task.escape_rate = f"{rate:.2%}"
    task.state = "done"
    task.save()
    return


def task_exec(request):
    example = """
    传入参数如下
    {
        "Task_name" : "Task1"
    }
    """
    if request.method == 'POST':
        params = json.loads(request.body)
        task_name = params['Task_name']
        # print(request.body)
        task_instance = Task.objects.get(name=task_name)
        if task_instance.state != "starting":
            response = HttpResponse()
            response.status_code = 404
            response.content = "当前任务已运行"
            return response
        test_instance = task_instance.test
        if test_instance.collection.cate == "jailbreak":
            x = threading.Thread(target=jailbreak_exe, args=(task_instance, test_instance))
            x.start()
        else:
            x = threading.Thread(target=hallu_exe, args=(task_instance, test_instance))
            x.start()
        return HttpResponse()
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用post方法"
        return response


def task_res(request):
    example = """
            传入参数如下
            {
                "Task_name" : "task1"
            }
            """
    if request.method == 'GET':
        params = request.GET
        task_name = params["Task_name"]
        task = Task.objects.get(name=task_name)
        test_name = task.test.name
        suite_name = task.test.suite.name
        filename = task_name+'_'+test_name+'_'+suite_name+'.json'
        file_path = f"{filename}"
        content = ' '
        with open(file_path, 'r') as file:
            content =file.read()
        content = json.loads(content)
        return JsonResponse(content)
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用get方法"
        return response


def test_suite_dele(request):
    example = """
        传入参数如下
        {
            "Suite_name" : "testSuiteDelete"
        }
        """
    if request.method == 'POST':
        params = json.loads(request.body)
        suite_name = params['Suite_name']

        # print(request.body)
        suite_instance = Suite.objects.get(
            name=suite_name
        )
        suite_instance.delete()
        return HttpResponse()
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用post方法"
        return response


def test_dele(request):
    example = """
            传入参数如下
            {
                "Test_name" : "testDelete"
            }
            """
    if request.method == 'POST':
        params = json.loads(request.body)
        test_name = params['Test_name']

        # print(request.body)
        test_instance = Test.objects.get(
            name=test_name
        )
        test_instance.delete()
        return HttpResponse()
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用post方法"
        return response


def task_dele(request):
    example = """
            传入参数如下
            {
                "Task_name" : "taskDelete"
            }
            """
    if request.method == 'POST':
        params = json.loads(request.body)
        task_name = params['Task_name']

        # print(request.body)
        task_instance = Task.objects.get(
            name=task_name
        )
        task_instance.delete()
        return HttpResponse()
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用post方法"
        return response
