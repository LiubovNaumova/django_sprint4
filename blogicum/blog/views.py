from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post
from .utils import get_published_posts

User = get_user_model()


def get_post_comments(post):
    """Вернуть queryset комментариев к посту (с автором, по времени создания)."""
    return post.comments.select_related("author").order_by("created_at")


class PostListView(ListView):
    """Главная страница: список опубликованных постов."""

    template_name = "blog/index.html"
    paginate_by = 10

    def get_queryset(self):
        """A) Показываем только опубликованные посты."""
        return get_published_posts().order_by("-pub_date")


class CategoryPostsView(ListView):
    """Страница категории: опубликованные посты выбранной категории."""

    template_name = "blog/category.html"
    paginate_by = 10

    def get_queryset(self):
        """A) В категории показываем только опубликованные посты."""
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs["category_slug"],
            is_published=True,
        )
        return (
            get_published_posts()
            .filter(category=self.category)
            .order_by("-pub_date")
        )

    def get_context_data(self, **kwargs):
        """Добавить категорию в контекст."""
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class PostDetailView(DetailView):
    """Детальная страница поста + комментарии."""

    model = Post
    template_name = "blog/detail.html"
    pk_url_kwarg = "post_id"

    def get_object(self, queryset=None):
        """
        B) Автор видит свой пост всегда.
        Остальные видят только если пост опубликован,
        категория опубликована и дата не в будущем.
        """
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])

        if self.request.user.is_authenticated and self.request.user == post.author:
            return post

        if (
            post.is_published
            and post.category.is_published
            and post.pub_date <= timezone.now()
        ):
            return post

        raise Http404("Страница не найдена")

    def get_context_data(self, **kwargs):
        """Добавить форму комментария и список комментариев."""
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = get_post_comments(self.object)
        return context


class ProfileView(ListView):
    """C) Профиль пользователя: все посты автора (включая непубличные)."""

    template_name = "blog/profile.html"
    paginate_by = 10

    def get_queryset(self):
        username = self.kwargs["username"]
        self.profile_user = get_object_or_404(User, username=username)

        return (
            Post.objects.filter(author=self.profile_user)
            .select_related("author", "category", "location")
            .annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
        )

    def get_context_data(self, **kwargs):
        """Добавить объект профиля в контекст."""
        context = super().get_context_data(**kwargs)
        context["profile"] = self.profile_user
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание поста."""

    model = Post
    form_class = PostForm
    template_name = "blog/create.html"
    
    def form_valid(self, form):
        """Привязать автора и сохранить."""
        form.instance.author = self.request.user
        self.object = form.save()
        return redirect("blog:profile", username=self.object.author.username)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование поста (в т.ч. is_published)."""

    model = Post
    form_class = PostForm
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"

    def dispatch(self, request, *args, **kwargs):
        """Редактировать может только автор."""
        self.object = self.get_object()
        if self.object.author != request.user:
            return redirect("blog:post_detail", post_id=self.object.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Сохранить изменения. is_published меняется из формы."""
        self.object = form.save()
        return redirect("blog:post_detail", post_id=self.object.pk)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление поста автором."""

    model = Post
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"
    success_url = reverse_lazy("blog:index")

    def get_queryset(self):
        """Удалять можно только свои посты."""
        return super().get_queryset().filter(author=self.request.user)


class AddCommentView(LoginRequiredMixin, CreateView):
    """Добавление комментария к посту."""

    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"

    def form_valid(self, form):
        """Привязать комментарий к посту и автору."""
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        form.instance.post = post
        form.instance.author = self.request.user
        self.object = form.save()
        return redirect("blog:post_detail", post_id=post.pk)


class EditCommentView(LoginRequiredMixin, UpdateView):
    """Редактирование комментария (только автором комментария)."""

    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"

    def dispatch(self, request, *args, **kwargs):
        """Редактировать может только автор комментария."""
        self.object = self.get_object()
        if self.object.author != request.user:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Сохранить изменения и вернуться к посту."""
        self.object = form.save()
        return redirect("blog:post_detail", post_id=self.kwargs["post_id"])


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    """Удаление комментария (только автором комментария)."""

    model = Comment
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"

    def get_success_url(self):
        """После удаления вернуться на страницу поста."""
        return reverse("blog:post_detail", kwargs={"post_id": self.kwargs["post_id"]})
