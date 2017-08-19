from rest_framework import serializers

from players.models import Player, SeasonStats, Team


class TeamSerializer(serializers.ModelSerializer):
    current_players = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name='player-detail'
    )

    class Meta:
        model = Team
        fields = ('name', 'short_name', 'city', 'division', 'wins', 'losses', 'current_players')


class PlayerSerializer(serializers.ModelSerializer):
    current_team = serializers.HyperlinkedRelatedField(
        queryset=Team.objects.all(),
        view_name='team-detail'
    )
    season_stats = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name='seasonstats-detail'
    )

    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'dob', 'age', 'pos',
                  'current_team', 'season_stats')


class SeasonStatsSerializer(serializers.ModelSerializer):
    player = serializers.HyperlinkedRelatedField(
        queryset=Player.objects.all(),
        view_name='player-detail'
    )
    team = serializers.HyperlinkedRelatedField(
        queryset=Team.objects.all(),
        view_name='team-detail'
    )

    class Meta:
        model = SeasonStats
        fields = ('player', 'team', 'start', 'end', 'playoffs', 'gp', 'mp',
                  'fg', 'fga', 'ft', 'fta', 'three_pointers',
                  'threes_attempted', 'orb', 'drb', 'ast', 'stl', 'blk')
