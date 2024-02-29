## Setup
# Modules
from main import app, cur

# Constantes
corr = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}

## Request
# Get the Board game
@app.get('/room/{room_name}/board')
def get_board(room_name: str):
    cur.execute(f"SELECT `zero`, `one`, `two`, `three`, `four`, `five`, `six`, `seven`, `eight` FROM `morpion-board` WHERE `name` = '{room_name}'")
    board = [(ze, on, tw, th, fo, fi, si, se, ei) for ze, on, tw, th, fo, fi, si, se, ei in cur][0]
    
    result = win(board)
    if result != None:
        return result
    
    return board

# Modify a box
@app.post('/room/{room_name}/board/{token}/{case}')
def place(room_name: str, token: str, case: int):
    cur.execute(f"SELECT player1, player2, turn from `morpion-board` WHERE `name` = '{room_name}'")
    player = [(p1, p2, turn) for p1, p2, turn in cur][0]
    
    connection = 0
    
    if player[0] == token:
        connection = 1
    elif player[1] == token:
        connection = 2
    else:
        return {"error": "token or room doesn't exist"}
    
    cur.execute(f"SELECT `zero`, `one`, `two`, `three`, `four`, `five`, `six`, `seven`, `eight` FROM `morpion-board` WHERE `name` = '{room_name}'")
    board = [(ze, on, tw, th, fo, fi, si, se, ei) for ze, on, tw, th, fo, fi, si, se, ei in cur][0]
    
    if board[case] != "":
        return {"error": "Already an item in the box"}
    
    elif (player[2] == "X") and (connection == 1):
        cur.execute(f"UPDATE `morpion-board` SET `{corr[case]}` = '{player[2]}' WHERE `morpion-board`.`name` = '{room_name}'")
        cur.execute(f"UPDATE `morpion-board` SET `turn` = 'O' WHERE `morpion-board`.`name` = '{room_name}'")
        
        return {"Success": f"player1, you have put a 'X' in the case number {case}"}
    
    elif (player[2] == "O") and (connection == 2):
        cur.execute(f"UPDATE `morpion-board` SET `{corr[case]}` = '{player[2]}' WHERE `morpion-board`.`name` = '{room_name}'")
        cur.execute(f"UPDATE `morpion-board` SET `turn` = 'X' WHERE `morpion-board`.`name` = '{room_name}'")
        
        return {"Success": f"player2, you have put a 'O' in the case number {case}"}
    
    return {"error": "It's not your turn"}

# Win ?
def win(board: list):
    board = [[board[0], board[1], board[2]], [board[3], board[4], board[5]], [board[6], board[7], board[8]]]
    
    # Horizontal
    for i in range(3):
        if (board[i][0] == "X") and (board[i][1] == "X") and (board[i][2] == "X"):
            return "X win"
        
        if (board[i][0] == "O") and (board[i][1] == "O") and (board[i][2] == "O"):
            return "O win"
    
    # Vertical
    for i in range(3):
        if (board[0][i] == "X") and (board[1][i] == "X") and (board[2][i] == "X"):
            return "X win"
        
        if (board[0][i] == "O") and (board[1][i] == "O") and (board[2][i] == "O"):
            return "O win"
    
    # Diagonal
    if (board[0][0] == "X") and (board[1][1] == "X") and (board[2][2] == "X"):
        return "X win"

    if (board[0][0] == "O") and (board[1][1] == "O") and (board[2][2] == "O"):
        return "O win"

    if (board[0][2] == "X") and (board[1][1] == "X") and (board[2][0] == "X"):
        return "X win"

    if (board[0][2] == "O") and (board[1][1] == "O") and (board[2][0] == "O"):
        return "O win"