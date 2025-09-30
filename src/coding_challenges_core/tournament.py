import atexit
import pickle
from pathlib import Path

from coding_challenges_core.bot import Bot
from coding_challenges_core.brackets.abc import Bracket
from coding_challenges_core.limits import Limits, validate

class Tournament():
    def __init__(self, tournament_dir: Path):
        self.__tournament_dir = tournament_dir
        self.__tournament_dir.mkdir(parents=True, exist_ok=True)
        self.bots = []  # type: list[type[Bot]]
        atexit.register(self.__save_state)
    
    @classmethod
    def load(cls, tournament_dir: Path) -> "Tournament":
        """Load a tournament from the given directory, or create a new one if none exists."""
        try:
            with open(tournament_dir / "state.pkl", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return cls(tournament_dir)
    
    def configure(self, limits: Limits, bracket: Bracket):
        self.limits = limits
        self.bracket = bracket
        self.__save_state()

    def discover_bots(self, bot_folder: Path):
        """Discover and load bots from the given folder."""
        if not hasattr(self, "bracket") or not hasattr(self, "limits"):
            raise RuntimeError("Tournament not configured. Please call configure() before running the tournament.")
        
        # TODO: logging and reports! i wanna know things
        # TODO: stable bot ordering (needed for seeding)
        for file in bot_folder.glob("*.py"):
            # Step 1: Validate!
            with open(file, "r") as f:
                source = f.read()
                try:
                    validate(self.limits, source)
                except ValueError as e:
                    print(f"Skipping {file}: {e}")
                    continue
            # Step 2: We passed! Import!!
            compiled = compile(source, file.name, 'exec')
            bot_module = eval(compiled, {}, {})
            # Step 2.5: Find bot class
            bot_class = None
            for obj in bot_module.values():
                if isinstance(obj, type) and issubclass(obj, Bot) and obj is not Bot:
                    bot_class = obj
                    break
            if bot_class is None:
                print(f"Skipping {file}: no Bot subclass found")
                continue
            # Step 3: Add to tournament
            # we're not initalizing the bot yet, just storing the class
            # we'll init them later for each match
            self.bots.append(bot_class)
        self.__save_state()
    
    def run_tournament(self):
        """Run the tournament to completion with the currently loaded bots.
        
        If you want to run a single round, use run_next_round() instead.
        """
        # yeah.
        while not self.bracket.is_complete():
            self.run_next_round()
        
    def run_next_round(self):
        """Run the next round of the tournament."""
        if not len(self.bots):
            raise RuntimeError("No bots loaded. Please call discover_bots() before running the tournament.")
        
        if self.bracket.is_complete():
            raise RuntimeError("Tournament is already complete.")
        
        self.bracket.run_next_round(self.bots, self.limits) # api WILL change, but the jist remains
        self.__save_state()

    def __save_state(self):
        with open(self.__tournament_dir / "state.pkl", "wb") as f:
            pickle.dump(self, f)
