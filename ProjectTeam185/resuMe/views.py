from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from resuMe.forms import *
from resuMe.models import *
from django.core.urlresolvers import reverse
from mimetypes import guess_type
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.mail import send_mail


# page for login
def index(request):
    return render(request, 'index.html')


# views for register
def register(request):
    context = {'SignInForm': SignInForm, 'RForm': RegistrationForm()}
    # return immediately when the method is get
    if request.method == 'GET':
        return render(request, 'index.html', context)
    # create a form from the POST
    form = RegistrationForm(request.POST)
    context['RForm'] = form
    # if form is not valid, redirect back to register page
    if not form.is_valid():
        return render(request, 'index.html', context)
    # a valid form will create a new user
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'])
    new_user.save()
    new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
    # create a user's correspond account object
    new_account = UserInfo(user=new_user)
    new_account.save()
    login(request, new_user)
    # pre generate default resume for user
    # =============================================================================================
    education = Block(title='EDUCATION', user=new_user, index=1)
    skills = Block(title='SKILL', user=new_user, index=2)
    workE = Block(title='WORK EXPERIENCE', user=new_user, index=3)
    education.save()
    skills.save()
    workE.save()
    college1 = BlockContent(block=education, sub_title='College1', content='Degree1', index=1)
    college2 = BlockContent(block=education, sub_title='College2', content='Degree2', index=2)
    college1.save()
    college2.save()
    skill1 = BlockContent(block=skills, sub_title='Skill1', index=1)
    skill2 = BlockContent(block=skills, sub_title='Skill2', index=2)
    skill1.save()
    skill2.save()
    workExperience1 = BlockContent(block=workE, sub_title='Experience1', index=1)
    workExperience1.save()
    # =============================================================================================
    # end pre generate
    return redirect(reverse('resuMe.views.main_page'))


# Views to get photo
def photo(request, id):
    show_user = get_object_or_404(User, id=id)
    account = get_object_or_404(UserInfo, user=show_user)
    content_type = guess_type(account.photo.name)
    return HttpResponse(account.photo, content_type=content_type)


# Given a block-content id, get all it's picture's id
def get_picture_ids(request,blockcontent_id):
    blockcontent = BlockContent.objects.get(id=blockcontent_id)
    pictures = Picture.objects.filter(blockcontent=blockcontent)
    list = [0]*len(pictures)
    for i in range(len(pictures)):
        list[i] = pictures[i].id
    return JsonResponse(list, safe=False)


# Given a user id, go to his resume page
def resume(request, id):
    context = {}
    homeUser = get_object_or_404(User, id=id)
    context['user'] = request.user
    uInfo = get_object_or_404(UserInfo, user=homeUser)
    uInfo.click()
    context['userInfo'] = uInfo
    resumeContent = {}
    blocks = Block.objects.all().filter(user=homeUser).order_by('index')
    context['blocks'] = blocks
    context['isEdit'] = 'false'
    for bb in blocks:
        contents = BlockContent.objects.all().filter(block=bb).order_by('index')
        resumeContent[bb.id] = contents
    context['resumeContent'] = resumeContent
    return render(request, 'Home.html', context)


# Views for edit resume
@login_required
def edit_resume(request):
    context = {}
    context['myself'] = 'True'
    context['user'] = request.user
    uInfo = get_object_or_404(UserInfo, user=request.user)
    context['userInfo'] = uInfo
    resumeContent = {}
    blocks = Block.objects.all().filter(user=request.user).order_by('index')
    context['blocks'] = blocks
    context['isEdit'] = 'True'
    for bb in blocks:
        contents = BlockContent.objects.all().filter(block=bb).order_by('index')
        resumeContent[bb.id] = contents
    context['resumeContent'] = resumeContent
    return render(request, 'Home.html', context)


# Views to get picture
def get_picture(request, pid):
    picture = get_object_or_404(Picture, id=pid)
    picture_file = picture.picture_file
    content_type = guess_type(picture_file.name)
    return HttpResponse(picture_file, content_type=content_type)


# Views for main page
def main_page(request):
    return render(request, 'main.html')


# Views for send email
def send_email(request, uid):
    toUser = get_object_or_404(UserInfo, id=uid)
    form = EmailForm(request.GET)
    if not form.is_valid():
        return HttpResponse('fail')
    email_content = 'Hello ' + toUser.user.get_full_name() + ', '
    email_content += form.cleaned_data['name'] + ' send you an email from resuMe. \n'
    email_content += 'To reply, send to: ' + form.cleaned_data['email']
    email_content += '\n================================================================\n'
    email_content += 'From: ' + form.cleaned_data['name']
    email_content += '\nMessage: \n' + form.cleaned_data['message']
    send_mail('Email from resuMe', email_content, 'kangw@andrew.cmu.edu', [toUser.user.email])
    return HttpResponse('success')















