import itertools

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import *
from .forms import *


def index(request):
    context = dict()
    context['auth'] = request.user.is_authenticated     # нужно для отображения меню
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
    single_vote(request)
    return render(request, 'vote.html', context)

def edit(request, option_id):
    context = dict()
    context['auth'] = request.user.is_authenticated
    if request.method == "POST":
        if request.POST.get("delete"):
            context['need_button'] = False
            context['deleted'] = True
            voting = Voting.objects.get(id=option_id)
            voting.delete()
        if request.POST.get("delete_option"):
            context['need_buttons'] = True
            context['deleted'] = False
            context['mode'] = 2
            context['voting'] = Voting.objects.get(id=option_id)
            context['options'] = Option.objects.filter(voting_id=option_id)
            context['option_id'] = option_id
        if request.POST.get("delete_selected"):
            for i in request.POST:
                if not((i == 'csrfmiddlewaretoken') or (i == 'delete_selected')):
                    id = int(i[7:])
                    option = Option.objects.get(id=id)
                    voting = Voting.objects.get(id=option.voting_id)
                    option.delete()
                    context['deleted'] = False
                    context['deleted_option'] = True
                    if Option.objects.filter(voting_id=voting.id).count() == 0:
                        voting.delete()
                        context['deleted'] = True
                        context['deleted_option'] = False
                    context['need_buttons'] = False
    elif (Voting.objects.filter(id=option_id).count() == 0):
        context['need_buttons'] = False
        context['deleted'] = True
    else:
        context['need_buttons'] = True
        context['deleted'] = False
        context['voting'] = Voting.objects.get(id=option_id)
        context['options'] = Option.objects.filter(voting_id=option_id)
        context['option_id'] = option_id
        context['mode'] = 1
        single_vote(request)
    return render(request, 'edit.html', context)

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
