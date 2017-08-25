from datetime import datetime
import logging
from time import sleep

from marshmallow import fields, post_load, Schema
import requests

from nba_stats import settings as my_settings
from players.models import Player, SeasonStats

logger = logging.getLogger(__name__)

REQUEST_ARGS = dict(
    headers={'Content-Type': 'application/json'},
    timeout=300
)

STATS_URL = "http://data.nba.net/10s/prod/v1/2016/players/{}_profile.json"


class SeasonStatsSchema(Schema):
    gp = fields.Method(load_from='gamesPlayed', deserialize='cast_int')  # games played
    mp = fields.Method(load_from='min', deserialize='cast_int')  # minutes played
    fg = fields.Method(load_from='fgm', deserialize='cast_int')  # field goals made
    fga = fields.Method(deserialize='cast_int')  # field goals attempted
    ft = fields.Method(load_from='ftm', deserialize='cast_int')  # free throws made
    fta = fields.Method(deserialize='cast_int')  # free throws attempted
    three_pointers = fields.Method(load_from='tpm', deserialize='cast_int')  # threes made
    threes_attempted = fields.Method(load_from='tpa', deserialize='cast_int')
    orb = fields.Method(load_from='offReb', deserialize='cast_int')  # offensive rebounds
    drb = fields.Method(load_from='defReb', deserialize='cast_int')  # defensive rebounds
    ast = fields.Method(load_from='assists', deserialize='cast_int')  # assists
    stl = fields.Method(load_from='steals', deserialize='cast_int')  # steals
    blk = fields.Method(load_from='blocks', deserialize='cast_int')  # blocks
    tov = fields.Method(load_from='turnovers', deserialize='cast_int')  # turnovers
    pf = fields.Method(load_from='pFouls', deserialize='cast_int')  # personal fouls
    pts = fields.Method(load_from='points', deserialize='cast_int')  # points
    season_year = fields.Integer()
    player_id = fields.Integer()

    def cast_int(self, value):
        return int(value)

    @post_load
    def create_season_stats(self, data):
        return SeasonStats(**data)


def gather_player_stats(player, seasons_added):
    season_stats_schema = SeasonStatsSchema(many=True, strict=True)
    player_stats_url = STATS_URL.format(player.api_id)

    logger.debug({
        'msg': 'Requesting player stats for {} {}'.format(
            player.first_name, player.last_name),
        'url': player_stats_url
    })
    player_stats_response = requests.get(player_stats_url, REQUEST_ARGS)

    player_stats = player_stats_response.json()['league']['standard'][
        'stats']['regularSeason']['season']

    for stats in player_stats:
        stats['total']['season_year'] = stats['seasonYear']
        stats['total']['player_id'] = player.id

    season_stats = season_stats_schema.load(
        [stats['total'] for stats in player_stats]
    ).data

    for season in season_stats:
        existing = SeasonStats.objects.filter(
            player_id__exact=player.id, 
            season_year__exact=season.season_year
        )
        today = datetime.now()
        
        is_current_season = (
            season.season_year == today.year or
            (
                season.season_year == (today.year - 1) and 
                today.date() < my_settings.SEASON_OPENER
            )
        )

        if not existing or existing and is_current_season:
            season.save()
            seasons_added += 1

    return seasons_added


def import_stats():
    players = Player.objects.all()
    seasons_added = 0

    for player in players:
        seasons_added = gather_player_stats(player, seasons_added)

    logger.info({
        'msg': 'Stats gathering complete!',
        'num_seasons_added': seasons_added
    })


def add_stats_gatherer_parser(subparsers):
    stat_gatherer_parser = subparsers.add_parser(
        'stat-gatherer',
        help='Gathers a list of all stats in the NBA'
    )
    stat_gatherer_parser.set_defaults(func=import_stats)
