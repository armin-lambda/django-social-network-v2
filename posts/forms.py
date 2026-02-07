import os

from django import forms

from .models import Post, Comment


class PostCreateForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Title',
            'class': 'form-input',
        }),
    )
    description = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Description',
            'class': 'form-textarea',
        }),
    )
    file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-input-file'
        }),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self):
        self.cleaned_data['user'] = self.user
        cd = self.cleaned_data

        return Post.objects.create(**cd)


class PostUpdateForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Title',
            'class': 'form-input',
        }),
    )
    description = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Description',
            'class': 'form-textarea',
        }),
    )
    file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-input-file',
        }),
    )

    def __init__(self, *args, **kwargs):
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
    
    def save(self):
        cd = self.cleaned_data

        self.post.title = cd['title']
        self.post.description = cd['description']

        if cd['file'] is not None:
            os.remove(self.post.file.path)
            self.post.file = cd['file']
        self.post.save()
        
        return self.post


class CommentCreateForm(forms.Form):
    body = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'placeholder': 'Write your comment...',
            'class': 'form-textarea',
            'rows': '5',
        }),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
    
    def save(self):
        self.cleaned_data['user'] = self.user
        self.cleaned_data['post'] = self.post
        cd = self.cleaned_data
        
        return Comment.objects.create(**cd)
