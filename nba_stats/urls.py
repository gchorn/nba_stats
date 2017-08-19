from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from players import views

router = DefaultRouter(trailing_slash=False)
router.register(r'players', views.PlayerViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'season_stats', views.SeasonStatsViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
