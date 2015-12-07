from django.contrib.auth.decorators import login_required
from resuMe.models import *
from django.shortcuts import render


# Get top 5 popular User
def get_popular(request):
    context = {}
    popularU = UserInfo.objects.all().filter(edited=True).order_by('-click_count')
    index = min(5, len(popularU))
    popularU = popularU[:index]
    context['Infos'] = popularU
    return render(request, 'Infos.json', context, content_type='application/json')


# Get top 5 new User
def get_newest(request):
    context = {}
    newestU = UserInfo.objects.all().filter(edited=True).order_by('-created_at')
    index = min(5, len(newestU))
    newestU = newestU[:index]
    context['Infos'] = newestU
    return render(request, 'Infos.json', context, content_type='application/json')


# Get random 5 User as recommendation
def get_recommend(request):
    context = {}
    recommendU = UserInfo.objects.all().filter(edited=True).order_by('?')
    index = min(5, len(recommendU))
    recommendU = recommendU[:index]
    context['Infos'] = recommendU
    return render(request, 'Infos.json', context, content_type='application/json')


# Get all User
def get_all(request):
    context = {}
    allU = UserInfo.objects.all().filter(edited=True).order_by('user__first_name', 'user__last_name')
    context['Infos'] = allU
    return render(request, 'Infos.json', context, content_type='application/json')
