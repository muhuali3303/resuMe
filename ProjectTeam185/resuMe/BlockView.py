from resuMe.forms import *
from resuMe.models import *
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse


# add a block
def add_block(request):
    title = request.POST.get('title', '')
    new_block = Block(title=title, user=request.user, index=len(Block.objects.all().filter(user=request.user)) + 1)
    new_block.save()
    userInfo = get_object_or_404(UserInfo, user=request.user)
    userInfo.edited = True
    userInfo.created_at = datetime.datetime.now()
    userInfo.save()
    return HttpResponse(new_block.id)


# delete a block
def delete_block(request):
    toDelete = get_object_or_404(Block, id=request.POST.get('id', 0))
    toDelete.delete()
    return HttpResponse("")


# add a block content
def add_block_content(request, block_id):
    block = get_object_or_404(Block, id=block_id)
    new_blockcontent = BlockContent(block=block, index=len(BlockContent.objects.all().filter(block=block)) + 1)
    new_blockcontent.save()
    id = new_blockcontent.id
    userInfo = get_object_or_404(UserInfo, user=request.user)
    userInfo.edited = True
    userInfo.created_at = datetime.datetime.now()
    userInfo.save()
    return HttpResponse(id)


# edit block content
def edit_blockcontent(request, blockcontent_id):
    blockcontent = get_object_or_404(BlockContent, id=blockcontent_id)
    bForm = BlockContentForm(request.POST, instance=blockcontent)

    # valid by form
    if not bForm.is_valid():
        return JsonResponse(bForm.errors.as_json(), safe=False)

    bForm.save()
    userInfo = get_object_or_404(UserInfo, user=request.user)
    userInfo.edited = True
    userInfo.created_at = datetime.datetime.now()
    userInfo.save()
    # If contain picture
    if request.FILES:
        picture = Picture(blockcontent=blockcontent)
        pForm = BlockContentPicForm(request.POST, request.FILES, instance=picture)
        if pForm.is_valid():
            pForm.save()
            # blockcontent.picture_number = blockcontent.picture_number + 1

    return HttpResponse("Success")


# change position with upper
def block_up(request):
    block = get_object_or_404(Block, id=request.POST.get('id', 0))
    next_content = get_object_or_404(Block, id=request.POST.get('upblock_id', 0))
    this = block.index
    block.index = next_content.index
    next_content.index = this
    block.save()
    next_content.save()
    return HttpResponse('Success')


# change position with down
def block_down(request):
    block = get_object_or_404(Block, id=request.POST.get('id', 0))
    next_content = get_object_or_404(Block, id=request.POST.get('down_id', 0))
    this = block.index
    block.index = next_content.index
    next_content.index = this
    block.save()
    next_content.save()
    return HttpResponse('Success')


# change position with upper
def content_up(request):
    content = get_object_or_404(BlockContent, id=request.POST.get('id', 0))
    next_content = get_object_or_404(BlockContent, id=request.POST.get('next_id', 0))
    this = content.index
    content.index = next_content.index
    next_content.index = this
    content.save()
    next_content.save()
    return HttpResponse('Success')


# change position with down
def content_down(request):
    content = get_object_or_404(BlockContent, id=request.POST.get('id', 0))
    next_content = get_object_or_404(BlockContent, id=request.POST.get('next_id', 0))
    this = content.index
    content.index = next_content.index
    next_content.index = this
    content.save()
    next_content.save()
    return HttpResponse('Success')


# delete a content
def delete_content(request):
    toDelete = get_object_or_404(BlockContent, id=request.POST.get('id', 0))
    toDelete.delete()
    return HttpResponse("")





