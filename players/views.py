from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from players.models import Division, Player, SeasonStats, Team
from players.serializers import (
    DivisionSerializer, PlayerSerializer, SeasonStatsSerializer,
    TeamSerializer)


class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    @list_route()
    def player_search(self, request):
        player_query = request.query_params.get('name', None)

        names = player_query.split()

        query = Q(first_name__icontains=names[0]) | Q(
            last_name__icontains=names[0])
        for name in names[1:]:
            query = query | (
                Q(first_name__icontains=name) | Q(last_name__icontains=name)
            )

        if player_query:
            player_matches = Player.objects.filter(query)

        page = self.paginate_queryset(player_matches)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(player_query, many=True)
        return Response(serializer.data)


class SeasonStatsViewSet(viewsets.ModelViewSet):
    queryset = SeasonStats.objects.all()
    serializer_class = SeasonStatsSerializer
