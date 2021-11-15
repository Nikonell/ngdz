from django.urls import path
from .views import *

urlpatterns = [
    path('parsing/manual/start/', manual_parse),
    path('', index, name='home'),
    path('<slug:lesson>/<int:klass>/<slug:book_slug>/', show_book),
    path('task/<path:task_link>/', show_task),
]
