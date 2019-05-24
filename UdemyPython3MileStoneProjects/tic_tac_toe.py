#board => dictionary , players are 2 sets to record positions, winning position - a set of  positions (8 positions)
# a-> a1 a2 a3
# b-> b1 b2 b3
# c-> c1 c2 c3 		
# test if play 1 wins -> is a subset of a winning condition, if not, call it draw
#play 1 = #, play2 = O

# construct the board dictionary
board = [[' ',' ',' '] for _ in range(3)]
play1=set()
play2=set()
someone_win=False

winning_sets={frozenset(['a1','a2','a3']),frozenset(['c1','c2','c3']),frozenset(['b1','b2','b3']),frozenset(['a1','b1','c1']),frozenset(['a2','b2','c2']),frozenset(['a3','b3','c3']),frozenset(['a1','b2','c3']),frozenset(['a3','b2','c1'])}
def check_win(playerset):
	for item in winning_sets:
		if item.issubset(playerset):
			return True
			break
		else:
			continue
	return False

def draw_board(board):
    boardstr=''
    for i in range(3):
        for j in range (3):
            boardstr+=str(board[i][j])+ '|'
        boardstr+='\n'
        boardstr+='-----'
        boardstr+='\n'
    print (boardstr)

def row_letter_translation(move):
	row_letter = move[0]
	#row=0
	if row_letter == 'a':
		row=0
	elif row_letter =='b':
		row=1
	else:
		row=2
	return row


def add_board(player,move):
	row=row_letter_translation(move)
	column=int(move[1])-1
	if player == 1:
		board[row][column]='X' 
	else:
		board[row][column]='O'
         
def check_validity(board,move):
	row=row_letter_translation(move)
	column=int(move[1])-1
	if board[row][column]==' ':
		return True
	else:
		print ("this position has already been taken, pick another one!")
		return False


while not(someone_win):
	play1_move=input("play1 - type in the position: ")
	if check_validity(board,play1_move):
		play1.add(play1_move)
		add_board(1,play1_move)
		draw_board(board)
		print('1',play1)
		if check_win(play1):
			print ("Congrats, play1, you win!")
			someone_win=True
			break
		else:
			play2_move=input("play2 - type in the position: ")
			if check_validity(board,play2_move):
				play2.add(play2_move)
				add_board(2,play2_move)
				draw_board(board)
				print('2',play2)
				if check_win(play2):
					print ("Congrats, play2, you win!")
					someone_win=True
					break
			else:
				continue
	else:
		continue


if not someone_win:
	print("both players: it's a draw")
