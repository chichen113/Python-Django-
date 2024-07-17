from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CSVUploadForm
from .models import Question
import pandas as pd


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            try:
                df = pd.read_csv(csv_file)
                for index, row in df.iterrows():
                    Question.objects.create(
                        goal=row['goal'],
                        target=row['target'],
                        behavior=row['behavior'],
                        category=row['category']
                    )
                messages.success(request, "CSV file uploaded and data added to database.")
            except Exception as e:
                messages.error(request, f"Error processing CSV file: {e}")
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
