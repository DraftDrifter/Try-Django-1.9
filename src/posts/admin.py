from django import forms
from django.contrib import admin
from .models import Post
from ckeditor.widgets import CKEditorWidget
# Register your models here.

#

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = [
            "title",
            "image",
            "content",
            "draft",
            "published"

        ]



class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ["title", "timestamp", "updated"]
    list_display_links = ["timestamp"]
    list_filter = ["timestamp"]
    search_fields = ["title", "content"]
    list_editable = ["title"]
    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)
