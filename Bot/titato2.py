"""
A fun answer to the question:
How would you determine if someone has won a game of tic-tac-toe on a board of any size?

Reference:
(https://www.glassdoor.com/Interview/How-would-you-determine-if-someone-has-won-a-game-of-tic-tac-toe-on-a-board-of-any-size-QTN_1104.htm)

Teine versioon lubab suvalistel mängijatel liituda. Ei järgi käikude järjekorda.

Compiler
Since no conditionals are needed to find the winner, the compiler no longer
needs to do branch prediction. (Still need to run benchmarks)
"""

import operator
from functools import reduce

def let2regi(letter, size):
    letter=letter.lower()
    if size >9:
        return letter.upper()
    if letter=='.':
        return ':black_large_square:'
    if letter in "abcdefghijklmnopqrstuvwxyz":
        return ':regional_indicator_'+letter+':'
    return letter
class tic_tac_toe(object):
    def __init__(self, size=3, win=None, players=2):
        self.size = size
        self.reset()
        self.players = players
        self.show = list('.ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        if win:
            wins = win
        else:
            wins = size
        self.wins = wins
        # positions_groups on see koht, kus genereeritakse võimalikud võidujadad.
        """
        self.positions_groups = (
            [[(x, y) for y in range(size)] for x in range(size)] + # horizontals
            [[(x, y) for x in range(size)] for y in range(size)] + # verticals
            [[(d, d) for d in range(size)]] + # diagonal from top-left to bottom-right
            [[(size-1-d, d) for d in range(size)]] # diagonal from top-right to bottom-left
            )
        #"""
        self.positions_groups = list()
        for d in range(size - wins + 1):
            for y in range(size):
                self.positions_groups.append([])
                for x in range(d, d + wins):
                    self.positions_groups[-1].append((y, x))  # horizontals

        for d in range(size - wins + 1):
            for x in range(size):
                self.positions_groups.append([])
                for y in range(d, d + wins):
                    self.positions_groups[-1].append((y, x))  # verticals ?
        for dx in range(size - wins + 1):
            for dy in range(size - wins + 1):
                self.positions_groups.append([])
                for x in range(wins):
                    self.positions_groups[-1].append((dx + x, dy + x))  # diagonal from top-left to bottom-right

        for dx in range(size - wins + 1):
            for dy in range(size - wins + 1):
                self.positions_groups.append([])
                for x in range(wins):
                    self.positions_groups[-1].append(
                        (-dx + size - 1 - x, dy + x))  # diagonal from top-right to bottom-left
        self.positions_groups = set(map(tuple, self.positions_groups))
        # """

    def reset(self):
        self.board = [[0] * self.size for _ in range(self.size)]

    def play(self, player, x, y):
        self.board[x][y] = player

    def play_x(self, x, y):
        self.board[x][y] = 1

    def play_o(self, x, y):
        self.board[x][y] = 2

    def check_win(self):
        """
        check_win returns:
            0 if no winners
            1 if x won
            2 if y won
        """
        winner = 0

        for positions in self.positions_groups:
            values = [self.board[x][y] for (x, y) in positions]
            winner |= reduce(operator.__and__, values, -1)

        return winner

    def view(self):
        for row in self.board:
            print(row)

    def view2(self):
        for row in self.board:
            print(''.join(list(map(lambda x: self.show[x], row))))


def test_all():
    # Testing check_win
    #
    # We just covering the basics, not full coverage
    # since there are (p+1)^(n*n) possible end states (not accounting for symmetry),
    # where p is the number of players, and n is the board_size

    board_size = 4
    no_win = 0
    x_win = 1
    y_win = 2
    game = tic_tac_toe(board_size)

    # Kuvab erinevaid võiduolukordi.
    """
    g2=tic_tac_toe(4)
    for arr in game.positions_groups:
        g2.reset()
        for (x,y) in arr:
            g2.play_x(x,y)
        g2.view2()
        print()
    """

    # Test Empty
    print(game.check_win() == no_win)

    # Test Horizontals
    for x in range(board_size):
        game.reset()
        [game.play_o(x, y) for y in range(board_size)]
        print(game.check_win() == y_win)
        game.reset()
        [game.play_x(x, y) for y in range(board_size)]
        print(game.check_win() == x_win)

    # Test Verticals
    for y in range(board_size):
        game.reset()
        [game.play_o(x, y) for x in range(board_size)]
        print(game.check_win() == y_win)

        game.reset()
        [game.play_x(x, y) for x in range(board_size)]
        print(game.check_win() == x_win)

    # Test Diagonal top-left to bottom-right
    game.reset()
    [game.play_o(n, n) for n in range(board_size)]
    print(game.check_win() == y_win)

    game.reset()
    [game.play_x(n, n) for n in range(board_size)]
    print(game.check_win() == x_win)

    # Test Diagonal top-right to bottom-left
    game.reset()
    [game.play_o(board_size - 1 - n, n) for n in range(board_size)]
    print(game.check_win() == y_win)

    game.reset()
    [game.play_x(board_size - 1 - n, n) for n in range(board_size)]
    print(game.check_win() == x_win)
    # Spot Check Cats Game
    game.reset()
    [game.play_x(x, y) for x in range(board_size - 1) for y in range(board_size - 1)]
    [game.play_o(n, n) for n in range(board_size)]
    game.play_x(0, 0)
    print(game.check_win() == no_win)


class game_warp:
    def __init__(self,into):  # into = käsutaja käivituskäsk
        s = ['?g']+list(into[1:])
        # Sisend on list argumentidega. alates ttt-st.
        # ?g new ttt suurus win oselejad...
        if len(s)<4:raise SyntaxError( 'Liiga vähe argumente')
        suurus = int(s[2])
        if suurus > 30 or suurus < 2:
            raise SyntaxError('Discordi piirangute tõttu on max väljaku suurus 30.')
        if s[3].isnumeric():
            win = max([min([int(s[3]), suurus]), 1])
            start = 4
        else:
            start = 3  # Start on index, mitmendalt positsioonilt hakkab mängijate nimekiri.
            win = suurus
        self.players=s[start:]
        # print(self.players)
        self.next=0
        self.game = tic_tac_toe(suurus, win, len(self.players))
        self.startup='Mäng läks käima, osalevad '+', '.join(self.players)+'.'
    def move(self, player, x,y):
        # Sisaldab ka käimisvõimaluse kontrolli.
        # def play(self, player, x, y):
        x=int(x)-1
        y=int(y)-1
        if player!=self.players[self.next]:
            return 'Hetkel on '+self.players[self.next]+' käik.', 0
        if self.game.board[x][y]==0:
            player=self.next+1
            self.next=player
            if self.next==len(self.players):
                self.next=0
            self.game.play(player,x,y)
            self.game.board[x][y] = player
            x=list(map(lambda x:let2regi(x,self.game.size), self.show2()))
            if self.game.size>9:
                x='```'+' '.join(x).replace('   ','\n')+'```'
            else:
                x=''.join(x).replace(' ','\n')
            out='\n'+x+''
            win=self.game.check_win()
            # print(self.game.check_win())
            if win:
                out+='\n'+self.players[self.game.check_win()-1]+'võitis.'
            elif 'black_large_square' not in out and '.' not in out:
                out+='\nViik!'
                win=True
            return out, win
        else:
            return 'See koht on juba kinni.', 0
    def show(self):
        return self.game.view2()
    
    def show2(self):
        return ' '.join(list(map(lambda row: ''.join(list(map(
            lambda x: self.game.show[x], row))), self.game.board)))
    @property
    def type(self):
        return 'TicTacToe `'+self.show2()+'`'
    @property
    def next_player(self):
        return self.players[self.next]

    @property
    def win(self):
        return self.game.check_win()
#  ?g new ttt 4 @test9#0460
g=game_warp('new ttt 4 @test9#0460'.split())
print(g.type)
