from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'question': 'What is the most widely used Python framework?',
        'option1': 'Django',
        'option2': 'Flask',
        'option3': 'Pyramid',
    }
    return render(request, 'home/index.html', context)