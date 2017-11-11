from rest_framework import serializers

from players.models import Division, Player, SeasonStats, Team


class DivisionSerializer(serializers.HyperlinkedModelSerializer):
    conference = serializers.CharField(source='get_conference_display', read_only=True)

    class Meta:
        model = Division
        fields = ('id', 'name', 'conference', 'teams')
        depth = 1


class TeamDivisionSerializer(serializers.HyperlinkedModelSerializer):
    conference = serializers.CharField(source='get_conference_display', read_only=True)

    class Meta:
        model = Division
        fields = ('url', 'name', 'conference')


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    choose_division = serializers.HyperlinkedRelatedField(
        queryset=Division.objects.all(), 
        view_name='division-detail', 
        source='division',
        write_only=True)
    division = TeamDivisionSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'short_name', 'city', 'wins', 'division',
                  'losses', 'current_players', 'choose_division')
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
