# Street Fighter Bot Training

A machine learning project that trains AI agents to play Street Fighter through reinforcement learning.

## Overview

This repository contains code for training and deploying AI bots that can play Street Fighter. The bots use reinforcement learning techniques to master game mechanics and develop fighting strategies.

## Installation Guide

Follow these steps to set up the Street Fighter Bot Training environment on your system.

### Prerequisites

- Python 3.11 or higher
- Git
- Compatible operating system (Windows, Linux, or macOS)

### Step 1: Create a Virtual Environment

To avoid conflicts with other Python packages, create a dedicated virtual environment:

```bash
# Create a virtual environment named 'your_venv_name'
python3.11 -m venv your_venv_name
```

### Step 2: Activate the Virtual Environment

**Windows:**
```bash
.\your_venv_name\Scriptsctivate
```

**Linux or macOS:**
```bash
source ./your_venv_name/bin/activate
```

### Step 3: Clone the Repository

```bash
git clone https://github.com/AlgorithmicAhsan/Street-Fighter-Bot-Training
cd Street-Fighter-Bot-Training
```

### Step 4: Install Required Dependencies

```bash
pip install -r requirements.txt
```

## Running the Bot

Navigate to the Single Player directory:

```bash
cd Single-Player
```

Run the controller script:

```bash
python controller.py
```

Launch the emulator:

```bash
# Still in the Single-Player directory
./emuHawk.exe
```

### Configure the emulator:

1. Open the Street Fighter ROM
2. From the **Config** menu, select **Toolbox**
3. Start a game match
4. After selecting your character and when the match begins, select **Gyroscope bot** from the toolbox (2nd option)

Your AI model is now controlling Player 1!

## Features

- Reinforcement learning based fighting strategies
- Real-time control of game characters
- Performance analytics and training metrics
- Compatible with popular Street Fighter ROM versions

## Troubleshooting

If you encounter any issues during installation or execution:

- Make sure your Python version is 3.11 or higher
- Verify that all dependencies were successfully installed
- Check that the ROM is compatible with the emulator
- Ensure your virtual environment is activated when running scripts

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## Acknowledgments

- Special thanks to all contributors