from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if not text:
            return render(request, 'blog/comment_form.html', {
                'post': post,
                'error': 'Comentário vazio não permitido.'
            })

        Comment.objects.create(
            post=post,
            author=request.user,
            text=text,
            created_at=timezone.now()
        )
        return redirect('blog:post_detail', pk=post.pk)

    return render(request, 'blog/comment_form.html', {'post': post})