import msvcrt, os, sys, random, configparser, winsound

os.system("title Coin Thief")

# Create or load the high score config file
config_file = 'high_score.ini'
config = configparser.ConfigParser()
if os.path.exists(config_file):
    try:     
        config.read(config_file)
    except (configparser.Error, ValueError) as e:
        print(f"Error reading config file: {e}")
        sys.exit(1)
else:
    config.add_section('Score')
    config.set('Score', 'Easy_Small', '0')
    config.set('Score', 'Easy_Medium', '0')
    config.set('Score', 'Easy_Large', '0')
    config.set('Score', 'Normal_Small', '0')
    config.set('Score', 'Normal_Medium', '0')
    config.set('Score', 'Normal_Large', '0')
    config.set('Score', 'Hard_Small', '0')
    config.set('Score', 'Hard_Medium', '0')
    config.set('Score', 'Hard_Large', '0')
    config.set('Score', 'Endless_Endless', '0')
    with open('high_score.ini', 'w') as f:
        config.write(f)
    
# Set some tunes
notes = {'C': 262, 'D': 294, 'E': 330, 'F': 349, 'G': 392, 'A': 440, 'B': 494}
theme = ['A', 'D', 'A', 'D', 'G', 'F', 'E']
win = ['B', 'A', 'G']
lose = ['E', 'G']

# Set the in-game characters
thief_char = "\033[32m@\033[0m"    # Thief symbol in green
guard_char = "\033[31m&\033[0m" # Guard symbol in red
stair_char = "\033[36m%\033[0m"  # Stairs symbol in cyan
coin_char = "\033[33m*\033[0m"  # Coin symbol in yellow
crate_char = "\033[35m#\033[0m"  # Crate symbol in magenta
wall_char = "\033[90m+\033[0m" # Wall symbol in grey
empty_char = " " # Empty space symbol (it's empty)

# Define the play_sound function
def play_sound(sound):
    if sound == theme:
        for note in theme:
            frequency = notes[note]
            duration = 100  # In milliseconds
            winsound.Beep(frequency, duration)
    if sound == win:
        for note in win:
            frequency = notes[note]
            duration = 100  # In milliseconds
            winsound.Beep(frequency, duration)
    if sound == lose:
        for note in lose:
            frequency = notes[note]
            duration = 100  # In milliseconds
            winsound.Beep(frequency, duration)
    """
    This uses winsound to to play a series of notes in the theme dictionary.
    The different themes are stored in the variables and called in the for loops. The function calls the sound effect.
    """

# Show the instructions and credits
def title_screen():
    print("   ___ \033[33m___\033[0m ___ _  _\n"
        "  / __\033[33m/ _ \\\033[0m_ _| \| |\n"
        " | (_\033[33m| (_) |\033[0m || .` |\n"
        "  \___\033[33m\___/\033[0m___|_|\_| ___     v1.5 \u00A9 2023 Lanecrest Tech\n"
        " |_   _| || |_ _| __| __|\n"
        "   | | | __ || || _|| _|\n"
        "   |_| |_||_|___|___|_|\n\n"
        "INSTRUCTIONS:\n"
        f"You are the {thief_char} thief. Move with the arrow keys.\n"
        f"Collect {coin_char} coins to increase your score!\n"
        f"Move around {crate_char} crates which block you and the guard.\n"
        f"Reach the {stair_char} stairs to move up to the next floor.\n"
        f"Getting caught by the {guard_char} guard ends the game!\n\n"
        f"You do not need to collect every {coin_char} on each floor.\n"
        "If you do collect every coin on a floor, you receive a bonus.\n"
        f"You must reach the {stair_char} on the fifth floor to escape!\n"
        "Your score is only saved if you escape to the roof.\n\n"
        "You can choose the difficulty and floor sizes on the next screens.\n"
        "Your high scores are saved separately for each mode.\n")
    play_sound(theme)
    input("Press Enter to continue.")

# Define the difficulty mode function
def difficulty_mode():
    global guard_difficulty, floor_size
    while True:
        os.system('cls')
        print("Choose the difficulty:\n"
            "1 - Easy\n2 - Normal\n3 - Hard\n4 - Endless\n\n"
            "The difficulty determines the starting speed of the guard.\n"
            "The guard gets faster every floor.\n\n"
            "Endless Mode:\n\n"
            "Endless Mode has special rules.\n"
            "You keep moving up floors until caught at which point your score is saved.\n"
            "The guard speed is random on every floor, ranging among the fastest speeds in the other modes.\n"
            "The floor size is random on every floor, ranging among the small, medium, and large modes.\n"
            "There is no bonus score for collecting all the coins on a floor.\n")
        difficulty_prompt = input("Enter your choice: ")
        if difficulty_prompt == "1":
            guard_difficulty = "Easy"
            break
        elif difficulty_prompt == "2":
            guard_difficulty = "Normal"
            break
        elif difficulty_prompt == "3":
            guard_difficulty = "Hard"
            break
        elif difficulty_prompt == "4":
            guard_difficulty = "Endless"
            floor_size = "Endless"
            break
    """
    This prompts the user to select the difficulty. It stores the value as a string so it can be read in other functions.
    The functions are separated so the player only needs to enter 1, 2, or 3.
    """

# Define the floor_mode function
def floor_mode():
    global floor_size
    if guard_difficulty != "Endless":
        while True:
            os.system('cls')
            print("Choose the floor size:\n"
            "1 - Small\n2 - Medium\n3 - Large\n\n"
            "The floor size determines the width and height as well as how many coins and crates spawn.\n"
            "Each floor layout is randomly generated but all five will have the same dimensions.\n")
            size_prompt = input("Enter your choice: ")
            if size_prompt == "1":
                floor_size = "Small"
                break
            elif size_prompt == "2":
                floor_size = "Medium"
                break
            elif size_prompt == "3":
                floor_size = "Large"
                break
    """
    This prompts the user to select the floor size. It stores the value as a string so it can be read in other functions.
    The functions are separated so the player only needs to enter 1, 2, or 3.
    This should only prompt if the player did not select Endless difficulty.
    """

# Define the set_difficulty function
def set_difficulty(difficulty):
    if difficulty == "Easy":
        return 9    # The "Speed" or frequency of movement for the guard
    elif difficulty == "Normal":
        return 8
    elif difficulty == "Hard":
        return 7
    elif difficulty == "Endless":
        return random.choice([2, 3, 4])
    """
    Pulls the strings from the difficulty_mode function and sets them as values.
    Gets called in the game_defaults function.
    """

# Define the set_size function
def set_size(size):
    if size == "Small":
        return 20, 10, 20, 10   # Width, Height, Crates, Coins
    elif size == "Medium":
        return 30, 15, 30, 15
    elif size == "Large":
        return 40, 20, 40, 20
    elif size == "Endless":
        return random.choice([
            (20, 10, 20, 10),
            (30, 15, 30, 15),
            (40, 20, 40, 20)
        ])
    """
    Pulls the strings from the floor_mode function and sets them as values.
    Gets called in the game_defaults functions.
    """

# Define the game_defaults function
def game_defaults():
    global guard_speed, floor_width, floor_height, crate_num, coin_num, new_thief_pos, game_mode, high_score
    guard_speed = set_difficulty(guard_difficulty)
    floor_width, floor_height, crate_num, coin_num = set_size(floor_size)
    new_thief_pos = None
    game_mode = guard_difficulty + "_" + floor_size
    high_score = int(config.get('Score', game_mode))
    """
    This takes the settings defined in the difficulty and floor mode functions and pulls high score data as well as sets some other needed variables.
    This allows the game to be restarted with new settings between rounds.
    """

# Define the print_floor function
def print_floor():
    wall = wall_char * (floor_width + 2)
    level_string = wall + "\n"
    for y in range(floor_height):
        row = ""
        for x in range(floor_width):
            row += (thief_char if (x, y) == thief_pos else
                guard_char if (x, y) == guard_pos else
                stair_char if (x, y) == stair_pos else
                coin_char if (x, y) in coin_pos else
                crate_char if (x, y) in crate_pos else
                empty_char)
        level_string += wall_char + row + wall_char + "\n"
    level_string += wall
    print(level_string)
    """
    Draws the floor.
    The characters are displayed in their corresponding positions and the empty space is filled out.
    Every time the function is called it should have updated positions for everything.
    """

# Define the no_softlock function
def no_softlock(pos, walls, crates):
    x, y = pos
    adjacent_positions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    walls = list(walls)
    num_crates = 0
    num_walls = 0
    for adj_pos in adjacent_positions:
        if adj_pos in walls:
            num_walls += 1
        elif adj_pos in crates:
            num_crates += 1
    return num_crates > 3 or (num_crates > 1 and num_walls > 1)
    """
    This checks that the number of adjacent crates or walls will not exceed a certain threshold causing them to generate a softlock.
    """

# Define the game_hud function
def game_hud():
    if guard_difficulty == "Endless":
        print(f"Level: {floor_no} of \u221E\n"
              f"Coins: {score}\n\n"
              f"High Score: {high_score}")
    else:
        print(f"Level: {floor_no} of 5\n"
            f"Coins: {score}\n\n"
            f"Difficulty: {guard_difficulty}\n"
            f"Level Size: {floor_size}\n"
            f"High Score: {high_score}")
    """
    Draws the game hud based on mode.
    It displays basic info about the game such as level info, difficulty, and score
    """

# Define the end_game function
def end_game():
    global floor_no, score
    floor_no = 0
    score = 0
    while True:
        print("Continue?\n"
        "1 - Restart\n2 - Change Settings\n3 - Quit\n")
        end_prompt = input("Enter your choice: ")
        if end_prompt == "1":
            game_defaults()
            break
        elif end_prompt == "2":
            difficulty_mode()
            floor_mode()
            game_defaults()
            break
        elif end_prompt == "3":
            sys.exit(0)
        else:
            os.system('cls')
    """
    This prompts the user to to restart the game with the same settings, new setting, or gives them the option to quit.
    """

# Start the main game loop. The first sections only run when a new floor (or game start) is loaded

if __name__ == "__main__":
    floor_no = 0
    score = 0
    title_screen()
    difficulty_mode()
    floor_mode()
    game_defaults()

    while True:
        os.system('cls')

        # Update the counters  or settings when a new floor loads
        if guard_difficulty == "Endless":   # This make the guard speed and floor size regenerate on each floor in Endless
            game_defaults()
        else:
            guard_speed -= 1
        floor_no += 1
        move_counter = 0

        # Set the new character positions when a new floor loads
        thief_pos = new_thief_pos   # This lets the thief spawn where the stairs were on the last floor
        if new_thief_pos is None:
            thief_pos = (random.randint(0, floor_width - 1), random.randint(0, floor_height - 1))
        guard_pos = (random.randint(0, floor_width - 1), random.randint(0, floor_height - 1))
        stair_pos = (random.randint(0, floor_width - 1), random.randint(0, floor_height - 1))
        while guard_pos == stair_pos or guard_pos == thief_pos:
            guard_pos = (random.randint(0, floor_width - 1), random.randint(0, floor_height - 1))
        while stair_pos == guard_pos or stair_pos == thief_pos:
            stair_pos = (random.randint(0, floor_width - 1), random.randint(0, floor_height - 1))
        coin_pos = []
        for _ in range(coin_num):
            coin = (random.randint(0, floor_width - 1), random.randint(0, floor_height - 1))
            while (coin == thief_pos or coin == guard_pos or coin == stair_pos or coin in coin_pos):
                coin = (random.randint(0, floor_width - 1), random.randint(0, floor_height - 1))
            coin_pos.append(coin)
        crate_pos = []
        for _ in range(crate_num):
            crate = (random.randint(0, floor_width - 1), random.randint(0, floor_height - 1))
            while (crate == thief_pos or crate == guard_pos or crate == stair_pos or crate in coin_pos or crate in crate_pos or no_softlock(crate, wall_char, crate_pos)):
                crate = (random.randint(0, floor_width - 1), random.randint(0, floor_height - 1))
            crate_pos.append(crate)

        # Sub loop that in order checks if won, next floor, lose, coin collected, thief move, guard move
        while True:

            # Check if the thief has finished the 5th floor (win). Also updates the high score for the mode if it's a new record
            if floor_no == 6 and guard_difficulty != "Endless":
                os.system('cls')
                if score > high_score:
                    config.set('Score', game_mode, str(score))
                    with open('high_score.ini', 'w') as f:
                         config.write(f)
                high_score = int(config.get('Score', game_mode))
                print(f"You escaped!\n\n"
                    f"You reached the roof with {score} coins.\n"
                    f"Your high score is: {high_score}\n")
                play_sound(win)
                end_game()
                break

            # Check if the thief has reached the stairs (next floor)
            if thief_pos == stair_pos:
                if floor_no != 5:   # Split in an if/else so the stairs sound doesn't play when reaching the roof on normal modes
                    winsound.Beep(notes['E'], 25)
                elif guard_difficulty == "Endless":
                    winsound.Beep(notes['E'], 25)
                break

            # Check if the thief has been caught by the guard (lose)
            if thief_pos == guard_pos and guard_difficulty != "Endless":
                os.system('cls')
                print(f"You were caught!\n\n"
                    f"You were on floor {floor_no} and collected {score} coins.\n"
                    f"Your high score is: {high_score}\n")
                play_sound(lose)
                end_game()
                break
            elif thief_pos == guard_pos:   # Alternate end condition if game is being played on Endless
                os.system('cls')
                if score > high_score:
                    config.set('Score', game_mode, str(score))
                    with open('high_score.ini', 'w') as f:
                         config.write(f)
                high_score = int(config.get('Score', game_mode))
                print(f"Game Over!\n\n"
                    f"You were on floor {floor_no} and collected {score} coins.\n"
                    f"Your high score is: {high_score}\n")
                play_sound(win)
                end_game()
                break

            # Check if the thief has collected a coin
            if thief_pos in coin_pos:
                winsound.Beep(notes['B'], 25)
                coin_pos.remove(thief_pos)
                score += 1
                if guard_difficulty != "Endless":   # Provides a bonus score if not in Endless mode
                    if not coin_pos:
                        score += 10

            # Draw the floor. This is in the loop so character objects update whenever they move
            print_floor()
            game_hud()
            print("\033[H", end="")

            # Check for thief movement. The game stops updating until one of the move keys is pressed
            move = msvcrt.getch()
            new_thief_pos = thief_pos
            if move == b'M':    # Right key
                new_thief_pos = (thief_pos[0] + 1, thief_pos[1])
            if move == b'K':    # Left key
                new_thief_pos = (thief_pos[0] - 1, thief_pos[1])
            if move == b'P':    # Down key
                new_thief_pos = (thief_pos[0], thief_pos[1] + 1)
            if move == b'H':    # Up key
                new_thief_pos = (thief_pos[0], thief_pos[1] - 1)
            if (0 <= new_thief_pos[0] < floor_width and 0 <= new_thief_pos[1] < floor_height and new_thief_pos not in crate_pos):
                thief_pos = new_thief_pos
            else:
                winsound.Beep(notes['C'], 25)   # This sound plays if the thief bumps a wall or crate
            move_counter += 1
   
            # Check for guard movement. After the guard moves, the sub loop repeats
            if move_counter % guard_speed == 0:
                dx = abs(thief_pos[0] - guard_pos[0])
                dy = abs(thief_pos[1] - guard_pos[1])
                if dx > dy:
                    if thief_pos[0] < guard_pos[0]:
                        new_guard_pos = (max(0, guard_pos[0] - 1), guard_pos[1])
                    elif thief_pos[0] > guard_pos[0]:
                        new_guard_pos = (min(floor_width - 1, guard_pos[0] + 1), guard_pos[1])
                    else:
                        new_guard_pos = guard_pos
                else:
                    if thief_pos[1] < guard_pos[1]:
                        new_guard_pos = (guard_pos[0], max(0, guard_pos[1] - 1))
                    elif thief_pos[1] > guard_pos[1]:
                        new_guard_pos = (guard_pos[0], min(floor_height - 1, guard_pos[1] + 1))
                    else:
                        new_guard_pos = guard_pos
                if new_guard_pos in crate_pos:
                    if thief_pos[0] < guard_pos[0]:
                        new_guard_pos = (max(0, guard_pos[0] - 1), guard_pos[1])
                    elif thief_pos[0] > guard_pos[0]:
                        new_guard_pos = (min(floor_width - 1, guard_pos[0] + 1), guard_pos[1])
                    if new_guard_pos in crate_pos:
                        if thief_pos[1] < guard_pos[1]:
                            new_guard_pos = (guard_pos[0], max(0, guard_pos[1] - 1))
                        elif thief_pos[1] > guard_pos[1]:
                            new_guard_pos = (guard_pos[0], min(floor_height - 1, guard_pos[1] + 1))
                    if new_guard_pos in crate_pos:
                        new_guard_pos = guard_pos
                guard_pos = new_guard_pos