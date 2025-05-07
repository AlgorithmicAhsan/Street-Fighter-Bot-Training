
import socket
import json
import sys
import keyboard  # You can install this via pip: pip install keyboard
from game_state import GameState
from bot import Bot
from command import Command
import pandas as pd

# Initialize an empty list globally to collect all frame data
frame_logs = []

def log_game_state_to_pandas(game_state: GameState, frame_number: int):
    global frame_logs

    frame_logs.append({
        "frame": frame_number,

        # Player 1
        "p1_id": game_state.player1.player_id,
        "p1_health": game_state.player1.health,
        "p1_x": game_state.player1.x_coord,
        "p1_y": game_state.player1.y_coord,
        "p1_jumping": game_state.player1.is_jumping,
        "p1_crouching": game_state.player1.is_crouching,
        "p1_in_move": game_state.player1.is_player_in_move,
        "p1_move_id": game_state.player1.move_id,

        # Player 1 buttons
        "p1_up": game_state.player1.player_buttons.up,
        "p1_down": game_state.player1.player_buttons.down,
        "p1_left": game_state.player1.player_buttons.left,
        "p1_right": game_state.player1.player_buttons.right,
        "p1_select": game_state.player1.player_buttons.select,
        "p1_start": game_state.player1.player_buttons.start,
        "p1_Y": game_state.player1.player_buttons.Y,
        "p1_B": game_state.player1.player_buttons.B,
        "p1_X": game_state.player1.player_buttons.X,
        "p1_A": game_state.player1.player_buttons.A,
        "p1_L": game_state.player1.player_buttons.L,
        "p1_R": game_state.player1.player_buttons.R,

        # Player 2
        "p2_id": game_state.player2.player_id,
        "p2_health": game_state.player2.health,
        "p2_x": game_state.player2.x_coord,
        "p2_y": game_state.player2.y_coord,
        "p2_jumping": game_state.player2.is_jumping,
        "p2_crouching": game_state.player2.is_crouching,
        "p2_in_move": game_state.player2.is_player_in_move,
        "p2_move_id": game_state.player2.move_id,

        # Player 2 buttons
        "p2_up": game_state.player2.player_buttons.up,
        "p2_down": game_state.player2.player_buttons.down,
        "p2_left": game_state.player2.player_buttons.left,
        "p2_right": game_state.player2.player_buttons.right,
        "p2_select": game_state.player2.player_buttons.select,
        "p2_start": game_state.player2.player_buttons.start,
        "p2_Y": game_state.player2.player_buttons.Y,
        "p2_B": game_state.player2.player_buttons.B,
        "p2_X": game_state.player2.player_buttons.X,
        "p2_A": game_state.player2.player_buttons.A,
        "p2_L": game_state.player2.player_buttons.L,
        "p2_R": game_state.player2.player_buttons.R,

        # Round info
        "timer": game_state.timer,
        "round_started": game_state.has_round_started,
        "round_over": game_state.is_round_over,
        "fight_result": game_state.fight_result
    })

def save_logs_to_csv(filename="game_log.csv"):
    global frame_logs
    df = pd.DataFrame(frame_logs)
    df.to_csv("Dataset/" + filename, index=False)
    print(f"[✓] Game data saved to {filename}")

def connect(port):
    # For making a connection with the game
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    (client_socket, _) = server_socket.accept()
    print("Connected to game!")
    return client_socket

def send(client_socket, command):
    # This function will send your updated command to Bizhawk so that game reacts according to your command
    command_dict = command.object_to_dict()
    pay_load = json.dumps(command_dict).encode()
    client_socket.sendall(pay_load)

def receive(client_socket):
    # Receive the game state and return the game state
    pay_load = client_socket.recv(4096)
    input_dict = json.loads(pay_load.decode())
    game_state = GameState(input_dict)
    return game_state

def get_manual_command():
    # Handle manual input for Player 1
    command = Command()
    # Set Player 1 controls based on keypresses
    # Example: Using 'w', 'a', 's', 'd' for up, left, down, right movement
    command.player_buttons.up = keyboard.is_pressed('w')
    command.player_buttons.down = keyboard.is_pressed('s')
    command.player_buttons.left = keyboard.is_pressed('a')
    command.player_buttons.right = keyboard.is_pressed('d')
    command.player_buttons.A = keyboard.is_pressed('j')  # Use 'j' for A button
    command.player_buttons.B = keyboard.is_pressed('k')  # Use 'k' for B button
    command.player_buttons.X = keyboard.is_pressed('l')  # Use 'l' for X button
    command.player_buttons.Y = keyboard.is_pressed('i')  # Use 'i' for Y button
    command.player_buttons.L = keyboard.is_pressed('n')  # Use 'n' for L button
    command.player_buttons.R = keyboard.is_pressed('m')  # Use 'm' for R button
    return command


def main():
    if len(sys.argv) < 2:
        print("Usage: python controller.py <output_csv_file>")
        sys.exit(1)
    client_socket = connect(9999)
    current_game_state = None
    frame_counter = 0
    while True:
        current_game_state = receive(client_socket)
        log_game_state_to_pandas(current_game_state, frame_counter)
        manual_command = get_manual_command()
        send(client_socket, manual_command)  # Send Player 1's manual command
        frame_counter += 1

if __name__ == '__main__':
    try:
        main()
    finally:
        save_logs_to_csv(sys.argv[1])
