from rest_framework import viewsets

from players.models import Player, SeasonStats, Team
from players.serializers import (PlayerSerializer, SeasonStatsSerializer,
                                 TeamSerializer)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class SeasonStatsViewSet(viewsets.ModelViewSet):
    queryset = SeasonStats.objects.all()
    serializer_class = SeasonStatsSerializer
