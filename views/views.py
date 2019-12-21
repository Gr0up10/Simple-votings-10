from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
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


def vote(request,option_id):
    if request.method== 'POST':
        vote = Vote(option=Option.objects.get(id=option_id),user=request.user)
        vote.save()
        return HttpResponse('Ваш голос защитан')

    return HttpResponse('передай пост запрос плиз')

def create(request):
    context = {}
    context['mode'] = 1
    if request.method == 'GET':
        context['form'] = CreateVoting()

    if request.method == 'POST':
        if request.user.is_authenticated:
            main_text = request.POST.get('main_text')
            voting = Voting(question=main_text, author=request.user.id)

            voting.save()
            count = request.POST.get('count')
            if count :
                for i in range(1,int(count)+1):
                    text = request.POST.get('option'+str(i))
                    option = Option(voting = voting, text =text)
                    option.save()
            return HttpResponse('Ваш вопрос добавлен')
        else:
            return HttpResponse('Сперва войди!')
    return render(request, 'creation.html', context)

