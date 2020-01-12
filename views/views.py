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
    data = ThemeBD.objects.in_bulk()
    lent = len(data)
    print(data[lent].Theme)
    context['flag'] = (data[lent].Theme)
    # context['optNum'] = len(context['options'])

    if request.method == 'POST':
        single_vote(request)

        f = ThemeForm(request.POST)
        if f.is_valid():
            flag = bool(request.POST.get('flag'))
            # Сохранение данных
            item = ThemeBD(Theme= flag)
            item.save()
            # Формирование ответа
            context['flag'] = flag
            context['form'] = f
        else:
            context['form'] = f
    else:
        context['nothing_entered'] = True
        context['form'] = ThemeForm()

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
    data = ThemeBD.objects.in_bulk()
    lent = len(data)
    print(data[lent].Theme)
    context['flag'] = (data[lent].Theme)
    if request.method == 'GET':
        context['form'] = CreateVoting()

    if request.method == 'POST':

        f = ThemeForm(request.POST)
        if f.is_valid():
            flag = bool(request.POST.get('flag'))
            # Сохранение данных
            item = ThemeBD(Theme=flag)
            item.save()
            # Формирование ответа
            context['flag'] = flag
            context['form'] = f
        else:
            context['form'] = f

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
    else:
        context['nothing_entered'] = True
        context['form'] = ThemeForm()

    return render(request, 'creation.html', context)
