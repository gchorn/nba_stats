from datetime import datetime
import logging
from time import sleep

from marshmallow import fields, post_load, Schema
import requests

from players.models import Player, Team

logger = logging.getLogger(__name__)

PLAYER_URL = ("http://data.nba.net/10s/prod/v1/2016/players.json")

REQUEST_ARGS = dict(
    headers={'Content-Type': 'application/json'},
    timeout=300
)

teams = Team.objects.all()
TEAM_MAP = {team.api_id: team.id for team in teams}


class PlayersSchema(Schema):
    first_name = fields.Str(load_from='firstName')
    last_name = fields.Str(load_from='lastName')
    pos = fields.Str()
    dob = fields.Method(load_from='dateOfBirthUTC', deserialize='load_date')
    height_feet = fields.Method(load_from='heightFeet', deserialize='cast_int')
    height_inches = fields.Method(load_from='heightInches', deserialize='cast_int')
    weight = fields.Method(load_from='weightPounds', deserialize='cast_int')
    years_pro = fields.Method(load_from='yearsPro', deserialize='cast_int')
    current_team_id = fields.Method(load_from='teamId', deserialize='team_lookup')
    api_id = fields.String(load_from='personId')

    def load_date(self, value):
        return datetime.strptime(value, "%Y-%m-%d").date()

    def team_lookup(self, value):
        return TEAM_MAP[
            value.split()[0]
        ]

    def cast_int(self, value):
        return int(value)

    @post_load
    def create_player(self, data):
        return Player(**data)


def import_players():
    player_schema = PlayersSchema(many=True, strict=True)
    
    player_request = requests.get(PLAYER_URL, REQUEST_ARGS)

    player_data = player_request.json()['league']['standard']
    nba_players = [player for player in player_data if player['nbaDebutYear']]

    players = player_schema.load(nba_players).data

    players_added = 0
    for player in players:
        existing_player = Player.objects.filter(first_name__exact=player.first_name, last_name__exact=player.last_name)
        if not existing_player:
            player.save()
            players_added += 1
        else:
            logger.debug({
                'msg': '{} {} already exists in the database'.format(player.first_name, player.last_name)
            })

    logger.info({
        'msg': 'Successfully imported players!',
        'num_added': players_added
    })


def add_player_gatherer_parser(subparsers):
    player_gatherer_parser = subparsers.add_parser(
        'player-gatherer',
        help='Gathers a list of all players in the NBA'
    )
    player_gatherer_parser.set_defaults(func=import_players)
