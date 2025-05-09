import torch
import torch.nn as nn
import numpy as np
import joblib
import pandas as pd
from math import sqrt
from command import Command
from buttons import Buttons
from training_model import LSTMModel  # Your PyTorch model definition

class Bot:
    def __init__(self):
        self.state_buffer = []
        self.prev_buttons = [0] * 10
        self.prev_p1_x = None
        self.prev_p2_x = None
        self.prev_p1_health = None
        self.prev_p2_health = None
        self.frame_window = 10
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load scaler
        self.scaler = joblib.load('scaler.pkl')

        # Columns to normalize (same as used during training + new ones)
        self.norm_cols = [
            'p1_health', 'p1_x', 'p1_y',
            'p2_health', 'p2_x', 'p2_y',
            'timer', 'dx', 'dy', 'distance',
            'p1_velocity_x', 'p2_velocity_x',
            'p1_health_change', 'p2_health_change'
        ]
        with open("input_features.txt", "r") as f:
            self.input_feature_cols = [line.strip() for line in f.readlines()]

        input_size = len(self.input_feature_cols)
        output_size = 10  # Number of buttons
        self.model = LSTMModel(input_size=input_size, hidden_size=128, output_size=output_size).to(self.device)
        self.model.load_state_dict(torch.load("lstm_model.pt", map_location=self.device))
        self.model.eval()

        self.my_command = Command()
        self.buttn = Buttons()

    def extract_features(self, game_state):
        p1 = game_state.player1
        p2 = game_state.player2
        btns_2 = p2.player_buttons

        # Derived features
        dx = p1.x_coord - p2.x_coord
        dy = p1.y_coord - p2.y_coord
        distance = sqrt(dx ** 2 + dy ** 2)

        p1_velocity_x = 0 if self.prev_p1_x is None else p1.x_coord - self.prev_p1_x
        p2_velocity_x = 0 if self.prev_p2_x is None else p2.x_coord - self.prev_p2_x
        p1_health_change = 0 if self.prev_p1_health is None else p1.health - self.prev_p1_health
        p2_health_change = 0 if self.prev_p2_health is None else p2.health - self.prev_p2_health

        # Update previous values
        self.prev_p1_x = p1.x_coord
        self.prev_p2_x = p2.x_coord
        self.prev_p1_health = p1.health
        self.prev_p2_health = p2.health

        return [
            p1.player_id, p1.health, p1.x_coord, p1.y_coord,
            int(p1.is_jumping), int(p1.is_crouching), int(p1.is_player_in_move), p1.move_id,

            p2.health, p2.x_coord, p2.y_coord,
            int(p2.is_jumping), int(p2.is_crouching), int(p2.is_player_in_move), p2.move_id,

            int(btns_2.up), int(btns_2.down), int(btns_2.left), int(btns_2.right),
            int(btns_2.Y), int(btns_2.B), int(btns_2.X), int(btns_2.A), int(btns_2.L), int(btns_2.R),

            game_state.timer,
            int(game_state.has_round_started),
            0 if game_state.fight_result == 'NOT_OVER' else 1,

            dx, dy, distance,
            p1_velocity_x, p2_velocity_x,
            p1_health_change, p2_health_change,

            *self.prev_buttons  # Append previous predictions
        ]

    def fight(self, current_game_state, player):
        self.my_command = Command()
        self.buttn = Buttons()

        # Extract features
        features = self.extract_features(current_game_state)
        self.state_buffer.append(features)
        if len(self.state_buffer) > self.frame_window:
            self.state_buffer.pop(0)

        # Wait until buffer is full
        if len(self.state_buffer) < self.frame_window:
            return self.my_command

        # Normalize and predict
        buffer_df = pd.DataFrame(self.state_buffer, columns=self.input_feature_cols)
        buffer_df[self.norm_cols] = self.scaler.transform(buffer_df[self.norm_cols])
        input_seq = torch.tensor(buffer_df.to_numpy(), dtype=torch.float32).unsqueeze(0).to(self.device)

        with torch.no_grad():
            preds = self.model(input_seq).squeeze(0).cpu().numpy()

        predictions = [1 if p >= 0.3 else 0 for p in preds]
        self.prev_buttons = predictions.copy()  # Store for next time

        self.set_buttons(predictions)
        self.my_command.player_buttons = self.buttn
        return self.my_command

    def set_buttons(self, predictions):
        self.buttn.up     = bool(predictions[0])
        self.buttn.down   = bool(predictions[1])
        self.buttn.left   = bool(predictions[2])
        self.buttn.right  = bool(predictions[3])
        self.buttn.Y      = bool(predictions[4])
        self.buttn.B      = bool(predictions[5])
        self.buttn.X      = bool(predictions[6])
        self.buttn.A      = bool(predictions[7])
        self.buttn.L      = bool(predictions[8])
        self.buttn.R      = bool(predictions[9])
