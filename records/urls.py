from django.urls import path
from .views import RecordListView, RecordDetailView, RecordCreateView, RecordUpdateView, RecordDeleteView

app_name = 'records'

urlpatterns = [
    path('', RecordListView.as_view(), name='list'),
    path('create/', RecordCreateView.as_view(), name='create'),
    path('<int:pk>/', RecordDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', RecordUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', RecordDeleteView.as_view(), name='delete'),
]
