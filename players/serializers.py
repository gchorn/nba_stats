from rest_framework import serializers

from players.models import Division, Player, SeasonStats, Team


class DivisionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Division
        fields = ('id', 'name', 'conference', 'teams')
        depth = 1


class TeamSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Team
        fields = ('id', 'name', 'short_name', 'city', 'division', 'wins', 'losses', 'current_players')
        depth = 1


class PlayerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'first_name', 'last_name', 'dob', 'age', 'pos',
                  'current_team', 'season_stats', 'height_inches',
                  'height_feet', 'weight', 'years_pro')
        depth = 1


class SeasonStatsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SeasonStats
        fields = ('id', 'player', 'season_year', 'playoffs', 'gp', 'mp',
                  'fg', 'fga', 'ft', 'fta', 'three_pointers',
                  'threes_attempted', 'orb', 'drb', 'ast', 'stl', 'blk')
        depth = 1
