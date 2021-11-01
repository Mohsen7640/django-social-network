from django.contrib import messages

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView
from django.http import JsonResponse

from post.models import Post, Like
from account.models import Profile
from post.forms import CreatePostForm, CreateCommentForm


@login_required
def list_post_view(request):
    qs = Post.objects.all()
    profile = get_object_or_404(Profile, user=request.user)

    # Post form, Comment form
    p_form = CreatePostForm()
    c_form = CreateCommentForm()

    context = {
        'qs': qs,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
    }
    return render(request, 'post/main.html', context)


@login_required
@require_POST
def create_post_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    p_form = CreatePostForm(data=request.POST or None, files=request.FILES or None)

    if p_form.is_valid():
        instance = p_form.save(commit=False)
        instance.author = profile
        instance.save()

    return redirect('post:list-post')


@login_required
@require_POST
def create_comment_view(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)

    profile = get_object_or_404(Profile, user=request.user)
    c_form = CreateCommentForm(data=request.POST or None)

    if c_form.is_valid():
        instance = c_form.save(commit=False)
        instance.user = profile
        instance.post = post
        instance.save()

    return redirect('post:list-post')


@login_required
@require_POST
def like_unlike_post_view(request):
    user_obj = request.user
    profile_obj = get_object_or_404(Profile, user=user_obj)

    post_id = request.POST.get('post_id')
    post_obj = get_object_or_404(Post, id=post_id)

    if profile_obj in post_obj.liked.all():
        post_obj.liked.remove(profile_obj)
    else:
        post_obj.liked.add(profile_obj)

    like, created = Like.objects.get_or_create(user=user_obj, post=post_obj)

    if created:
        like.value = Like.LIKE
    else:
        if like.value == Like.LIKE:
            like.value = Like.UNLIKE
        else:
            like.value = Like.LIKE
    
    profile_obj.save()
    like.save()

    return redirect('post:list-post')


class UpdatePostView(LoginRequiredMixin, UpdateView):
    template_name = 'post/update.html'
    model = Post
    form_class = CreatePostForm
    success_url = reverse_lazy('post:list-post')

    def get_object(self, queryset=None, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Post, pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, message='You need to be the author of the post in order to update it.')
        return obj

    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user)

        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You need to be the author of the post in order to update it.')
            return super().form_invalid(form)
 

class DeletePostView(LoginRequiredMixin, DeleteView):
    template_name = 'post/confirm_delete.html'
    model = Post
    success_url = reverse_lazy('post:list-post')

    def get_object(self, queryset=None, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Post, pk=pk)

        if not obj.author.user == self.request.user:
            messages.warning(self.request, message='You need to be the author of the post in order to delete it.')
        return obj
