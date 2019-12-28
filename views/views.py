from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import *


def index(request):
    context = dict()

    context['votings'] = Voting.objects.all()
    context['votes'] = Vote.objects.all()

    if request.method == 'POST':
        option_id = request.POST.getlist('answer')                           # getlist - функция , которая возвращяет list всех answer

        for i in range(len(option_id)):                                      # добавление всех отвтов
            num = int(Vote.objects.filter(option_id=option_id[i])[0].number)
            num += 1
            Vote.objects.filter(option_id=option_id[i]).update(number=num)


    return render(request, 'index.html', context)


def create(request):
    context = dict()
    context['mode'] = 1
    context['form_for_num'] = NumOfOptions()
    if request.method == 'GET':
        number = request.GET.get('number')
        print(number)
        if number:
            number = int(number)
            if number > 0 and number <11:
                context['mode'] = 2
                context['form'] = CreateVoting()
                context['form_for_num'] = forms.Form

    if request.method == 'POST':
        main_text = request.POST.get('main_text')
        first = request.POST.get('first')
        second = request.POST.get('second')
        isCheckbox = bool(request.POST.get('isCheckbox'))

        voting = Voting(question=main_text, author=1 , isCheckbox = isCheckbox)
        voting.save()

        option1 = Option(voting=voting, text=first)
        option2 = Option(voting=voting, text=second)
        option1.save()
        option2.save()

        vote1 = Vote(option=option1, number=0)
        vote2 = Vote(option=option2, number=0)
        vote1.save()
        vote2.save()

    return render(request, 'creation.html', context)

