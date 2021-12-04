# -*- coding: utf-8 -*-

import numpy as np


"""
# Field
field_len = 6
start_filling = 3
field = np.zeros((2, field_len)).astype(int) + start_filling
# Goals
goals = np.zeros(2).astype(int)
# Player
player = 0
"""
def start_minimax(field, goals, player, sp=1, md=3):
    moves = find_moves(field, player)
    moves = quick_eval(field, moves, player)
    move_vals = np.zeros(len(moves))
    ab=[-np.inf, np.inf]
    for cm, m in enumerate(moves):
        undo_inf = apply_move(field, goals, player, m)
        if undo_inf[5] == 1:
            move_vals[cm] = max_s(field, goals, player, d=1, ab=ab[:2], sp=sp, md=md)
        else:
            move_vals[cm] = min_s(field, goals, (player+1)%2, d=1, ab=ab[:2], sp=sp, md=md)
        undo_move(field, goals, player, undo_inf)
        if move_vals[cm] > ab[0]:
            ab[0] = move_vals[cm]
        if move_vals[cm] > ab[1]:
            return move_vals[cm]
    max_val = np.max(move_vals)
    max_moves = np.where(move_vals == max_val)[0]
    rand_max_move = np.random.choice(max_moves, 1)[0]
    return moves[rand_max_move], max_val
    

def min_s(field, goals, player, d, ab, sp, md):
    if d==md:
        return sp*evaluate(goals)
    if np.sum(field[player]) == 0:
        if goals[player] - goals[(player+1)%2] > 0:
            if d==1:
                return -9999
            return -999
        elif goals[player] - goals[(player+1)%2] < 0:
            if d==1:
                return 9999
            return 999
        else:
            return 0
    moves = find_moves(field, player)
    moves = quick_eval(field, moves, player)
    move_vals = np.zeros(len(moves))
    for cm, m in enumerate(moves):
        undo_inf = apply_move(field, goals, player, m)
        if undo_inf[5] == 1:
            move_vals[cm] = min_s(field, goals, player, d=d+1, ab=ab[:2], sp=sp, md=md)
        else:
            move_vals[cm] = max_s(field, goals, (player+1)%2, d=d+1, ab=ab[:2], sp=sp, md=md)
        undo_move(field, goals, player, undo_inf)
        if move_vals[cm] < ab[1]:
            ab[1] = move_vals[cm]
        if move_vals[cm] < ab[0]:
            return move_vals[cm]
    return np.min(move_vals)


def max_s(field, goals, player, d, ab, sp, md):
    if d==md:
        return sp*evaluate(goals)
    if np.sum(field[player]) == 0:
        if goals[player] - goals[(player+1)%2] > 0:
            if d==1:
                return 9999
            return 999
        elif goals[player] - goals[(player+1)%2] < 0:
            if d==1:
                return -9999
            return -999
        else:
            return 0
    moves = find_moves(field, player)
    moves = quick_eval(field, moves, player)
    move_vals = np.zeros(len(moves))
    for cm, m in enumerate(moves):
        undo_inf = apply_move(field, goals, player, m)
        if undo_inf[5] == 1:
            move_vals[cm] = max_s(field, goals, player, d=d+1, ab=ab[:2], sp=sp, md=md)
        else:
            move_vals[cm] = min_s(field, goals, (player+1)%2, d=d+1, ab=ab[:2], sp=sp, md=md)
        undo_move(field, goals, player, undo_inf)
        if move_vals[cm] > ab[0]:
            ab[0] = move_vals[cm]
        if move_vals[cm] > ab[1]:
            return move_vals[cm]
    return np.max(move_vals)


def evaluate(goals):
    return goals[0] - goals[1]
    

def apply_move(field, goals, player, move):
    to_distrib = field[player, move]
    n = len(field[0])
    to_all = int(to_distrib // (2*n + 1))
    rest = int(to_distrib % (2*n + 1))
    field[player, move] = 0
    field += to_all
    goals[player] += to_all
    undo_info = np.zeros(6).astype(int) - 1
    undo_info[:2] = np.array([move, to_distrib])
    row_to_check = -1
    fin_p = -1
    ended_in_goal = 0
    if player == 0:
        if rest <= move:
            field[0][move-rest:move] += 1
            row_to_check = move - rest
            fin_p = 0
        elif rest == move + 1:
            field[0][:move] += 1
            goals[0] += 1
            row_to_check = -1
            fin_p = -1
            ended_in_goal = 1
        elif rest <= move + 1 + n:
            field[0][:move] += 1
            goals[0] += 1
            field[1][:rest-move-1] += 1
            row_to_check = rest - move - 2
            fin_p = 1
        else:
            field[0][:move] += 1
            goals[0] += 1
            field[1] += 1
            field[0][move + 1 + n - rest:] += 1
            row_to_check = move + 1 + 2*n - rest
            fin_p = 0
        if row_to_check != -1 and fin_p == 0 and field[0][row_to_check] == 1:
            if field[1][row_to_check] >= 1:
                goals[0] += field[0][row_to_check] + field[1][row_to_check]
                undo_info[3] = field[0][row_to_check]
                undo_info[4] = field[1][row_to_check]
                field[:, row_to_check] = 0
                undo_info[2] = row_to_check
            else:
                undo_info[2] = -1
        else:
            undo_info[2] = -1
    else:
        if rest <= n - move - 1:
            field[1][move+1:move+rest+1] += 1
            row_to_check = move + rest
            fin_p = 1
        elif rest == n - move:
            field[1][move+1:] += 1
            goals[1] += 1
            row_to_check = -1
            fin_p = -1
            ended_in_goal = 1
        elif rest <= 2 * n - move:
            field[1][move+1:] += 1
            goals[1] += 1
            field[0][n - move - rest:] += 1
            row_to_check = 2*n - move - rest
            fin_p = 0
        else:
            field[1][move+1:] += 1
            goals[1] += 1
            field[0] += 1
            field[1][:rest-n-(n-move)] += 1
            row_to_check = rest-n-(n-move)-1
            fin_p = 1
        if row_to_check != -1 and fin_p == 1 and field[1][row_to_check] == 1:
            if field[0][row_to_check] >= 1:
                goals[1] += field[0][row_to_check] + field[1][row_to_check]
                undo_info[3] = field[1][row_to_check]
                undo_info[4] = field[0][row_to_check]
                field[:, row_to_check] = 0
                undo_info[2] = row_to_check
            else:
                undo_info[2] = -1
        else:
            undo_info[2] = -1
    undo_info[5] = ended_in_goal
    return undo_info
        

def undo_move(field, goals, player, undo_info):
    # Undo_info: [move, to_distrib, row_to_check, own_m, op_m, extra_move]
    n = len(field[0])
    from_all = undo_info[1] // (2*n + 1)
    rest = undo_info[1] % (2*n + 1)
    if undo_info[2] != -1:
        field[player][undo_info[2]] += undo_info[3]
        field[(player+1)%2][undo_info[2]] += undo_info[4]
        goals[player] -= (undo_info[3] + undo_info[4])
    field -= from_all
    m = undo_info[0]
    goals[player] -= from_all
    if player == 0:
        if rest <= m:
            field[0][m-rest:m] -= 1
        elif rest == m + 1:
            field[0][:m] -= 1
            goals[0] -= 1
        elif rest <= m + 1 + n:
            field[0][:m] -= 1
            goals[0] -= 1
            field[1][:rest-m-1] -= 1
        else:
            field[0][:m] -= 1
            goals[0] -= 1
            field[1] -= 1
            field[0][m + 1 + n - rest:] -= 1
    else:
        if rest <= n - m - 1:
            field[1][m+1:m+rest+1] -= 1
        elif rest == n - m:
            field[1][m+1:] -= 1
            goals[1] -= 1
        elif rest <= 2 * n - m:
            field[1][m+1:] -= 1
            goals[1] -= 1
            field[0][n - m - rest:] -= 1
        else:
            field[1][m+1:] -= 1
            goals[1] -= 1
            field[0] -= 1
            field[1][:rest-n-(n-m)] -= 1
    field[player, m] = undo_info[1]
    return


def quick_eval(field, moves, player):
    return moves[np.argsort(field[player, moves])[::-1]]
    
    
def find_moves(field, player):
    moves = np.where(field[player] != 0)[0]
    return np.array(moves)
