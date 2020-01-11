from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect, reverse
import datetime
from .models import *
from .forms import *


def index(request):
    context = dict()

    context['votings'] = Voting.objects.all()
    context['len'] = len(context['votings'])
    ids = dict()
    # context['optNum'] = len(context['options'])

    for vote in context['votings']:
        li = vote.options()
        ids['v' + str(vote.id) + '_min'] = li[0].id
        ids['v' + str(vote.id) + '_max'] = li[len(li) - 1].id
    context['ids'] = ids

    if request.method == 'POST':
        option_id = request.POST.getlist('answer')  # getlist - функция , которая возвращяет list всех answer
        voting_id = request.POST.get('voting_id')
        if not (Vote.objects.filter(user=request.user,
                                    voting=Voting.objects.get(
                                        id=voting_id)).exists()):  # Проверка голосовал ли пользователь в этом голосовании или нет
            for i in range(len(option_id)):  # добавление всех ответов
                if request.user.is_authenticated:
                    vote1 = Vote(option=Option.objects.get(id=option_id[i]),
                                 user=request.user,
                                 voting=Voting.objects.get(id=voting_id))
                    vote1.save()
                else:
                    return HttpResponse('Сперва войди!')
        else:
            return HttpResponse('Вы уже голосовали')  # красиво оформить вывод
    return render(request, 'index.html', context)


def vote(request, option_id):  # никак не используется !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    context = {}
    context['voting'] = Voting.objects.get(id=option_id)  # добавление вопроса по его id
    context['options'] = Option.objects.filter(voting_id=option_id)  # добавление всех его вариантов ответа
    context['option_id'] = option_id  # номер вопроса
    # обработка
    if request.method == 'POST':
        option_id = request.POST.getlist('answer')  # getlist - функция , которая возвращяет list всех answer
        for i in range(len(option_id)):  # добавление всех отвтов
            if request.user.is_authenticated:
                vote1 = Vote(option=Option.objects.get(id=option_id[i]), user=request.user)
                vote1.save()
            else:
                return HttpResponse('Сперва войди!')
    return render(request, 'vote.html', context)


def create(request):
    context = {}
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
            return HttpResponse('Сперва войди!')

    return render(request, 'creation.html', context)
