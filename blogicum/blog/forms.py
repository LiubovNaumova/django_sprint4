from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Форма создания и редактирования постов."""

    class Meta:
        model = Post
        # Важно: добавили is_published, чтобы автор мог снять публикацию
        fields = (
            "title",
            "text",
            "pub_date",
            "location",
            "category",
            "image",
            "is_published",
        )
        widgets = {
            "pub_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def init(self, *args, **kwargs):
        """Приведение формата pub_date к HTML5 datetime-local."""
        super().init(*args, **kwargs)
        if self.instance and self.instance.pub_date:
            self.initial["pub_date"] = self.instance.pub_date.strftime(
                "%Y-%m-%dT%H:%M"
            )


class CommentForm(forms.ModelForm):
    """Форма для добавления и редактирования комментариев к посту."""

    class Meta:
        model = Comment
        fields = ("text",)
