from django import forms
from pagedown.widgets import PagedownWidget
from posts.models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(attrs={"show_preview": False}))
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = [
            "title",
            "image",
            "content",
            "draft",
            "publish",

        ]