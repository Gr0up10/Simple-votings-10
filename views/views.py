from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import *


def index(request):
    context = dict()

    context['votings'] = Voting.objects.all()
    context['votes'] = Vote.objects.all()

    if request.method == 'POST':
        option_id = request.POST.get('vote_button')
        if option_id:
            num = int(Vote.objects.filter(option_id=option_id)[0].number)
            num +=1
            Vote.objects.filter(option_id=option_id).update(number=num)

    return render(request, 'index.html', context)


def create(request):
    context = dict()
    context['form'] = CreateVoting()
    if request.method == 'POST':
        main_text = request.POST.get('main_text')
        first = request.POST.get('first')
        second = request.POST.get('second')

        voting = Voting(question=main_text, author=1)
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

