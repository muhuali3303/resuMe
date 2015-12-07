"""ProjectTeam185 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from resuMe.forms import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^resuMe/login$', 'django.contrib.auth.views.login', {'template_name': 'index.html',
                                                                'extra_context': {'showIn': 'active',
                                                                                  'RForm': RegistrationForm(),
                                                                                  'SignInForm': SignInForm(),
                                                                                  },
                                                                }, name='login'),
    url(r'^$', 'resuMe.views.main_page', name='mainPage'),
    url(r'^resuMe/register$', 'resuMe.views.register', name='register'),
    url(r'^resuMe/resume/(?P<id>\d+)$', 'resuMe.views.resume',name="readResume"),
    url(r'^resuMe/photo/(?P<id>\d+)$', 'resuMe.views.photo', name='photo'),
    url(r'^resuMe/get_picture_ids/(?P<blockcontent_id>\d+)$', 'resuMe.views.get_picture_ids', name='getPictureIds'),
    url(r'^resuMe/get_picture/(?P<pid>\d+)$', 'resuMe.views.get_picture', name='getPicture'),
    url(r'^resuMe/resume_edit$', 'resuMe.views.edit_resume', name='Edit_resume'),
    url(r'^resuMe/edit_profile$','resuMe.ProfileEditViews.first_last_sum',name='editProfile'),
    url(r'^resuMe/edit_contact$', 'resuMe.ProfileEditViews.edit_contact', name='editContact'),
    url(r'^resuMe/edit_about$', 'resuMe.ProfileEditViews.edit_about', name='editAbout'),
    url(r'resuMe/add_block$', 'resuMe.BlockView.add_block', name="addBlock"),
    url(r'resuMe/add_block_content/(?P<block_id>\d+)$','resuMe.BlockView.add_block_content', name="addBlockContent"),
    url(r'resuMe/edit_block_content/(?P<blockcontent_id>\d+)$','resuMe.BlockView.edit_blockcontent', name="addBlockContent"),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main$', 'resuMe.views.main_page', name='main'),
    url(r'^get_all$', 'resuMe.GetUserViews.get_all', name='all'),
    url(r'^get_popular$', 'resuMe.GetUserViews.get_popular', name='popular'),
    url(r'^get_new$', 'resuMe.GetUserViews.get_newest', name='newest'),
    url(r'^get_recommend$', 'resuMe.GetUserViews.get_recommend', name='recommend'),
    url(r'^search$', 'resuMe.SearchView.search', name='search'),
    url(r'^content_down$', 'resuMe.BlockView.content_down', name='contentDown'),
    url(r'^content_up$', 'resuMe.BlockView.content_up', name='contentUP'),
    url(r'^block_down$', 'resuMe.BlockView.block_down', name='blockDown'),
    url(r'^block_up$', 'resuMe.BlockView.block_up', name='blockUp'),
    url(r'^resuMe/delete_block$', 'resuMe.BlockView.delete_block', name="deleteBlock"),
    url(r'^resuMe/delete_content$', 'resuMe.BlockView.delete_content', name="deleteContent"),
    url(r'^send_email/(?P<uid>\d+)$', 'resuMe.views.send_email', name='email')
]
