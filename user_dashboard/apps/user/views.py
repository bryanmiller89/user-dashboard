from django.shortcuts import render, redirect
from django.contrib import messages
from .models import * 
# Create your views here.
def index(request):
    return render(request, 'user/index.html')

def register(request):
    # Invoking the register method that we defined in the PersonManager
    result = Person.objects.register(request.POST)
    if 'errors' in result:
        for i in result['errors']:
            messages.error(request, i)
        return redirect('/')
    else:
        messages.success(request, 'You registered someone! yay')
        return redirect('/')

def login(request):

    login = Person.objects.login(request.POST)
    if login['result'] == 'success':
        request.session['user_id'] = login['user'].id 
        messages.success(request, 'You logged in!')
    else:
        for err in login['errors']:
            messages.error(request, err)

    return redirect('/')

def show(request, user_id):
    user = Person.objects.get(id = user_id)
    # messages = Message.objects.filter(reciever = )
    context = {
        'user': user
    }
    return render(request, 'user/profile.html', context)

def message(request, receiver_id):
    message = Message.objects.post_message(request.POST, receiver_id, request.session['user_id'])
    return redirect("/user/{}".format(receiver_id))

def comment(request, message_id, receiver_id):
    comment = Comment.objects.post_comment(request.POST, message_id, request.session['user_id'])
    return redirect("/user/{}".format(receiver_id))