from django.urls import path

from ai.views import AiView

app_name = 'ai'

urlpatterns = [
    path('similar/', AiView.as_view(), name='similar')
]