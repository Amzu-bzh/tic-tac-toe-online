## Setup
# Modules
from uuid import uuid4

from main import app, cur

## Request
# Get rooms
@app.get('/room')
def get_room():
    cur.execute('SELECT name FROM `morpion-board-board`')
    room_list = [name for name in cur]
    print(room_list)
    
    return room_list

# Create room
@app.post('/room/{room_name}')
def create_room(room_name: str):
    cur.execute(f"INSERT INTO `morpion-board` (`name`, `player1`, `player2`, `turn`, `zero`, `one`, `two`, `three`, `four`, `five`, `six`, `seven`, `eight`) VALUES ('{room_name}', '', '', 'X', '', '', '', '', '', '', '', '', '');")
    return {"Succes": f"The room {room_name} has been created"}

# Deleate room
@app.delete('/room/{room_name}')
def deleate_room(room_name: str):
    cur.execute(f"DELETE FROM `morpion-board` WHERE `morpion-board`.`name` = '{room_name}'")
    return {"Succes": f"The room {room_name} has been deleated"}

# Join room
@app.post('/room/{room_name}/play')
def join_room(room_name: str):    
    cur.execute(f"SELECT player1, player2 from `morpion-board` WHERE `name` = '{room_name}'")
    
    token = uuid4()
    for p1, p2 in cur:
        if p1 == "":
            cur.execute(f"UPDATE `morpion-board` SET `player1` = '{token}' WHERE `morpion-board`.`name` = '{room_name}'")
            break
        elif p2 =="":
            cur.execute(f"UPDATE `morpion-board` SET `player2` = '{token}' WHERE `morpion-board`.`name` = '{room_name}'")
            break
        else:
            return {"error": "2 players in the room"}
    
    return {"token": token}

# Quit room
@app.put('/room/{room_name}/play/{token}')
def quit_room(room_name: str, token:str):
    cur.execute(f"SELECT player1, player2 from `morpion-board` WHERE `name` = '{room_name}'")
    player = [(p1, p2) for p1, p2 in cur][0]
    
    if player[0] == token:
        cur.execute(f"UPDATE `morpion-board` SET `player1` = '' WHERE `morpion-board`.`name` = '{room_name}'")
        
    elif player[1] == token:
        cur.execute(f"UPDATE `morpion-board` SET `player2` = '' WHERE `morpion-board`.`name` = '{room_name}'")
    
    else:
        return {"error": "token or room doesn't exist"}        
    
    return {"Success": "You left the room"}