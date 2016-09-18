#!/usr/bin/python
# coding=utf-8

# import peewee as pw
# from iso3166 import countries
# from playhouse.shortcuts import model_to_dict, dict_to_model
# import connection

# # from catcher.models import MySQLModel

# db = connection.connect_database()

# # -------------------------------------------------------------------------------------
# class MySQLModel(pw.Model):
#     """A base model that will use our MySQL database"""

#     def __str__(self):
#         return str(model_to_dict(self))

#     class Meta:
#         database = db
# -------------------------------------------------------------------------------------
# class Division(MySQLModel):
#     division = pw.CharField()


# -------------------------------------------------------------------------------------
# class Club(MySQLModel):
#     # id       = pw.PrimaryKeyField()
#     user     = pw.IntegerField(db_column='user_id')
#     caldId   = pw.IntegerField(db_column='cald_id')
#     name     = pw.CharField()
#     shortcut = pw.FixedCharField(max_length=3)
#     city     = pw.CharField()
#     country  = CountryCode(max_length=3)
# # -------------------------------------------------------------------------------------
# # Placeholder for the through model 
# # DeferredClubHasPlayer = DeferredThroughModel()
# # -------------------------------------------------------------------------------------
# class Player(MySQLModel):
#     firstname = pw.CharField()
#     lastname  = pw.CharField()
#     nickname  = pw.CharField()
#     number    = pw.IntegerField()
#     ranking   = pw.FloatField()
#     caldId    = pw.IntegerField(db_column='cald_id')
#     clubId    = pw.IntegerField(db_column='club_id')
#     # clubs     = ManyToManyField(Club, through_model=DeferredClubHasPlayer)
# # -------------------------------------------------------------------------------------
# # class ClubHasPlayer(MySQLModel):
# #     club         = pw.ForeignKeyField(Club)
# #     player       = pw.ForeignKeyField(Player)
# #     caldRelation = pw.BooleanField(db_column='cald_relation')

# #     primary_key = pw.CompositeKey('club', 'player') 
# #         db_table = 'club_has_player'
# #         indexes = (
# #             (('cald_relation', 'player'), True),
# #         )
# # -------------------------------------------------------------------------------------
# # DeferredClubHasPlayer.set_model(ClubHasPlayer)
# # -------------------------------------------------------------------------------------
# class Division(MySQLModel):
#     id = pw.PrimaryKeyField()
#     division = pw.CharField()
# # -------------------------------------------------------------------------------------
# class Team(MySQLModel):
#     clubId     = pw.IntegerField(db_column='club_id')
#     divisionId = pw.IntegerField(db_column='division_id')
#     degree     = pw.FixedCharField(max_length=1)
#     # # TODO: invent, how to remove dependency with db column
#     # name       = pw.CharField(db_column='degree')

#     # def prepared(self):
#     #     self.name = self.club.name + " " + self.degree
# # -------------------------------------------------------------------------------------
# class CaldTournament(MySQLModel):
#     id    = pw.PrimaryKeyField()
#     name  = pw.CharField()
#     place = pw.CharField()
#     date  = pw.DateTimeField()

#     class Meta:
#         db_table = 'cald_tournament'
# # -------------------------------------------------------------------------------------
# class Tournament(MySQLModel):
#     caldTournamentId = pw.IntegerField(db_column='cald_tournament_id')
#     city             = pw.CharField()
#     country          = CountryCode()
#     divisionId       = pw.IntegerField(db_column='division_id')
#     name             = pw.CharField()
#     startDate        = pw.DateTimeField(db_column='start_date')
#     endDate          = pw.DateTimeField(db_column='end_date')
#     teams            = pw.IntegerField()
#     ready            = pw.BooleanField()
#     terminated       = pw.BooleanField()
#     userId           = pw.IntegerField(db_column='user_id')
# # -------------------------------------------------------------------------------------
# class Field(MySQLModel):
#     id         = pw.IntegerField()
#     name       = pw.CharField()
#     tournament = pw.ForeignKeyField(Tournament)

#     class Meta:
#         indexes = (
#             (('id', 'tournament'), True),
#             (('name', 'tournament'), True),
#         )
#         # Nemuzu pouzivat, protoze bych jinak nemohl vytvaret nove zaznamy
#         # primary_key = pw.CompositeKey('id', 'tournament')
# # -------------------------------------------------------------------------------------
# class TeamAtTournament(MySQLModel):
#     seeding      = pw.IntegerField()
#     teamId       = pw.IntegerField(db_column='team_id')
#     tournamentId = pw.IntegerField(db_column='tournament_id')

#     class Meta:
#         db_table = 'team_at_tournament'
#         primary_key = False
#         # indexes = (
#         #     (('tournament', 'team'), True),
#         # )
#         # primary_key = pw.CompositeKey('team', 'tournament')

#     # def prepared(self):
#         # self.json = {
#         #     "teamId"    : self.team_id,
#         #     "name"      : (self.team.club.name + " " + self.team.degree),
#         #     "degree"    : self.team.degree,
#         #     "divisionId": self.team.division_id,
#         #     "seeding"   : self.seeding,
#         #     "clubId"    : self.team.club_id
#         #     }

# # ------------------------------------------------------------------------------------- 
# class Identificator(MySQLModel):
#     ide           = pw.CharField(max_length=3)
#     tournamentId  = pw.IntegerField(db_column='tournament_id')
#     matchId       = pw.IntegerField(db_column='match_id')
#     # groupId       = pw.IntegerField(db_column='group_id')

#     class Meta:
#         # primary_key = False
#         # Nemuzu pouzivat, protoze bych jinak nemohl vytvaret nove zaznamy
#         primary_key = pw.CompositeKey('ide', 'tournamentId')
# # ------------------------------------------------------------------------------------- 
# class Match(MySQLModel):
#     # id                  = pw.IntegerField()
#     fieldId             = pw.IntegerField(db_column='field_id')
#     description         = pw.CharField()
#     startTime           = pw.DateTimeField(db_column = 'start_time')
#     endTime             = pw.DateTimeField(db_column = 'end_time')
#     tournamentId        = pw.IntegerField(db_column='tournament_id')
#     terminated          = pw.BooleanField()
#     looserFinalStanding = pw.IntegerField(db_column = 'looser_final_standing')
#     winnerFinalStanding = pw.IntegerField(db_column = 'winner_final_standing')
#     ide                 = pw.CharField()
#     looserNextStepIde   = pw.CharField(db_column='looser_next_step_ide')
#     winnerNextStepIde   = pw.CharField(db_column='winner_next_step_ide')
#     homeSeed            = pw.IntegerField(db_column = 'home_seed')
#     awaySeed            = pw.IntegerField(db_column = 'away_seed')
#     flip                = pw.BooleanField()
#     awayScore           = pw.IntegerField(db_column = 'away_score')
#     homeScore           = pw.IntegerField(db_column = 'home_score')
#     spiritAway          = pw.IntegerField(db_column = 'spirit_away')
#     spiritHome          = pw.IntegerField(db_column = 'spirit_home')
#     awayTeamId          = pw.IntegerField(db_column='away_team_id')
#     homeTeamId          = pw.IntegerField(db_column='home_team_id')
#     active              = pw.BooleanField()
#     groupIde            = pw.CharField(db_column = 'group_ide')

#     # class Meta:
#     #     primary_key = pw.CompositeKey('ide', 'tournamentId')
# # -------------------------------------------------------------------------------------
# class Standing(MySQLModel):
#     standing     = pw.IntegerField()
#     teamId       = pw.IntegerField(db_column = 'team_id')
#     tournamentId = pw.IntegerField(db_column = 'tournament_id')
#     json         = None

#     class Meta:
#         # pass
#         # indexes = (
#         #     (('tournament', 'team', 'standing'), True),
#         # )
#         primary_key = False
#         # pw.CompositeKey('standing', 'team', 'tournament')

#     def prepared(self):
#         self.json = {
#             "standing": self.standing,
#             "teamId"  : self.teamId
#         }
# # -------------------------------------------------------------------------------------
# class PlayerAtTournament(MySQLModel):
#     assists      = pw.IntegerField(default=0)
#     matches      = pw.IntegerField(default=0)
#     scores       = pw.IntegerField(default=0)
#     total        = pw.IntegerField(default=0)
#     playerId     = pw.IntegerField(db_column='player_id')
#     teamId       = pw.IntegerField(db_column='team_id')
#     tournamentId = pw.IntegerField(db_column='tournament_id')
#     json         = None

#     class Meta:
#         db_table = 'player_at_tournament'
#         primary_key = False
#     #     primary_key = pw.CompositeKey('playerId', 'teamId', 'tournamentId')

#     # def prepared(self):
#     #     self.json = {
#     #         "assists"     : self.assists,
#     #         "matches"     : self.matches,
#     #         "scores"      : self.scores,
#     #         "total"       : self.total,
#     #         "playerId"    : self.playerId,
#     #         "teamId"      : self.teamId, 
#     #         "tournamentId": self.tournamentId
#     #         }
# # -------------------------------------------------------------------------------------
# class PlayerAtMatch(MySQLModel):
#     assists    = pw.IntegerField()
#     matchId    = pw.IntegerField(db_column='match_id')
#     playerId   = pw.IntegerField(db_column='player_id')
#     scores     = pw.IntegerField()
#     total      = pw.IntegerField()
    
#     class Meta:
#         primary_key = False
#         db_table = 'player_at_match'
# # -------------------------------------------------------------------------------------
# class Point(MySQLModel):
#     homePoint      = pw.BooleanField(db_column='home_point')
#     matchId        = pw.IntegerField(db_column='match_id')
#     order          = pw.IntegerField()
#     assistPlayerId = pw.IntegerField(db_column='assist_player_id')
#     scorePlayerId  = pw.IntegerField(db_column='score_player_id')
#     awayScore      = pw.IntegerField(db_column='away_score')
#     homeScore      = pw.IntegerField(db_column='home_score')
#     callahan       = pw.BooleanField()

#     class Meta:
#         primary_key = False
# # -------------------------------------------------------------------------------------
# class Spirit(MySQLModel):
#     matchId         = pw.IntegerField(db_column='match_id')
#     teamId          = pw.IntegerField(db_column='team_id')
#     givingTeamId    = pw.IntegerField(db_column='giving_team_id')
#     communication   = pw.IntegerField()
#     fair            = pw.IntegerField()
#     fouls           = pw.IntegerField()
#     positive        = pw.IntegerField()
#     rules           = pw.IntegerField()
#     total           = pw.IntegerField()
#     comment         = pw.CharField()

#     class Meta:
#         # primary_key = False
#         primary_key = pw.CompositeKey('matchId', 'teamId') 
# # -------------------------------------------------------------------------------------
# class SpiritAvg(MySQLModel):
#     teamId             = pw.IntegerField(db_column='team_id')
#     tournamentId       = pw.IntegerField(db_column='tournament_id')
#     matches            = pw.IntegerField()
#     matchesGiven       = pw.IntegerField(db_column='matches_given')
#     communication      = pw.FloatField()
#     communicationGiven = pw.FloatField(db_column='communication_given')
#     fair               = pw.FloatField()
#     fairGiven          = pw.FloatField(db_column='fair_given')
#     fouls              = pw.FloatField()
#     foulsGiven         = pw.FloatField(db_column='fouls_given')
#     positive           = pw.FloatField()
#     positiveGiven      = pw.FloatField(db_column='positive_given')
#     rules              = pw.FloatField()
#     rulesGiven         = pw.FloatField(db_column='rules_given')
#     total              = pw.FloatField()
#     totalGiven         = pw.FloatField(db_column='total_given')

#     class Meta:
#         primary_key = pw.CompositeKey('teamId', 'tournamentId') 
#         db_table = 'spirit_avg'
# # -------------------------------------------------------------------------------------
# class Group(MySQLModel):
#     tournamentId  = pw.IntegerField(db_column='tournament_id')
#     ide           = pw.CharField()
#     teams         = pw.IntegerField()
#     description   = pw.CharField()

#     class Meta:
#         primary_key = pw.CompositeKey('tournamentId', 'ide')
# # -------------------------------------------------------------------------------------
# class Advancement(MySQLModel):
#     tournamentId  = pw.IntegerField(db_column='tournament_id')
#     ide           = pw.CharField()
#     standing      = pw.IntegerField()
#     finalStanding = pw.IntegerField(db_column='final_standing')
#     nextStepIde   = pw.CharField(db_column='next_step_ide')
    
#     class Meta:
#         primary_key = pw.CompositeKey('group', 'standing')
# # -------------------------------------------------------------------------------------
# class GroupHasTeam(MySQLModel):
#     tournamentId = pw.IntegerField(db_column='tournament_id')
#     ide          = pw.CharField()
#     teamId       = pw.IntegerField(db_column='team_id')
#     matches      = pw.IntegerField()
#     wins         = pw.IntegerField()
#     losses       = pw.IntegerField()
#     plus         = pw.IntegerField()
#     minus        = pw.IntegerField()
#     points       = pw.IntegerField()
#     standing     = pw.IntegerField()

#     class Meta:
#         db_table = 'group_has_team'
#         primary_key = pw.CompositeKey('tournamentId', 'ide', 'teamId')