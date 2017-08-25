""" Single point of entry for running workers in the nba_stats app """
import argparse
import logging
from logging import config as logging_config

import django
from django.conf import settings
from nba_stats import settings as my_settings


settings.configure(
    DATABASES=my_settings.DATABASES,
    INSTALLED_APPS=('players.apps.PlayersConfig', )
)
django.setup()

logger = logging.getLogger('workers')
logging_config.dictConfig(my_settings.LOGGING)


if __name__ == '__main__':
    from scripts.player_gatherer import add_player_gatherer_parser
    from scripts.stats_gatherer import add_stats_gatherer_parser
    from scripts.team_gatherer import add_team_gatherer_parser

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    add_team_gatherer_parser(subparsers)
    add_player_gatherer_parser(subparsers)
    add_stats_gatherer_parser(subparsers)
    
    args = parser.parse_args()

    args.func()
