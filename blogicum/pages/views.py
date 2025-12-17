from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    """Обработчик для страницы "О проекте".
    
    Отображает статическую страницу с информацией о проекте,
    используя шаблон 'pages/about.html'.
    
    Наследуется от TemplateView, поэтому автоматически обрабатывает GET-запросы
    и отображает указанный шаблон без дополнительной логики.
    """
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Обработчик для страницы правил проекта.
    
    Отображает статическую страницу с правилами использования сервиса,
    используя шаблон 'pages/rules.html'.
    
    Как и AboutView, наследует базовую функциональность TemplateView
    для отображения шаблона без дополнительной бизнес-логики.
    """
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """Кастомный обработчик ошибки 404 (страница не найдена).
    
    Заменяет стандартную страницу 404 Django на пользовательскую версию.
    
    Args:
        request (HttpRequest): Объект HTTP-запроса
        exception (Exception): Исключение, вызвавшее ошибку 404
        
    Returns:
        HttpResponse: Ответ с пользовательской страницей 404 и статусом 404
    """
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Кастомный обработчик ошибки CSRF валидации.
    
    Заменяет стандартную страницу 403 CSRF Django на пользовательскую версию.
    
    Args:
        request (HttpRequest): Объект HTTP-запроса
        reason (str, optional): Причина ошибки CSRF. По умолчанию ''.
        
    Returns:
        HttpResponse: Ответ с пользовательской страницей 403 CSRF и статусом 403
    """
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """Кастомный обработчик ошибки 500 (внутренняя ошибка сервера).
    
    Заменяет стандартную страницу 500 Django на пользовательскую версию.
    Используется, когда возникает непредвиденная ошибка в приложении.
    
    Args:
        request (HttpRequest): Объект HTTP-запроса
        
    Returns:
        HttpResponse: Ответ с пользовательской страницей 500 и статусом 500
    """
    return render(request, 'pages/500.html', status=500)
