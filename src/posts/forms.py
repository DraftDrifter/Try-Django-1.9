from .models import Post
from django import forms
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import ugettext_lazy as _

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    published = forms.DateField(widget=forms.SelectDateWidget(), label="Published on:")
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "draft",
            "published",
            "image",

        ]
        labels = {
            "image": _("Thumbnail:")
        }
