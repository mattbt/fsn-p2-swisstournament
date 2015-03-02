#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches(id_tournament):
    deleteMatches(id_tournament)
    print "1. Old matches can be deleted."


def testDelete(id_tournament):
    deleteMatches(id_tournament)
    deletePlayers(id_tournament)
    print "2. Player records can be deleted."


def testCount(id_tournament):
    deleteMatches(id_tournament)
    deletePlayers(id_tournament)
    c = countPlayers(id_tournament)
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."

def testRegisterTournament(name):
    return registerTournament(name)
    
def testRegister(id_tournament):
    deleteMatches(id_tournament)
    deletePlayers(id_tournament)
    registerPlayer("Chandra Nalaar", id_tournament)
    c = countPlayers(id_tournament)
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete(id_tournament):
    deleteMatches(id_tournament)
    deletePlayers(id_tournament)
    registerPlayer("Markov Chaney",id_tournament)
    registerPlayer("Joe Malik",id_tournament)
    registerPlayer("Mao Tsu-hsi",id_tournament)
    registerPlayer("Atlanta Hope",id_tournament)
    c = countPlayers(id_tournament)
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers(id_tournament)
    c = countPlayers(id_tournament)
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches(id_tournament):
    deleteMatches(id_tournament)
    deletePlayers(id_tournament)
    registerPlayer("Melpomene Murray",id_tournament)
    registerPlayer("Randy Schwartz",id_tournament)
    standings = playerStandings(id_tournament)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches(id_tournament):
    deleteMatches(id_tournament)
    deletePlayers(id_tournament)
    registerPlayer("Bruno Walton",id_tournament)
    registerPlayer("Boots O'Neal",id_tournament)
    registerPlayer("Cathy Burton",id_tournament)
    registerPlayer("Diane Grant",id_tournament)
    standings = playerStandings(id_tournament)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2,id_tournament)
    reportMatch(id3, id4,id_tournament)
    standings = playerStandings(id_tournament)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."

def testReportMatchesWithBye(id_tournament):
    deleteMatches(id_tournament)
    deletePlayers(id_tournament)
    registerPlayer("Bruno Walton",id_tournament)
    registerPlayer("Boots O'Neal",id_tournament)
    registerPlayer("Cathy Burton",id_tournament)
    registerPlayer("Diane Grant",id_tournament)
    registerPlayer("Bruce Bald",id_tournament)

    standings = playerStandings(id_tournament)
    [id1, id2, id3, id4, id5] = [row[0] for row in standings]
    reportMatch(id1, id2,id_tournament)
    reportMatch(id3, id4,id_tournament)
    reportMatch(id5, '', id_tournament) # register the first BYE
    
    standings = playerStandings(id_tournament)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3, id5) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings in tournament with BYE."

def testPairings(id_tournament):
    deleteMatches(id_tournament)
    deletePlayers(id_tournament)
    registerPlayer("Twilight Sparkle",id_tournament)
    registerPlayer("Fluttershy",id_tournament)
    registerPlayer("Applejack",id_tournament)
    registerPlayer("Pinkie Pie",id_tournament)
    standings = playerStandings(id_tournament)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2,id_tournament)
    reportMatch(id3, id4,id_tournament)
    pairings = swissPairings(id_tournament)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."

if __name__ == '__main__':
    id_tournament1 = testRegisterTournament('Spring 2015 Tournament')
    testDeleteMatches(id_tournament1)
    testDelete(id_tournament1)
    testCount(id_tournament1)
    testRegister(id_tournament1)
    testRegisterCountDelete(id_tournament1)
    testStandingsBeforeMatches(id_tournament1)
    testReportMatches(id_tournament1)
    testPairings(id_tournament1)

    print "Success!  All tests pass!"


