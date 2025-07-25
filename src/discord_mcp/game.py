import random

class HangmanGame:
    """
    Manages the state and logic for a single game of Hangman.
    """
    
    WORDS = [
        # Well-known animals of varying difficulty
        "alligator", "alpaca", "badger", "beaver", "bison", "bobcat",
        "butterfly", "camel", "caterpillar", "cheetah", "chicken",
        "chimpanzee", "cobra", "condor", "cougar", "crocodile", "dolphin",
        "donkey", "eagle", "elephant", "falcon", "ferret", "flamingo",
        "giraffe", "gorilla", "horse", "hyena", "iguana", "jaguar",
        "koala", "lemur", "leopard", "lion", "lizard", "llama", "lobster",
        "monkey", "octopus", "otter", "panda", "panther", "parrot",
        "pelican", "penguin", "puffin", "python", "rabbit", "raven",
        "rhinoceros", "scorpion", "shark", "sheep", "skunk", "sloth",
        "snake", "spider", "squid", "squirrel", "tiger", "turtle",
        "vulture", "weasel", "whale", "wolf", "wombat", "zebra"
    ]


    HANGMAN_PICS = [
        # State 0: 6 attempts left
        """
        ☀️
          +---+
          |   |
              |
              |
              |
              |
         =========
        """,
        # State 1: 5 attempts left
        """
        ☀️
          +---+
          |   |
          😐  |
              |
              |
              |
         =========
        """,
        # State 2: 4 attempts left
        """
        ☀️
          +---+
          |   |
          😐  |
          |   |
              |
              |
         =========
        """,
        # State 3: 3 attempts left
        """
        ☀️
          +---+
          |   |
          😐  |
         /|   |
              |
              |
         =========
        """,
        # State 4: 2 attempts left
        """
        ☀️
          +---+
          |   |
          😐  |
         /|\\  |
              |
              |
         =========
        """,
        # State 5: 1 attempt left
        """
        ☀️
          +---+
          |   |
          😐  |
         /|\\  |
         /    |
              |
         =========
        """,
        # State 6: 0 attempts left
        """
        ☀️
          +---+
          |   |
          💀  |
         /|\\  |
         / \\  |
              |
         =========
        """
    ]

    def __init__(self):
        self.word = random.choice(self.WORDS).lower()
        self.guesses_correct = set()
        self.guesses_incorrect = set()
        self.attempts_left = len(self.HANGMAN_PICS) - 1

    def guess(self, letter: str) -> bool:
        """Processes a single letter guess, updating the game state."""
        letter = letter.lower()
        if letter in self.word:
            self.guesses_correct.add(letter)
            return True
        else:
            if letter not in self.guesses_incorrect:
                self.guesses_incorrect.add(letter)
                self.attempts_left -= 1
            return False

    def is_won(self) -> bool:
        """Checks if the game has been won."""
        return set(self.word) <= self.guesses_correct

    def is_lost(self) -> bool:
        """Checks if the game has been lost."""
        return self.attempts_left <= 0

    def get_display_word(self) -> str:
        """Returns the word with unguessed letters as underscores."""
        return " ".join([letter if letter in self.guesses_correct else "_" for letter in self.word])

    def get_game_state_message(self) -> str:
        """Constructs the message to display the current game state within a retro terminal frame."""
        display_word = self.get_display_word()
        hangman_art_index = len(self.HANGMAN_PICS) - 1 - self.attempts_left
        hangman_art_index = max(0, min(hangman_art_index, len(self.HANGMAN_PICS) - 1))
        
        # Split the hangman art into lines and pad it for centering
        hangman_art_lines = self.HANGMAN_PICS[hangman_art_index].strip().split('\n')
        padded_art_lines = [f"║ {line.ljust(29)} ║" for line in hangman_art_lines]
        
        lives_display = '❤️' * self.attempts_left + '🖤' * (len(self.HANGMAN_PICS) - 1 - self.attempts_left)
        incorrect_guesses_str = ' '.join(sorted(self.guesses_incorrect))

        # Build the framed message
        message_lines = [
            "╔═══════════════════════════════╗",
            "║         H A N G M A N         ║",
            "╠═══════════════════════════════╣",
            "║                               ║",
            *padded_art_lines,
            "║                               ║",
            "╠═══════════════════════════════╣",
            f"║  Word:  {display_word.ljust(21)} ║",
            "║                               ║",
            f"║  Incorrect: {incorrect_guesses_str.ljust(17)} ║",
            "║                               ║",
            f"║  Lives: {lives_display.ljust(20)} ║",
            "╚═══════════════════════════════╝"
        ]
        
        message = "```\n" + "\n".join(message_lines) + "\n```"

        if self.is_won():
            message += f"\n**Congratulations! You won! The word was `{self.word}`.**"
        elif self.is_lost():
            message += f"\n**Game Over! You lost. The word was `{self.word}`.**"
        else:
            message += "\nType a letter to guess."

        return message