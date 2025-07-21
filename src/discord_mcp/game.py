import random

class HangmanGame:
    """
    Manages the state and logic for a single game of Hangman.
    """
    
    WORDS = [
        "adder", "alpaca", "anchovy", "anole", "aphid", "axolotl", 
        "badger", "bears", "beaver", "beetle", "bison", "bobcat", 
        "booby", "bunting", "camel", "canary", "cattle", "chicken", 
        "chimp", "cicada", "cobra", "conch", "condor", "coral", 
        "cougar", "crane", "cricket", "curlew", "donkey", "dragon", 
        "eagle", "egret", "falcon", "ferret", "finch", "foxes", 
        "gannet", "gecko", "goats", "goose", "gopher", "gorilla", 
        "grouper", "grouse", "halibut", "hares", "hawks", "heron", 
        "herring", "hippo", "hornet", "horse", "hyena", "iguana", 
        "jackal", "jaguar", "kestrel", "koala", "larva", "lemur", 
        "lions", "lizard", "llama", "lobster", "locust", "louse", 
        "macaw", "mamba", "manta", "mantis", "marlin", "marmot", 
        "mayfly", "monitor", "monkey", "moose", "mouse", "mussel", 
        "nurse", "ocelot", "octopus", "osprey", "otter", "oyster", 
        "panda", "parrot", "pelican", "perch", "petrel", "pigeon", 
        "plaice", "plover", "possum", "puffin", "python", "quail", 
        "rabbit", "racer", "rattler", "raven", "rhino", "roach", 
        "robin", "salmon", "sardine", "scallop", "shark", "sheep", 
        "shrew", "shrimp", "skate", "skink", "skunk", "sloth", 
        "snake", "snapper", "spider", "sponge", "squid", "stork", 
        "sunfish", "termite", "thrush", "tiger", "trout", "turbot", 
        "turkey", "turtle", "urchin", "viper", "vulture", "weasel", 
        "weevil", "whale", "wigeon", "wolves", "wombat", "wrasse", 
        "zebra"
    ]


    HANGMAN_PICS = [
        """
         +---+
         |   |
             |
             |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
             |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
         |   |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
        /|   |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
        /|\\  |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
        /|\\  |
        /    |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
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
        """Constructs the message to display the current game state."""
        display_word = self.get_display_word()
        hangman_art = self.HANGMAN_PICS[len(self.HANGMAN_PICS) - 1 - self.attempts_left]
        
        message = (
            f"```\n{hangman_art}\n\n"
            f"Word: {display_word}\n\n"
            f"Incorrect Guesses: {' '.join(sorted(self.guesses_incorrect))}\n"
            f"Attempts Left: {self.attempts_left}\n"
            f"```"
        )
        
        if self.is_won():
            message += f"\n**Congratulations! You won! The word was `{self.word}`.**"
        elif self.is_lost():
            message += f"\n**Game Over! You lost. The word was `{self.word}`.**"
        else:
            message += "\nType a letter to guess."
            
        return message