from datetime import date
from decimal import getcontext, Decimal

from django.db import models


getcontext().prec = 3

divisions = { u'MIL': 'Central', u'GSW': 'Pacific', u'MIN': 'Northwest', u'MIA': 'Southeast', u'ATL': 'Southeast', u'BOS': 'Atlantic', u'DET': 'Central', u'NYK': 'Atlantic', u'DEN': 'Northwest', u'SAC': 'Pacific', u'POR': 'Northwest', u'ORL': 'Southeast', u'TOR': 'Atlantic', u'CLE': 'Central', u'SAS': 'Southwest', u'CHO': 'Southeast', u'UTA': 'Northwest', u'CHI': 'Central', u'HOU': 'Southwest', u'NOP': 'Southwest', u'WAS': 'Southeast', u'LAL': 'Pacific', u'PHI': 'Atlantic', u'PHO': 'Pacific', u'MEM': 'Southwest', u'LAC': 'Pacific', u'DAL': 'Southwest', u'OKC': 'Northwest', u'BRK': 'Atlantic', u'IND': 'Central' }

cities = { 'LAL': 'Los Angeles', 'LAC': 'Los Angeles', 'GSW': 'Golden State', 'SAC': 'Sacramento', 'OKC': 'Oklahoma City', 'DAL': 'Dallas', 'MIL': 'Milwaukee', 'UTA': 'Utah', 'MIN': 'Minnesota', 'SAS': 'San Antonio', 'CLE': 'Cleveland', 'CHO': 'Charlotte', 'NOP': 'New Orleans', 'TOR': 'Toronto', 'WAS': 'Washington DC', 'CHI': 'Chicago', 'ORL': 'Orlando', 'MIA': 'Miami', 'DET': 'Detroit', 'PHO': 'Phoenix', 'DEN': 'Denver', 'ATL': 'Atlanta', 'BRK': 'Brooklyn', 'HOU': 'Houston', 'IND': 'Indianapolis', 'NYK': 'New York City', 'BOS': 'Boston', 'PHI': 'Philadelphia', 'POR': 'Portland', 'MEM': 'Memphis' }

NAME_CHOICES = ( (u'LAL', u'Lakers'), (u'LAC', u'Clippers'), (u'GSW', u'Warriors'), (u'SAC', u'Kings'), (u'OKC', u'Thunder'), (u'DAL', u'Mavericks'), (u'MIL', u'Bucks'), (u'UTA', u'Jazz'), (u'MIN', u'Timberwolves'), (u'SAS', u'Spurs'), (u'CLE', u'Cavaliers'), (u'CHO', u'Hornets'), (u'NOP', u'Pelicans'), (u'TOR', u'Raptors'), (u'WAS', u'Wizards'), (u'CHI', u'Bulls'), (u'ORL', u'Magic'), (u'MIA', u'Heat'), (u'DET', u'Pistons'), (u'PHO', u'Suns'), (u'DEN', u'Nuggets'), (u'ATL', u'Hawks'), (u'BRK', u'Nets'), (u'HOU', u'Rockets'), (u'IND', u'Pacers'), (u'NYK', u'Knicks'), (u'BOS', u'Celtics'), (u'PHI', u'76ers'), (u'POR', u'Trail Blazers'), (u'MEM', u'Grizzlies'), )

POSITION_CHOICES = (
    (u'PG', u'Point Guard'),
    (u'SG', u'Shooting Guard'),
    (u'SF', u'Small Forward'),
    (u'PF', u'Power Forward'),
    (u'C', u'Center'),
    (u'G', u'Guard'),
    (u'F', u'Forward'),
    (u'GF', u'Guard-Forward'),
    (u'FC', u'Forward-Center'),
)


class Division(models.Model):
    """ NBA conference division """
    name = models.CharField(max_length=30)
    conference = models.CharField(choices=[
        ('E', 'East'), ('W', 'West')
    ], max_length=1)

class Team(models.Model):
    """ A simple model to represent NBA teams and their win/loss record.
    """
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=3)
    city = models.CharField(max_length=30)
    division = models.ForeignKey(Division, on_delete=None, related_name='teams')
    wins = models.IntegerField(blank=True)
    losses = models.IntegerField(blank=True)

    @property
    def win_loss_percentage(self):
        try:
            return Decimal(self.wins) / (
                Decimal(self.wins) + Decimal(self.losses)
            )
        except ZeroDivisionError:
            return 0

    def __unicode__(self):
        return self.name


class Player(models.Model):
    """ Represents an NBA player, with basic info like date of birth and
    position.
    """

    current_team = models.ForeignKey(Team, related_name='current_players')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(blank=True, null=True)
    pos = models.CharField(blank=True, null=True,
                           max_length=2, choices=POSITION_CHOICES)

    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def age(self):
        """ Returns the player's age based on date of birth (dob) """
        today = date.today()
        try:
            return today.year - self.dob.year - \
                ((today.month, today.day) < (self.dob.month, self.dob.day))
        except AttributeError:
            return None

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('last_name', 'first_name')


class SeasonStats(models.Model):
    """ Represents a set of stats over a season for an individual
    player.

    player - the player to which these stats belong
    team - the team the player played for while accumulating these stats
    start - the start date for these stats
    end - the end date for these stats
    playoffs - boolean; true if these are playoff stats; false if reg
        season.
    """
    # Relational info
    player = models.ForeignKey(Player, related_name='season_stats')
    team = models.ForeignKey(Team, related_name='season_stats')
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    playoffs = models.BooleanField(default=False)
    # Stats
    gp = models.IntegerField(blank=True, null=True)  # games played
    mp = models.IntegerField(blank=True, null=True)  # minutes played
    fg = models.IntegerField(blank=True, null=True)  # field goals made
    fga = models.IntegerField(blank=True, null=True)  # field goals attempted
    ft = models.IntegerField(blank=True, null=True)  # free throws made
    fta = models.IntegerField(blank=True, null=True)  # free throws attempted
    three_pointers = models.IntegerField(blank=True, null=True)  # threes made
    threes_attempted = models.IntegerField(blank=True, null=True)
    orb = models.IntegerField(blank=True, null=True)  # offensive rebounds
    drb = models.IntegerField(blank=True, null=True)  # defensive rebounds
    ast = models.IntegerField(blank=True, null=True)  # assists
    stl = models.IntegerField(blank=True, null=True)  # steals
    blk = models.IntegerField(blank=True, null=True)  # blocks
    tov = models.IntegerField(blank=True, null=True)  # turnovers
    pf = models.IntegerField(blank=True, null=True)  # personal fouls
    pts = models.IntegerField(blank=True, null=True)  # points

    @property
    def trb(self):
        return self.orb + self.drb

    # Calculated stats (per game and per 36 minutes)
    def fgp(self):
        """ Field goal percentage """
        try:
            return Decimal(self.fg) / Decimal(self.fga)
        except ZeroDivisionError:
            return 0

    def ftp(self):
        """ Free throw percentage """
        try:
            return Decimal(self.ft) / Decimal(self.fta)
        except ZeroDivisionError:
            return 0

    def three_pp(self):
        """ Three pointer percentage """
        try:
            return Decimal(self.three_pointers) / Decimal(self.threes_attempted)
        except ZeroDivisionError:
            return 0

    def per_game(self, stat):
        """ Return the raw stat calculated on a per-game basis """
        try:
            return Decimal(getattr(self, stat)) / Decimal(self.gp)
        except ZeroDivisionError:
            return 0

    def per_36(self, stat):
        """ Return the raw stat calculated on a per-thirty-six-minute 
        basis. 
        """
        try:
            return 36 * (
                Decimal(getattr(self, stat)) / Decimal(self.mp)
            )
        except ZeroDivisionError:
            return 0

    class Meta:
        ordering = ('player__last_name', 'player__first_name', 'start')
