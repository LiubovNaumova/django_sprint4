from django.db.models import Count
from django.utils import timezone

from .models import Post


def get_published_posts():
    """
    Вернуть queryset постов, которые можно показывать всем пользователям.

    Условия:
    - пост опубликован (is_published=True)
    - дата публикации не в будущем (pub_date <= now)
    - категория опубликована (category__is_published=True)
    """
    return (
        Post.objects.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )
        .select_related("author", "category", "location")
        .annotate(comment_count=Count("comments"))
    )
