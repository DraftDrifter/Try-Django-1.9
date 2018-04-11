
from django.db import models

from django.db.models.signals import pre_save
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment
from .utils import get_read_time

# Create your models here.
class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(published__lte=timezone.now())

class FutDraPostManager(models.Manager):
    def all(self, current_user, *args, **kwargs):
        user_draft_posts =  super(FutDraPostManager, self).filter(user=current_user).filter(draft=True)
        user_future_posts = super(FutDraPostManager, self).filter(user=current_user).filter(draft=False).filter(published__gte=timezone.now())
        active_list = Post.objects.active()
        return user_draft_posts | user_future_posts | active_list

        
def upload_location(instance, filename):
    return "%s/%s"%(instance.id, filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True,
        width_field="width_field",
        height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    published = models.DateField(auto_now=False, auto_now_add=False)
    read_time = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = PostManager()
    current_user = FutDraPostManager()

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

#    def get_current_users_futureposts_drafts(request):
#        user_drafts = Post.objects.all().filter(user=request.user).filter(draft=True)
#        user_past_posts = Post.objects.all().filter(user=request.user).filter(draft=False).filter(published__gte=timezone.now())
#        active_list = Post.objects.active()
#        return user_drafts | active_list | user_past_posts


    class Meta:
        ordering=["-timestamp", "-updated"]

'''OOLD TRYDJANGO19 SLUG CREATOR:

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug= "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
'''

'''New Slug Creator:'''

from .utils import unique_slug_generator

def pre_save_post_receiver(sender, instance, *args, **wkargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

    if instance.content:
        html_string = instance.content
        read_time = get_read_time(html_string)
        instance.read_time = read_time

pre_save.connect(pre_save_post_receiver, sender=Post)
