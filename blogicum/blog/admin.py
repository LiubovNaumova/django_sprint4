from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category, Location, Post


DEFAULT_CITIES = [
    "Москва",
    "Санкт-Петербург",
    "Омск",
    "Саратов",
    "Казань",
    "Новосибирск",
    "Екатеринбург",
    "Самара",
    "Нижний Новгород",
    "Ростов-на-Дону",
    "Краснодар",
    "Уфа",
]

DEFAULT_CATEGORIES = [
    "Путешествия",
    "Туризм",
    "Развлечения",
    "Еда",
    "Спорт",
    "Технологии",
    "Учёба",
    "Музыка",
]


@admin.action(description=_("Создать стандартные города"))
def create_default_locations(modeladmin, request, queryset):
    created_count = 0
    for city in DEFAULT_CITIES:
        obj, created = Location.objects.get_or_create(
            name=city,
            defaults={"is_published": True},
        )
        if created:
            created_count += 1
    modeladmin.message_user(request, f"Города добавлены: {created_count}")


@admin.action(description=_("Создать стандартные категории"))
def create_default_categories(modeladmin, request, queryset):
    created_count = 0
    for title in DEFAULT_CATEGORIES:
        # slug у тебя создаётся автоматически из title в админке,
        # но get_or_create через админку slug сам не заполнит.
        # Поэтому создаём без slug, только если модель позволяет пустой slug.
        # Если slug обязателен — напиши, я дам версию с генерацией slug.
        obj, created = Category.objects.get_or_create(
            title=title,
            defaults={"is_published": True},
        )
        if created:
            created_count += 1
    modeladmin.message_user(request, f"Категории добавлены: {created_count}")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "pub_date",
        "is_published",
        "category",
        "location",
    )
    list_filter = ("is_published", "category", "location")
    search_fields = ("title", "text")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    actions = [create_default_categories]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("name",)
    actions = [create_default_locations]
