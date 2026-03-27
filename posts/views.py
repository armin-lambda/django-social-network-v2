from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType

from utils.pagination import get_pagination_context
from notifications.models import Notification
from .forms import CommentCreateForm, PostCreateForm, PostUpdateForm
from .models import Post, Like


class PostListView(LoginRequiredMixin, View):
    template_name = 'posts/index.html'

    def get(self, request):
        post_list = Post.objects.annotate(
            ranking_score=
                (0.5 * Count('comments')) +
                (0.3 * Count('likes'))
        ).order_by('-ranking_score', '-created_at')

        if request.GET.get('search'):
            search = request.GET.get('search')
            post_list = post_list.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(user__username__icontains=search)
            )

        return render(request, self.template_name, {
            'page_obj': get_pagination_context(request, post_list, 10),
        })


class PostCreateView(LoginRequiredMixin, View):
    template_name = 'posts/post_create.html'
    form_class = PostCreateForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES, user=request.user)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        
        post = form.save()
        notifications = [
            Notification(
                from_user=post.user,
                to_user=f,
                type=Notification.Type.POST,
                content_type=ContentType.objects.get_for_model(Post),
                object_id=post.id,
            )
            for f in post.user.get_follower_list()
        ]
        Notification.objects.bulk_create(notifications)

        messages.success(request, 'Post created successfully', 'success')
        return redirect(request.user.get_absolute_url())


class PostUpdateView(LoginRequiredMixin, View):
    template_name = 'posts/post_update.html'
    form_class = PostUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class(initial={
                'title': self.post_instance.title,
                'description': self.post_instance.description,
            }),
        })

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request.FILES, post=self.post_instance)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        post = form.save()
        messages.success(request, 'Post edited successfully', 'success')
        return redirect(post.get_absolute_url())


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        get_object_or_404(Post, pk=kwargs['pk']).delete()
        messages.success(request, 'Post deleted successfully', 'success')
        return redirect('posts:post-list')


class PostDetailView(LoginRequiredMixin, View):
    template_name = 'posts/post_detail.html'
    form_class = CommentCreateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, **kwargs):
        post = self.post_instance
        return render(request, self.template_name, {
            'post': post,
            'is_liked': Like.objects.filter(user=request.user, post=post).exists(),
            'form': self.form_class(),
            'page_obj': get_pagination_context(request, post.get_comment_list(), 10),
        })

    def post(self, request, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, user=request.user, post=post)

        if not form.is_valid():
            return render(request, self.template_name, {
                'post': post,
                'form': form,
                'page_obj': get_pagination_context(request, post.get_comment_list(), 10),
            })

        comment = form.save()

        if request.user != post.user:
            Notification.objects.create(
                from_user=request.user,
                to_user=post.user,
                type=Notification.Type.COMMENT,
                content_type=ContentType.objects.get_for_model(comment),
                object_id=comment.id,
            )

        messages.success(request, 'Comment posted successfully', 'success')
        return redirect(post.get_absolute_url())


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])

        if not Like.objects.filter(user=request.user, post=post).exists():
            like = Like.objects.create(user=request.user, post=post)

            if request.user != post.user:
                Notification.objects.create(
                    from_user=request.user,
                    to_user=post.user,
                    type=Notification.Type.LIKE,
                    content_type=ContentType.objects.get_for_model(Like),
                    object_id=like.id,
                )

            messages.success(request, 'Post liked successfully', 'success')
        return redirect(post.get_absolute_url())
  

class PostUnlikeView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        like = Like.objects.filter(user=request.user, post=post)

        if like.exists():
            like.delete()
            messages.success(request, 'Post unliked successfully', 'success')
        return redirect(post.get_absolute_url())
