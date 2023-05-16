from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),

]
