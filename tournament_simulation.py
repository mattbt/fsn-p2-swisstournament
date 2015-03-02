# tournament simulation for tournament.py

from tournament import *
import time
from random import randint
import math

def nextRound(idt):
        # swiss pair opponents
        print '\nRound ' + str(round_num) + ' matches:\n'
        pairing = swissPairings(idt)
        for p in pairing:
                print str(p[1]) + ' vs ' + str(p[3])
        time.sleep(1)

        # play matches
        print '\nRound ' + str(round_num) + ' scores:\n'
        for m in pairing:
                playMatch(m[0], m[1], m[2], m[3], idt)
                
        time.sleep(1)
        
def playMatch(id1, name1, id2, name2, idt):
        # play whatever the game
        # here winner is the one with higher random number
        score1 = randint(1,7)
        score2 = randint(1,7)
        print str(name1) + ' vs ' + str(name2) + '\t ' + str(score1) + ' - ' + str(score2)

        # register match result to DB
        if score1 > score2:
                reportMatch(id1, id2, idt)
        elif score1 < score2:
                reportMatch(id2, id1, idt)
        elif score1 == score2:
                reportMatch(id1, id2, idt, True) # DRAW    

def printStandings(idt, round_num):
        print '\n### Round ' + str(round_num) + ' standings:\n'
        
        #get and print standings with omw (optional argument True)
        st = playerStandings(idt, True)
        print 'id\t|username\t|total_win\t|total_matches\t|omw\t|'
        for pl in st:
                print str(pl[0]) + '\t|' + str(pl[1]) + '\t|' +str(pl[2]) + '\t\t|' +str(pl[3]) + '\t\t|' +str(pl[4]) + '\t|'

def registerPlayers(idt, players_num):
        # register fake players for tournament idt
        print '\nRegistering ' + str(players_num) + ' players'
        p = 1
        while p <= players_num:
                registerPlayer('player' + str(p), idt)
                p = p + 1
        time.sleep(1)


if __name__ == '__main__':
        #create tournament
        idt = registerTournament('Tournament Simulation from script')
        print '\nTournament Simulation from script - #' + str(idt) + ' just started!'
        time.sleep(1)

        # get a random num of players between 4 and 15
        players_num = randint(4,15)

        # fake players registration
        registerPlayers(idt, players_num)

        # calculate total round number
        round_total = math.ceil(math.log(players_num, 2))
        print 'Number of rounds: ' + str(int(round_total))

        # tournament simulation
        round_num = 1
        while round_num <= round_total:
                raw_input('\n### Press Enter to simulate round ' + str(round_num) + '!\n')
                nextRound(idt)    
                printStandings(idt, round_num)
                round_num = round_num + 1

        # get the winner
        st = playerStandings(idt)
        print '\n#####\t' + str(st[0][1]) + ' is the champion!\n\n'
        
