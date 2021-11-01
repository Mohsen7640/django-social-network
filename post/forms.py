from django import forms

from post.models import Post, Comment


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'image')

        widgets = {
            'content': forms.Textarea(attrs={'rows': 3})
        }


class CreateCommentForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))

    class Meta:
        model = Comment
        fields = ('body',)
