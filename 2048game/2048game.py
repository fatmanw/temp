#!/usr/bin/env python
#encoding:utf8

import curses
from random import randrange, choice
import time
from collections import defaultdict


letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
actions = ['up', 'left', 'down', 'right', 'Restart', 'Exit']
actions_dict = dict(zip(letter_codes, actions * 2))


class GameField(object):
    '''Game object supporting close methods'''
    def __init__(self, width=4, height=4, win_value=2048):
        self.width = width
        self.height = height
        self.win_value = win_value
        self.score = 0
        self.best_score = 0
        self.reset()

    def spawn(self):
        '''random create element'''
        new_element = 4 if randrange(100)>89 else 2
        (i,j) = choice([(i,j) for i in range(self.width) \
            for j in range(self.height) \
            if self.field[i][j]==0])
        self.field[i][j] = new_element

    def reset(self):
        '''init game's score and field'''
        self.best_score = max(self.score, self.best_score)
        self.score = 0
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()

    def draw(self, screen):
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '     (R)Restart (Q)Exit'
        gameover_string = '           GAME OVER'
        win_string = '          YOU WIN!'
        def cast(string):
            screen.addstr(string + '\n')

        def draw_hor_separator():
            line = '+' + ('+------' * self.width + '+')[1:]
            separator = defaultdict(lambda: line)
            if not hasattr(draw_hor_separator, "counter"):
                draw_hor_separator.counter = 0
            cast(separator[draw_hor_separator.counter])
            draw_hor_separator.counter += 1

        def draw_row(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

        screen.clear()
        cast('SCORE: ' + str(self.score))
        if 0 != self.best_score:
            cast('HGHSCORE: ' + str(self.best_score))
        for row in self.field:
            draw_hor_separator()
            draw_row(row)
        draw_hor_separator()
        if self.is_win():
            cast(win_string)
        else:
            if self.is_gameover():
                cast(gameover_string)
            else:
                cast(help_string1)
        cast(help_string2)

    def transpose(self,field):
        return [list(row) for row in zip(*field)]

    def invert(self,field):
        return [row[::-1] for row in field]

    def move(self, direction):
        '''return field list after moving'''
        def move_left_row(row):
            def tighten(row):
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row)-len(new_row))]
                return new_row

            def merge(row):
                merge_sign = False
                new_row = []
                for i in range(len(row)):
                    if merge_sign:
                        new_row.append(row[i]*2)
                        self.score += row[i]*2
                        merge_sign = False
                    else:
                        if i+1 < len(row) and row[i] == row[i+1]:
                            merge_sign = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                return new_row

            return tighten(merge(tighten(row)))

        moves = {}
        moves['left'] = lambda field: \
            [move_left_row(row) for row in field]
        moves['right'] = lambda field: \
            self.invert(moves['left'](self.invert(field)))
        moves['up'] = lambda field: \
            self.transpose(moves['left'](self.transpose(field)))
        moves['down'] = lambda field: \
            self.transpose(moves['right'](self.transpose(field)))

        if direction in moves:
            if self.is_move_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False

    def is_win(self):
        #return any([0 for i in self.width for j in self.height if self.field[i][j]<=self.win_value])
        return any(any(i==self.win_value for i in row) for row in self.field)

    def is_move_possible(self, direction):
        def is_left_movable_row(row):
            def chance(i):
                if row[i]==0 and row[i+1]!=0:
                    return True
                if row[i]!=0 and row[i+1]==row[i]:
                    return True
                return False
            return any(chance(i) for i in range(len(row)-1))

        check = {}
        check['left'] = lambda field: \
            any(is_left_movable_row(row) for row in field)
        check['right'] = lambda field: \
            check['left'](self.invert(field))
        check['up'] = lambda field: \
            check['left'](self.transpose(field))
        check['down'] = lambda field: \
            check['right'](self.transpose(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False

    def is_gameover(self):
        #return not any(is_move_possible(move) for move in self.move.moves.key())
        return not any(self.is_move_possible(move) \
            for move in ['up','down','left','right'])


def get_user_action(keyboard):    
    char = "N"
    while char not in actions_dict:    
        char = keyboard.getch()
    return actions_dict[char]

def main(stdscr):
    def init():
        #重置游戏棋盘
        game_field.reset()
        return 'Game'

    def not_game(state):
        #画出 GameOver 或者 Win 的界面
        game_field.draw(stdscr)
        #读取用户输入得到action，判断是重启游戏还是结束游戏
        action = get_user_action(stdscr)
        responses = defaultdict(lambda: state) #默认是当前状态，没有行为就会一直在当前界面循环
        responses['Restart'], responses['Exit'] = 'Init', 'Exit' #对应不同的行为转换到不同的状态
        return responses[action]

    def game():
        #画出当前棋盘状态
        game_field.draw(stdscr)
        #读取用户输入得到action
        action = get_user_action(stdscr)

        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action): # move successful
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'

    state_actions = {
            'Init': init,
            'Win': lambda: not_game('Win'),
            'Gameover': lambda: not_game('Gameover'),
            'Game': game
        }

    curses.use_default_colors()
    game_field = GameField()

    state = 'Init'

    #状态机开始循环
    while state != 'Exit':
        state = state_actions[state]()

if __name__ == '__main__':
    curses.wrapper(main)