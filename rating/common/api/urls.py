from django.urls import path, include
from rest_framework import routers

from .viewsets import LeaderBoardViewSet

router = routers.DefaultRouter()
router.register(r'leaderboard', LeaderBoardViewSet, 'leaderboard')

urlpatterns = [
    path(r'', include(router.urls)),

]
