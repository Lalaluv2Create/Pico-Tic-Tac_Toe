# Tic-Tac_Toe - Embedded Game

## About
- This is a Tic-Tac-Toe game I made for my CS 390 Embedded Systems class
- It uses a Raspberry Pi Pico and MicroPython to create an interactive game controlled by an infrared (IR) remote
- The game displays the board, menus, and game results on a small OLED screen

## Features
- Play Tic-Tac-Toe using an IR remote
- Navigate the main menu using the remote
- Chooce between a 3x3 and 4x4 game board
- Move around the board and place X and O marks
- Detect winning moves and ties
- Keep track of each player's wins, losses, and ties
- Reset player records through the settings menu
- Return to the main menu after a game ends

## Components Used
- Raspberry Pi Pico
- Infrared (IR) receiver
- IR remote control
- 128x32 SPI OLED display
- Breadboard and jumper wires

## Pin Connections
- | Component | Pico GPIO Pin |
- | IR Receiver | GP15 |
- | OLED Chip Select (CS) | GP20 |
- | OLED Reset (RST) | GP17 |
- | OLED Data/Command (DC) | GP16 |
- | OLED Clock (CLK) | GP18 |
- |OLED Data (DATA/MOSI) | GP19 |

## How to Use
1. Connect the Raspberry Pi Pico to your computer
2. Open main.py in Thonny or another MicroPython-compatible editor
3. Make sure the required libraries are saved on the Pico
4. Run the program on the Pico
5. Use the IR remote to navigate the main menu
6. Select Start New Game to begin playing
7. Move around the board and press the select button to place your mark
8. The game displays the winner or a tie when the game ends
9. Press the Select button to return to the main menu
10. Select See Records to view player statistics or Settings to change the board size and reset records

## IR Remote Controls
- Up: Move the selection up
- Down: Move the selection down
- Left: Move the selection left
- Right: Move the selection right
- Enter/Save: Select a menu option or place a mark
- Stop/Mode: End the current game and return to the main menu

## Files
- main.py: Main Tic-Tac-Toe game program
- ir_receiver_lib.py: IR receiver library
- Hardware Setup.pdf: hardware setup and wiring instructions
- User Guide.pdf: Instructions for playing the game

## What I Learned
- How to use an IR remote to control an embedded system
- How to connect and communicate with an SPI OLED display
- How to create interactive menus using MicroPython
- How to use functions, lists, loops, and conditional statements to organize a program
- How to implement Tic-Tac-Toe game logic and detect winning moves
- How to keep track of player records
- How to work with GPIO pins and external hardware components

## Future Improvements
- Save player records so they remain available after restarting the Pico
- Add more board sizes and game options
- Improve the display layout and game interface
- Add support for more players

