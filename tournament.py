#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

# NOTES

# More than one tournament is supported.

# DRAW MATCHES
# DRAW matches are considered lost for both opponents
# ReportMatch has an optional argument to record DRAW matches

# PAIRINGS
# Opponents are sorted and paired by total wins and OMW 
# (Opponent Match Wins, the total number of wins by players they have played against)
# Opponents might play against each other more than once in a tournament
# Player Standings has an optional argument to extract from DB the OMW value

# BYE
# If the number of players in a tournament is an odd number, each round one of the players is on BYE (randomly picked)
# A BYE is considered as a won match. 
# A player can be on a BYE once per tournament.


import psycopg2


def connect():
    # Connect to the PostgreSQL database.  Returns a database connection.
    return psycopg2.connect("dbname=tournament")

def deleteMatches(id_tournament):
    #Remove all the match records for tournament #id_tournament from the database.
    DB = connect()
    cur = DB.cursor()
    cur.execute('DELETE FROM single_match WHERE id_tournament = (%s)', [id_tournament])
    DB.commit()
    DB.close()

def deletePlayers(id_tournament):
    #Remove all the player records for tournament #id_tournament from the database.
    DB = connect()
    cur = DB.cursor()
    cur.execute('DELETE FROM player WHERE currentTournament = (%s)', [id_tournament])
    DB.commit()
    DB.close()

def countPlayers(id_tournament):
    #Returns the number of players currently registered for tournament #id_tournament.
    DB = connect()
    cur = DB.cursor()
    cur.execute('SELECT COUNT(*) FROM player WHERE currentTournament = (%s)', [id_tournament])
    count = cur.fetchone()
    DB.close()
    return count[0]

def registerTournament(name):
    """Adds a tournament to the database.
    Args:
      name: the tournament name (need not be unique).
    """
    DB = connect()
    cur = DB.cursor()
    cur.execute('insert INTO tournament(name) VALUES (%s) RETURNING id', [name])
    DB.commit()
    tournament_id = cur.fetchone()[0]
    DB.close()
    return tournament_id

def registerPlayer(name, id_tournament):
    """Adds a player to the tournament database. Sets its current tournament to #id_tournament
    Args:
      name: the player's full name (need not be unique).
      id_tournament: the player's current tournament
    """
    DB = connect()
    cur = DB.cursor()
    cur.execute('insert INTO player(username, currentTournament) VALUES (%s, %s)', [name, id_tournament])
    DB.commit()
    DB.close()

def playerStandings(id_tournament, omw = False):
    """Returns a list of the players and their win records, sorted by wins /omw. 
    If optional parameter omw is set to True, returns in addition omw column.
    """
    DB = connect()
    cur = DB.cursor()
    if omw:
        cur.execute('SELECT id, username, total_win, total_matches, omw FROM player_standings WHERE currentTournament = (%s)', [id_tournament])
    else:
        cur.execute('SELECT id, username, total_win, total_matches FROM player_standings WHERE currentTournament = (%s)', [id_tournament])
    
    playerStandings = cur.fetchall()
    DB.commit()
    DB.close()
    return playerStandings

def reportMatch(winnerORdraw, loserORdraw, id_tournament, draw = False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won or draw
      loser:  the id number of the player who lost or draw
      id_tournament: the match current tournament
      draw: optional argument to record a draw match
    """
    DB = connect()
    cur = DB.cursor()

    # set player1 as the player with lowest id. Match result parameter will be calculated accordingly.
    player1 = min(winnerORdraw, loserORdraw)
    player2 = max(winnerORdraw, loserORdraw)

    # calculate match result
    match_result = '4' if draw else '3' if player2 == '' else '1' if player1==winnerORdraw else '2'

    # save match in db
    if(match_result == '3'):
        cur.execute('insert INTO single_match(id_tournament, id_player1, mresult) VALUES (%s, %s, %s)', [id_tournament, player1, match_result])
    else:
        cur.execute('insert INTO single_match(id_tournament, id_player1, id_player2, mresult) VALUES (%s, %s, %s, %s)', [id_tournament, player1, player2, match_result])
    DB.commit()
    DB.close()

def swissPairings(id_tournament):
    """Returns a list of pairs of players for the next round of a match.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    
    DB = connect()
    cur = DB.cursor()
    bye = False if countPlayers(id_tournament) % 2 == 0 else True
    if bye:
        # select random player who's gonna skip the turn and register the BYE 
        cur.execute('SELECT id, username, bye FROM player_standings WHERE currentTournament = (%s) AND bye = 0 ORDER BY RANDOM()', [id_tournament])
        playerBye = cur.fetchone()
        reportMatch(playerBye[0], '', id_tournament, False)
        print playerBye[1] + ' on BYE'

        # select all remaining players to swiss pair them
        cur.execute('SELECT id, username FROM player_standings WHERE currentTournament = (%s) AND id <> (%s)', [id_tournament, playerBye[0]])
        playerStandingsNoBye = cur.fetchall()
    else:
        # select all players to swiss pair them
        cur.execute('SELECT id, username FROM player_standings WHERE currentTournament = (%s)', [id_tournament])
        playerStandingsNoBye = cur.fetchall()
 
    DB.close()

    i = 0
    swissPairings = []
    match_num = len(playerStandingsNoBye) / 2
    while i < match_num:
        player1 = playerStandingsNoBye.pop(0)
        player2 = playerStandingsNoBye.pop(0)
        swissPairings.append([player1[0], player1[1] , player2[0], player2[1]])      
        i = i + 1
    
    return swissPairings
        
    

