from django.urls import path
from apps.core.views import NotificationListView, NotificationReadView, NotificationUnreadCountView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<uuid:pk>/read/', NotificationReadView.as_view(), name='notification-read'),
    path('notifications/unread-count/', NotificationUnreadCountView.as_view(), name='notification-unread-count'),
]