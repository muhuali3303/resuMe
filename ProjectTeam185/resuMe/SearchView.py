from resuMe.models import *
from django.shortcuts import render
from django.contrib.auth.models import User
from itertools import chain
from django.db.models import Q

# Views for search
def search(request):
    keyword = request.GET['key']
    keyword = keyword.lower()
    result = set()
    context = {}
    blocks = Block.objects.all()
    contents = BlockContent.objects.all()
    all_users = User.objects.all()
    for block in blocks:
        if keyword in block.title.lower():
            result.add(block.user.id)
    for content in contents:
        if keyword in content.sub_title.lower() or keyword in content.content.lower():
            result.add(content.block.user.id)
    for user in all_users:
        if keyword in user.first_name.lower() or keyword in user.last_name.lower() or keyword in user.email.lower():
            result.add(user.id)
    user_infos = UserInfo.objects.filter(Q(about__icontains=keyword) | Q(summary__icontains=keyword))
    users = User.objects.all().filter(id__in=result)
    infos = chain(UserInfo.objects.all().filter(user__in=users.all()),user_infos)
    context['Infos'] = infos
    return render(request, 'Infos.json', context, content_type='application/json')
