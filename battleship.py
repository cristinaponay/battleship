# Assignment #4
# Program 3 – Battleship
# Design and develop a program that replicates the functionality of the provided sample application, 
# a simple version of the game Battleship.
# Name..: Cristina Ponay
# ID....: W0424195

__AUTHOR__ = "Cristina Ponay <w0424195@nscc.ca>"
import math

# function that will draw the targeted map each time a valid target is entered
# will be repeatedly called in the application
def drawBoard(in_targetMap):
    letters = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
    header = "   "
    for letter in letters.keys():
        header += " | " + letter
    print("-"*(len(header)+2))
    print(header + " |")
    print("-"*(len(header)+2))
    rows = ""
    for i, line in enumerate(in_targetMap):
        if i == len(line)-1:
            rows += str(i+1) + " "
        else:
            rows += str(i+1) + "  "
        for j in line:
            rows += " | " + j
        rows += " |\n"
    print(rows, end="")
    print("-"*(len(header)+2))

def validate(in_targetPos):
    # user input validation flags
    validX, validY = False, False

    letters = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}

    if (len(in_targetPos) < 2 or len(in_targetPos) > 3) or not in_targetPos[0].isalpha() or not in_targetPos[1:].isnumeric():
        print("INVALID ENTRY: Please enter a letter and a number")
        return validX, validY, 0, 0
    # split user input  
    col = in_targetPos[0]
    row = int(in_targetPos[1:])
    
    if not row in range(1, 11):
        print("INVALID ENTRY: Number must be from 1 to 10.")
    else:
        row -= 1 # set row position
        validX = True
    if not col in letters.keys():
        print("INVALID ENTRY: Letter portion must be from A to J.")
        return validX, validY, 0, 0
    else:
        col = letters[col] # set column position
        validY = True
    return validX, validY, col, row

def fire(in_row, in_col, in_shipMap, in_targetMap, in_totalHits, in_targetHits):
    hit = int(in_shipMap[in_row][in_col])
    win = False
    if hit == 1:
        print("HIT!!!")
        in_targetMap[in_row][in_col] = "X"   # mark the hit on the target map
        in_totalHits += 1
        # when all the targets have been hit, end the game
        if in_totalHits == in_targetHits:
            drawBoard(in_targetMap)
            print("YOU SANK MY ENTIRE FLEET!")
            print(f"You had {in_totalHits} of {in_targetHits} hits, which sank all the ships.")
            print("You won, congratulations!")
            win = True
            return win, in_totalHits 
    else:
        print("You missed!")
        in_targetMap[in_row][in_col] = "O"   # mark the miss on the target map
    return win, in_totalHits

def main():
    # open target map from file
    try:
        mapFile = open("map.txt", "r")
    except FileNotFoundError:
        print("The file \"map.txt\" does not exist.")   # if file does not exist
    else:
        # initialization
        ship_map = [] # will store the ship map which is hidden from view
        missiles = 30   # number of trials
        target_hits = 0 # will store the number of targets in the map
        total_hits = 0  # number of hits by player
        hitlist = []    # list of target positions hit by player
        target_map = [
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "," "," "]
        ]   # the targeted map visible to player

        # read the map file per line
        for row in mapFile:
            row = row.replace("\n", "")
            rowAsList = row.split(",")
            # count the number of occurences of 1 in the list
            target_hits += rowAsList.count("1")
            ship_map.append(rowAsList) # append row to target grid

        drawBoard(target_map) # display game board in initial state

        # play until game over or player has won
        while True:
            validX, validY = False, False
            # will keep asking for input if invalid
            while not validX or not validY:
                target_pos = input("Choose your target (Ex. A10): ").upper()

                if target_pos == "X": # my key to quit game immediately
                    break

                validX, validY, col, row = validate(target_pos)
                # check if player is hitting the same target again
                if validX and validY:
                    target_pos = f"{col}{str(row)}" # in case user input is like A09, g01
                    if target_pos in hitlist:
                        print("You've already selected this target. Please choose another.")
                        validX, validY = False, False # reset value to repeat prompt
                    else:
                        hitlist.append(target_pos)
            
            if target_pos == "X": # my key quit game
                break
            missiles -= 1 # reduce missile count regardless of hit or miss
            # start firing missile
            win, total_hits = fire(row, col, ship_map, target_map, total_hits, target_hits)
            
            if win: # if player wins, end the game
                break 
            print(f"You have {missiles} missiles remaining.\n")
            
            # when all missiles have been used, end the game
            if missiles == 0:
                drawBoard(target_map)
                print("GAME OVER")
                print(f"You had {total_hits} of {target_hits} hits, but didn't sink all the ships.")
                print("Sorry, you ran out of missiles. Better luck next time.")
                break
            
            drawBoard(target_map)   # redraw the game board
    finally:
        mapFile.close()

if __name__ == "__main__":
    main()