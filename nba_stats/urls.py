from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from players import views

router = DefaultRouter(trailing_slash=False)
router.register(r'players', views.PlayerViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'season-stats', views.SeasonStatsViewSet)
router.register(r'divisions', views.DivisionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]

urlpatterns += staticfiles_urlpatterns()