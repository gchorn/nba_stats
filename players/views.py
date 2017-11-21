from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from players.models import Division, Player, SeasonStats, Team
from players.serializers import (
    DivisionSerializer, PlayerSerializer, SeasonStatsSerializer,
    TeamSerializer)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_query_param = 'page'


class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    pagination_class = LargeResultsSetPagination


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    pagination_class = LargeResultsSetPagination

    @list_route()
    def search(self, request):
        name_query = request.query_params.get('name')
        team_query = request.query_params.get('team')
        team_id_query = request.query_params.get('teamId')

        if name_query:
            names = name_query.split()

            query = Q(first_name__icontains=names[0]) | Q(
                last_name__icontains=names[0])
            for name in names[1:]:
                query = query | (
                    Q(first_name__icontains=name) | Q(last_name__icontains=name)
                )

            player_matches = Player.objects.filter(query)
        elif team_query:
            query = Q(current_team__name__icontains=team_query) | Q(
                current_team__short_name__icontains=team_query)
            player_matches = Player.objects.filter(query)
        elif team_id_query:
            query = Q(current_team__id__exact=team_id_query)
            player_matches = Player.objects.filter(query)
        else:
            player_matches = Player.objects.all()

        page = self.paginate_queryset(player_matches)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(name_query, many=True)
        return Response(serializer.data)


class SeasonStatsViewSet(viewsets.ModelViewSet):
    queryset = SeasonStats.objects.all()
    serializer_class = SeasonStatsSerializer
