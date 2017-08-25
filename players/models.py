from datetime import date
from decimal import getcontext, Decimal

from django.db import models


getcontext().prec = 3

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
    wins = models.IntegerField(blank=True, null=True, default=0)
    losses = models.IntegerField(blank=True, null=True, default=0)
    api_id = models.CharField(max_length=30)

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
    height_feet = models.IntegerField(null=True)
    height_inches = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    years_pro = models.IntegerField(null=True)
    api_id = models.CharField(max_length=30, default='')

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
    season_year = models.CharField(max_length=4)
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
        ordering = ('player__last_name', 'player__first_name', 'season_year')
