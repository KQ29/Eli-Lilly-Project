import os
import json
from django.conf import settings
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def medicines(request):
    # 1) Construct the path to medicines.json
    #    e.g. "my_app/data/medicines.json" inside your BASE_DIR
    json_path = os.path.join(settings.BASE_DIR, 'myapp', 'data', 'medicines.json')
    # Adjust 'my_app' to your actual app name, if different

    # 2) Read/parse the JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Example JSON structure: {"medicines": [...]}
    # We'll extract the list of medicines
    medicines_list = data.get('medicines', [])

    # 3) Pass the list to the template
    context = {
        'medicines_list': medicines_list
    }
    return render(request, 'medicines.html', context)
