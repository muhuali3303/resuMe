from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.html import escape


# A user's information
class UserInfo(models.Model):
    user = models.OneToOneField(User)
    photo = models.ImageField(upload_to="./", blank=True, default='Doge.jpeg')
    summary = models.CharField(max_length=200, default='Take a look at my resume!')
    phone = models.IntegerField(default=0)
    address = models.CharField(max_length=50, default='No provided')
    profile_background = models.ImageField(upload_to="pictures")
    created_at = models.DateTimeField(default=datetime.datetime.now())
    click_count = models.IntegerField(default=0)
    about = models.CharField(max_length=500, default='No Information...')
    edited = models.BooleanField(default=False)

    def __unicode__(self):
        return "user_info: " + self.user.first_name + " " + self.user.last_name

    def click(self):
        self.click_count += 1

    @property
    def html(self):
        block = Block.objects.filter(user=self.user).order_by('index').first()
        contents = BlockContent.objects.all().filter(block=block)
        result = '''<h1>{}</h1>
                    <hr>
                    <div class="row">
                        <div class="col-md-4">
                            <img class="img-responsive img-circle" src="/resuMe/photo/{}">
                        </div>
                        <div class="col-md-8">
                        <h3 class="main-title">{}</h3>
                '''
        for content in contents:
            cont = '''
                <div>
                    <h4 class="main-sub">{}</h4>
                </div>
                <div class="col-sm-offset-1">
                    <p class="main-content">{}</p>
                </div>
            '''.format(content.sub_title, escape(content.content))
            result += cont
        result += '''</div>
                    </div>
                    <hr>
                    <p>{}</p>
                    <a class="btn btn-success" href="/resuMe/resume/{}">See More <span class="glyphicon glyphicon-chevron-right"></span></a>
                    <hr class="Seperator">'''.replace('\n', '\\n').replace('\t', '')
        result = result.format(self.user.get_full_name(), self.id, block.title, self.summary, self.id).replace('"', "'")
        return result


# block is the basic unit of a resume
# a block contains a title and a content
class Block(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=40)
    index = models.IntegerField(default=0)

    def __unicode__(self):
        return "Block " + self.user.first_name + " " + self.user.last_name


# a blockContent contains a subtitle and content
class BlockContent(models.Model):
    block = models.ForeignKey(Block)
    sub_title = models.CharField(max_length=40, blank=True, default="Description")
    content = models.CharField(max_length=200, blank=True, default="Description")
    url = models.URLField(blank=True, default="")
    index = models.IntegerField(default=0)

    def __unicode__(self):
        return "BlockContent " + self.sub_title

    def str(self):
        return "BlockContent " + self.sub_title


# a user can have many pictures which form a picture gallery.
class Picture(models.Model):
    picture_file = models.ImageField(upload_to="./", blank=True)
    blockcontent = models.ForeignKey(BlockContent)
    description = models.CharField(max_length=200, blank=True, default="Description")

    def __unicode__(self):
        return "Picture " + self.picture_file.name


