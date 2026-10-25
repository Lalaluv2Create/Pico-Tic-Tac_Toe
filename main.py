#Lauren Boykins
#Project 3: Tic-Tac-Toe
#Due 10-22-26

import time
from machine import Pin, SPI
from ir_receiver_lib import IRReceiver
import ssd1306 # install this module with thonny's package control

# IR remote receiver setup
IR_PIN_NUM = 15
ir_pin = Pin(IR_PIN_NUM, Pin.IN)

#Screen setup:
# Maps physical connections to variables
CS_PIN_NUM = 20
RST_PIN_NUM = 17
DC_PIN_NUM = 16
CLK_PIN_NUM = 18
DATA_PIN_NUM = 19

# Create the SPI connection
spi = SPI(
    0,
    baudrate=10_000_000,
    sck=Pin(CLK_PIN_NUM),
    mosi=Pin(DATA_PIN_NUM)
)

# Set up screen control pins
dc = Pin(DC_PIN_NUM, Pin.OUT)
rst = Pin(RST_PIN_NUM, Pin.OUT)
cs = Pin(CS_PIN_NUM, Pin.OUT)

# Initialize the 128x32 OLED screen
display = ssd1306.SSD1306_SPI(
    128, 32, spi, dc, rst, cs
)


# Store the most recent remote command
last_cmd = None
last_time = 0
repeat_cooldown = 500

# Receive commands from the remote
def ir_callback(new_cmd):
    global last_cmd, last_time

    now = time.ticks_ms()

    # A nonnegative command is a new button press
    if new_cmd >= 0:
        last_cmd = new_cmd
        last_time = now

    # Handle a held-button repeat
    elif new_cmd == -1 and last_cmd is not None:
        if time.ticks_diff(now, last_time) < repeat_cooldown:
            return

        last_time = now

# Start the receiver
receiver = IRReceiver(ir_pin, callback=ir_callback)

#Tic-Tac-Toe Game:

# 1.) Main Menu:
menu_options = [
    "Start New Game ",
    "See Records ",
    "Settings "
    ]

#remembers which menu option is selcected, 0 for first option selected
selected_option = 0
#store the settings menu options
settings_options = ["3x3 Board", "4x4 Board",
                    "Reset Records", "Back"]
settings_selected = 0
settings_active = False

#Make the menu appear on the OLED screen
def display_menu():
    #clear anything that was previously shown on the screen
    display.fill(0)
    
    #Display the tictactoe at the top of the screen
    display.text("Tic-Tac-Toe", 0, 0, 1)
    
    #Show each menu choice on its own line
    for i in range(len(menu_options)):
        #Add an arrow beside the currently selected choice
        if i == selected_option:
            marker = ">"
        else:
            marker = " "
            
        #since OLED text uses x and y coordinates
        #the y coordinates to move each choice down the screen
        display.text(marker + menu_options[i], 0, 8 + i * 8, 1)
        
    #Send the drawing to the screen
    display.show()

#display_settings to user
def display_settings():
    display.fill(0)

    if settings_selected == 0:
        display.text(">3x3 Board", 0, 0, 1)
    else:
        display.text("  3x3 Board", 0, 0, 1)

    if settings_selected == 1:
        display.text(">4x4 Board", 0, 8, 1)
    else:
        display.text("  4x4 Board", 0, 8, 1)

    if settings_selected == 2:
        display.text(">Reset Records", 0, 16, 1)
    else:
        display.text("  Reset Records", 0, 16, 1)

    if settings_selected == 3:
        display.text(">Back", 0, 24, 1)
    else:
        display.text("  Back", 0, 24, 1)

    display.show()
    
#helper to help with all the setting info
def handle_settings_input(command):
    global settings_selected
    global grid_rows, grid_columns, winning_length
    global player_x_wins, player_x_losses, player_x_ties
    global player_o_wins, player_o_losses, player_o_ties
    global settings_active, selected_option
    
    if command == BUTTON_UP:
        settings_selected = (settings_selected - 1) % len(settings_options)
    
    elif command == BUTTON_DOWN:
        settings_selected = (settings_selected + 1) % len(settings_options)
        
    elif command == BUTTON_SELECT:
        if settings_selected == 0:
            grid_rows = 3
            grid_columns = 3
            winning_length = 3
            
        elif settings_selected == 1:
            grid_rows = 4
            grid_columns = 4
            winning_length = 3
        
        elif settings_selected == 2:
            player_x_wins = 0
            player_x_losses = 0
            player_x_ties = 0
            player_o_wins = 0
            player_o_losses = 0
            player_o_ties = 0
            
        elif settings_selected == 3:
            settings_active = False
            selected_option = 0
            display_menu()
            return
        
    display_settings()
        
#button numbers
BUTTON_UP = 64
BUTTON_DOWN = 25
BUTTON_SELECT = 21
BUTTON_LEFT = 7
BUTTON_RIGHT = 9
BUTTON_STOP = 67

#Check whether a menu button was pressed
def handled_menu_input():
    global selected_option, last_cmd
    
    #save the latest command so we can process it once
    command = last_cmd
    last_cmd = None
    
    #If no button press is waiting, do nothing
    if command is None:
        return None
    
    #Move the selection up through the menu
    if command == BUTTON_UP:
        selected_option = (selected_option - 1) % len(menu_options)
        display_menu()
       
    #Move the selection down through the menu
    elif command == BUTTON_DOWN:
        selected_option = (selected_option + 1) % len(menu_options)
        display_menu()
    
    #Return the selected menu choice when Select is pressed
    elif command == BUTTON_SELECT:
         return menu_options[selected_option].strip()
    
    #No menu choice was selected
    return None
         
#store the grid size
grid_rows = 3
grid_columns = 3

#store the winning condition
winning_length = 3

# store each player's wins, losses, and ties
# wins:
player_x_wins = 0
player_o_wins = 0

# losses:
player_x_losses = 0
player_o_losses = 0

# ties for each player:
player_x_ties = 0
player_o_ties = 0

#Store the game board
board = []

#Store whose turn it is
current_player = "X"

#Store which square is selected
selected_row = 0
selected_column = 0
# Remember whether a game is currently active
game_active = False


# Create an empty board using the selected grid size
def create_board():
    board = []

    for row in range(grid_rows):
        board_row = []

        for column in range(grid_columns):
            board_row.append(" ")

        board.append(board_row)

    return board


# Display the game on the screen
def display_board():
    
    # Clear the screen
    display.fill(0)

    # Leave room on the right for the current player
    board_width = 96
    board_height = 32

    # Draw the vertical grid lines
    for column in range(grid_columns):
        x = column * board_width // grid_columns
        display.line(x, 0, x, 31, 1)

    display.line(95, 0, 95, 31, 1)

    # Draw the horizontal grid lines
    for row in range(grid_rows):
        y = row * board_height // grid_rows
        display.line(0, y, 95, y, 1)

    display.line(0, 31, 95, 31, 1)

    # Display each square's contents
    for row in range(grid_rows):
        for column in range(grid_columns):
            cell_x = column * board_width // grid_columns
            cell_y = row * board_height // grid_rows

            if row == selected_row and column == selected_column:
                marker = ">"
            else:
                marker = " "

            cell_text = marker + board[row][column]

            display.text(cell_text, cell_x + 4, cell_y, 1)

    # Show whose turn it is
    display.text("Turn", 96, 0, 1)
    display.text(current_player, 112, 8, 1)

    display.show()

# Display the winner or a tie
# Check for a tie after checking for a winner
def check_winner():
    # Check every square as a possible starting point
    for row in range(grid_rows):
        for column in range(grid_columns):

            # Empty squares cannot start a winning line
            player = board[row][column]
            if player == " ":
                continue

            # Check horizontal, vertical, and both diagonals
            directions = [
                (0, 1),
                (1, 0),
                (1, 1),
                (1, -1)
            ]

            for row_step, column_step in directions:
                count = 0

                # Check the required number of squares in this direction
                for step in range(winning_length):
                    check_row = row + row_step * step
                    check_column = column + column_step * step

                    # Stop if the line would go outside the board
                    if (check_row < 0 or check_row >= grid_rows or
                        check_column < 0 or check_column >= grid_columns):
                        break

                    # Stop if a square does not belong to this player
                    if board[check_row][check_column] != player:
                        break

                    count += 1

                # The player wins if enough matching squares were found
                if count == winning_length:
                    return player

    # No winner was found
    return None


# Check whether every square on the board is filled
def board_is_full():
    for row in range(grid_rows):
        for column in range(grid_columns):
            if board[row][column] == " ":
                return False

    return True


# 4.)Display results and return to the menu
def display_results(result):
    global game_active, selected_option
    global player_x_wins, player_o_wins
    global player_x_losses, player_o_losses
    global player_x_ties, player_o_ties
    global last_cmd

    # Clear the screen before showing the result
    display.fill(0)

    if result == "X":
        # Update both players' records
        player_x_wins += 1
        player_o_losses += 1
        display.text("Player X wins!", 0, 0, 1)
    elif result == "O":
        # Update both players' records
        player_o_wins += 1
        player_x_losses += 1
        display.text("Player O wins!", 0, 0, 1)
    else:
        # A tie counts for both players
        player_x_ties += 1
        player_o_ties += 1
        display.text("It's a tie!", 0, 0, 1)

    # Show the updated screen
    display.text("Game Over! ", 0, 16, 1)
    display.text("Press OK to exit", 0, 24, 1)
    display.show()
    
    #Wait until the player presses Select or Stop
    while True:
        command = last_cmd
        last_cmd = None

        if command == BUTTON_SELECT or command == BUTTON_STOP:
            break

        time.sleep(0.05)

    # Return to the main menu
    game_active = False
    selected_option = 0
    display_menu()

# Handle remote input while playing a game
def handle_board_input(command):
    global selected_row, selected_column, current_player
    global game_active, selected_option

    #Stop the game and return to the main menu
    if command == BUTTON_STOP:
        game_active = False
        selected_option = 0
        display_menu()
        return
    
    # Move the selected square up
    if command == BUTTON_UP:
        selected_row = (selected_row - 1) % grid_rows

    # Move the selected square down
    elif command == BUTTON_DOWN:
        selected_row = (selected_row + 1) % grid_rows

    # Move the selected square left
    elif command == BUTTON_LEFT:
        selected_column = (selected_column - 1) % grid_columns

    # Move the selected square right
    elif command == BUTTON_RIGHT:
        selected_column = (selected_column + 1) % grid_columns

    # Place the current player's mark
    elif command == BUTTON_SELECT:
        # Only allow a move if the square is empty
        if board[selected_row][selected_column] == " ":
            board[selected_row][selected_column] = current_player

            # Check whether the move won the game
            winner = check_winner()

            if winner is not None:
                display_board()
                display_results(winner)
                return

            # Check whether the game ended in a tie
            if board_is_full():
                display_board()
                display_results("Tie")
                return

            # Switch players if the game is still going
            if current_player == "X":
                current_player = "O"
            else:
                current_player = "X"

    # Refresh the board after the move or cursor movement
    display_board()


# Show the main menu when the program starts
display_menu()

# Keep checking for remote button presses
while True:

    # If a game is active, send button presses to the game
    if game_active:
        # Save the latest command and clear it so it is used once
        command = last_cmd
        last_cmd = None

        # Only handle a button if one was received
        if command is not None:
            handle_board_input(command)
    
    #if the settings screen is actie, handle the settings buttons
    elif settings_active:
        command = last_cmd
        last_cmd = None
        
        if command is not None:
            handle_settings_input(command)
            
    else:
        # Otherwise, handle input for the main menu
        choice = handled_menu_input()

        # Check which menu option was selected
        if choice == "Start New Game":
            print("Starting a new game!")

            # Create a new empty board
            board = create_board()

            # Reset the starting player and cursor position
            current_player = "X"
            selected_row = 0
            selected_column = 0

            # Enter the game
            game_active = True

            # Display the new board
            display_board()

        elif choice == "See Records":
            #clear the screen before showing the records
            display.fill(0)
            
            #Show Player X's record
            display.text("X W: {} L: {} T: {}".format(player_x_wins, player_x_losses, player_x_ties), 0, 0, 1)
            
            #Show Player O's record
            display.text("O W: {} L: {} T: {}". format(player_o_wins, player_o_losses, player_o_ties), 0, 8, 1)
    
            display.text("Press OK to exit", 0, 24, 1)
        
            # Display the records on the screen
            display.show()
            
            # Wait for the player to leave the records screen
            while True:
                command = last_cmd
                last_cmd = None

                if command == BUTTON_SELECT or command == BUTTON_STOP:
                    break

                time.sleep(0.05)
            
            #return to the main menu once done
            display_menu()

        elif choice == "Settings":
            # Open the settings screen
            settings_selected = 0
            settings_active = True
            display_settings()

    # Pause briefly before checking the remote again
    time.sleep(0.05)
