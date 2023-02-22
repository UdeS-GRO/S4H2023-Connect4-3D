# Jacob Lambert, Februrary 22th 2023

#This function, for a given play, counts the number of pieces in a row for every orientation and returns a list of every streak
def streak_counter(play,board,row_total,column_total,floor_total):
    row_index = play[0]-1
    column_index = play[1]-1
    player_id = play[2]
    streak_list = []
    #This finds the floor postion where the piece can be placed
    for i in range(floor_total):
                if board[i][row_index][column_index] == 0:  
                    floor_index = i
                    break 
    #Row counter
    streak = 0
    for i in range(0,row_total):
        if i == row_index:
            streak = streak + 1
        elif board[floor_index][i][column_index]==player_id:
            streak = streak + 1
        elif board[floor_index][i][column_index]!=0:
            streak = 0
            break
    streak_list.append(streak)
    #Column counter
    streak = 0
    for i in range(0,column_total):
        if i == column_index:
            streak = streak + 1
        elif board[floor_index][row_index][i]==player_id:
            streak = streak + 1
        elif board[floor_index][row_index][i]!=0:
               streak = 0
               break
    streak_list.append(streak)                     
    #Floor counter
    streak = 0
    for i in range(0,floor_total):
        if i == floor_index:
            streak = streak + 1
        elif board[i][row_index][column_index]==player_id:
            streak = streak + 1
        elif board[i][row_index][column_index]!=0:
               streak = 0
               break
    streak_list.append(streak)              
    #Positive diagonal column and row counter
    streak = 0
    if row_index == column_index:
        for i in range(0,column_total):
            if i == column_index:
                streak = streak + 1
            elif board[floor_index][i][i]==player_id:
                streak = streak + 1
            elif board[floor_index][i][i]!=0:
                streak = 0
                break
        streak_list.append(streak)
    #Negative diagonal column and row counter
    streak = 0
    if (row_total-1)-row_index == column_index:
        for i in range(0,column_total):
            if i == column_index:
                streak = streak + 1
            elif board[floor_index][(row_total-1-i)][i]==player_id:
                streak = streak + 1
            elif board[floor_index][(row_total-1-i)][i]!=0:
                streak = 0
                break
        streak_list.append(streak)
    #Positive diagonal column and floor counter
    streak = 0
    gap = floor_index - row_index
    if row_index <= floor_index and gap <= floor_total-row_total:
        for i in range(0,row_total):
            if i == row_index:
                streak = streak + 1
            elif board[i+gap][i][column_index]==player_id:
                streak = streak + 1
            elif board[i+gap][i][column_index]!=0:
                    streak = 0
                    break
        streak_list.append(streak)
    #Negative diagonal column and floor counter
    streak = 0
    gap = floor_index - ((row_total-1)-row_index)
    if (row_total-1)-row_index <= floor_index and gap <= floor_total-row_total:
        for i in range(0,row_total):
            if i == row_index:
                streak = streak + 1
            elif board[(row_total-1-i)+gap][i][column_index]==player_id:
                streak = streak + 1
            elif board[(row_total-1-i)+gap][i][column_index]!=0:
                    streak = 0
                    break
        streak_list.append(streak)
    #Positive diagonal row and floor counter
    streak = 0
    gap = floor_index - column_index
    if column_index <= floor_index and gap <= floor_total-column_total:
        for i in range(0,column_total):
            if i == column_index:
                streak = streak + 1
            elif board[i+gap][row_index][i]==player_id:
                streak = streak + 1
            elif board[i+gap][row_index][i]!=0:
                    streak = 0
                    break
        streak_list.append(streak)
    #Negative diagonal row and floor counter
    streak = 0
    gap = floor_index - ((column_total-1)-column_index)
    if (column_total-1)-column_index <= floor_index and gap <= floor_total-column_total:
        for i in range(0,column_total):
            if i == column_index:
                streak = streak + 1
            elif board[(column_total-1-i)+gap][row_index][i]==player_id:
                streak = streak + 1
            elif board[(column_total-1-i)+gap][row_index][i]!=0:
                    streak = 0
                    break
        streak_list.append(streak)
    #Positive positive diagonal column, row and floor counter
    streak = 0
    gap = floor_index - row_index
    if row_index <= floor_index and gap <= floor_total-row_total:
        for i in range(0,row_total):
            if i == row_index:
                streak = streak + 1
            elif board[i+gap][i][i]==player_id:
                streak = streak + 1
            elif board[i+gap][i][i]!=0:
                    streak = 0
                    break
        streak_list.append(streak)
    #Positive negative diagonal column, row and floor counter
    streak = 0
    gap = floor_index - ((row_total-1)-row_index)
    if (row_total-1)-row_index <= floor_index and gap <= floor_total-row_total:
        for i in range(0,row_total):
            if i == row_index:
                streak = streak + 1
            elif board[(row_total-1-i)+gap][i][i]==player_id:
                streak = streak + 1
            elif board[(row_total-1-i)+gap][i][i]!=0:
                    streak = 0
                    break
        streak_list.append(streak)
    #Negative positive diagonal column, row and floor counter
    streak = 0
    gap = floor_index - column_index
    if column_index <= floor_index and gap <= floor_total-column_total:
        for i in range(0,column_total):
            if i == column_index:
                streak = streak + 1
            elif board[i+gap][i][i]==player_id:
                streak = streak + 1
            elif board[i+gap][i][i]!=0:
                    streak = 0
                    break
        streak_list.append(streak)
    #Negative negative diagonal column, row and floor counter
    streak = 0
    gap = floor_index - ((column_total-1)-column_index)
    if (column_total-1)-column_index <= floor_index and gap <= floor_total-column_total:
        for i in range(0,column_total):
            if i == column_index:
                streak = streak + 1
            elif board[(column_total-1-i)+gap][i][i]==player_id:
                streak = streak + 1
            elif board[(column_total-1-i)+gap][i][i]!=0:
                    streak = 0
                    break
        streak_list.append(streak)
    return streak_list