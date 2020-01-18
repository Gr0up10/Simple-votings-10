import json
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse, redirect
from django.utils.safestring import SafeString

from .forms import *
from .models import *


def index(request):
    context = dict()
    context['auth'] = request.user.is_authenticated  # нужно для отображения меню
    context['votings'] = Voting.objects.all()
    ids = dict()
    # context['optNum'] = len(context['options'])

    if request.method == 'POST':
        single_vote(request)

    if request.method == 'GET':
        for vote in context['votings']:
            li = vote.options()
            ids['v' + str(vote.id) + '_min'] = li[0].id
            ids['v' + str(vote.id) + '_max'] = li[len(li) - 1].id
        context['ids'] = ids
    return render(request, 'index.html', context)


def single_vote(request):
    if request.method == 'POST':
        option_id = request.POST.getlist('answer')  # getlist - функция , которая возвращяет list всех answer
        voting_id = request.POST.get('voting_id')
        if request.user.is_authenticated:
            if not (Vote.objects.filter(user=request.user,
                                        voting=Voting.objects.get(
                                            id=voting_id)).exists()):  # Проверка голосовал ли пользователь в этом голосовании или нет
                for i in range(len(option_id)):  # добавление всех ответов
                    vote1 = Vote(option=Option.objects.get(id=option_id[i]),
                                 user=request.user,
                                 voting=Voting.objects.get(id=voting_id))
                    vote1.save()
            else:
                return HttpResponse('Вы уже голосовали')  # красиво оформить вывод
        else:
            context = dict()
            context['auth'] = request.user.is_authenticated  # нужно для отображения меню
            return render(request, 'Log_in.html', context)


def vote(request, option_id):
    context = dict()
    context['auth'] = request.user.is_authenticated  # нужно для отображения меню
    context['voting'] = Voting.objects.get(id=option_id)  # добавление вопроса по его id
    context['options'] = Option.objects.filter(voting_id=option_id)  # добавление всех его вариантов ответа
    context['option_id'] = option_id  # номер вопроса

    labels = []
    data = []

    for option in context['options']:
        labels.append(option.text)
        data.append(option.vote_count())

    context['labels'] = SafeString(json.dumps(labels))
    context['data'] = SafeString(json.dumps(data))

    single_vote(request)
    return render(request, 'vote.html', context)


def user(request):
    if request.user.is_authenticated:
        context = dict()
        context['auth'] = request.user.is_authenticated  # нужно для отображения меню
        votings = Voting.objects.all()
        context['votings'] = votings
    else:
        return render(request, 'Log_in.html')

    return render(request, 'user.html', context)


def create(request):
    context = dict()
    context['auth'] = request.user.is_authenticated  # нужно для отображения меню
    context['mode'] = 1
    if request.method == 'GET':
        context['form'] = CreateVoting()

    if request.method == 'POST':
        if request.user.is_authenticated:
            main_text = request.POST.get('main_text')
            isCheckbox = bool(request.POST.get('isCheckbox'))
            voting = Voting(question=main_text, author=request.user, isCheckbox=isCheckbox)
            voting.save()
            count = request.POST.get('count')
            if count:
                for i in range(1, int(count) + 1):
                    text = request.POST.get('option' + str(i))
                    option = Option(voting=voting, text=text)
                    option.save()

            tmp = Voting.objects.filter(author=request.user)  # отфильтровка вопросов данного пользователя
            voting_id = tmp[len(tmp) - 1].id  # определение id последнего вопроса
            return redirect(vote, voting_id)  # редирект на voting/voting_id
        else:
            return render(request, 'Log_in.html')

    return render(request, 'creation.html', context)


def register(request):
    context = dict()
    if request.method == 'POST':
        form = RegisterFormView(request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            my_password = form.cleaned_data.get('password1')
            _user = authenticate(username=username, password=my_password)
            if _user.is_active:
                login(request, _user)
                return render(request, 'index.html', context)
        return render(request, 'register.html', context)
    else:
        form = RegisterFormView()
        context['form'] = form
        return render(request, 'register.html', context)


def login_user(request):
    context = dict()
    if request.method == 'POST':
        if 'remind_password' in request.POST:
            subject = 'Hello from Django!'
            message = 'your password is in your mind :p'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['super.plastilinium@gmail.com', ]
            send_mail(subject, message, email_from, recipient_list)
            context['hints'] = '''Письмо с паролем отправлено на вашу почту.'''
    context['form'] = LoginView().form_class()
    return render(request, 'registration/login.html', context)


def send_password(request):
    pass
