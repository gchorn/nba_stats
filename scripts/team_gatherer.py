from datetime import datetime
from time import sleep
import logging

from marshmallow import fields, post_load, pre_load, Schema
import requests

from players.models import Division, Team

logger = logging.getLogger(__name__)

PLAYER_URL = ("http://data.nba.net/10s/prod/v1/2016/teams.json")
REQUEST_ARGS = dict(
    headers={'Content-Type': 'application/json'},
    timeout=300
)


class TeamSchema(Schema):
    name = fields.String(load_from='nickname')
    short_name = fields.String(load_from='tricode')
    api_id = fields.String(load_from='teamId')
    city = fields.String()
    division = fields.Function(lambda d: d['division'])

    @pre_load
    def create_or_update_division(self, in_data):
        divisions = Division.objects.filter(name=in_data['divName'])
        if not divisions:
            division = Division(name=in_data['divName'],
                                conference=in_data['confName'])
            division.save()
        else:
            division = divisions[0]
        in_data['division'] = division
        return in_data

    @post_load
    def create_player(self, data):
        return Team(**data)


def import_teams():
    logger.info({
        'msg': 'Initializing team import'
    })

    self.team_schema = TeamSchema(many=True, strict=True)
    team_request = requests.get(PLAYER_URL, REQUEST_ARGS)

    team_data = team_request.json()['league']['standard']
    nba_teams = [team for team in team_data if team['isNBAFranchise']]

    teams = self.team_schema.load(nba_teams).data 

    teams_added = 0
    for team in teams:
        existing_team = Team.objects.filter(name__exact=team.name)
        if not existing_team:
            team.save()
            teams_added += 1

    logger.info({
        'msg': 'Successfully imported teams!',
        'num_added': teams_added
    })


def add_team_gatherer_parser(subparsers):
    team_gatherer_parser = subparsers.add_parser(
        'team-gatherer',
        help='Gathers a list of all teams in the NBA'
    )
    team_gatherer_parser.set_defaults(func=import_teams)
