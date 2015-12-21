__author__ = 'ken'
from resuMe.forms import *
from resuMe.models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def first_last_sum(request):
    thisU = request.user
    userInfo = get_object_or_404(UserInfo, user=thisU)
    form = FLSForm(request.POST, request.FILES, instance=userInfo)
    if not form.is_valid():
        return JsonResponse(form.errors.as_json(), safe=False)
    form.save()
    datas = form.cleaned_data
    thisU.first_name = datas['first_name']
    thisU.last_name = datas['last_name']
    thisU.save()
    return HttpResponse("success")


@login_required
def edit_about(request):
    thisU = request.user
    userInfo = get_object_or_404(UserInfo, user=thisU)
    form = AboutForm(request.POST, instance=userInfo)
    if not form.is_valid():
        return HttpResponse('fail')
    form.save()
    return HttpResponse("success")


@login_required
def edit_contact(request):
    thisU = request.user
    userInfo = get_object_or_404(UserInfo, user=thisU)
    user = request.user
    form = APEForm(request.POST, instance=userInfo)
    if not form.is_valid():
        return HttpResponse('fail')
    form.save()
    user.email = form.cleaned_data.get("email")
    user.save()
    return HttpResponse("success")

