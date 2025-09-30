from abc import ABC, abstractmethod
from time import perf_counter_ns

# okay, so rounds work like this
# init bots
# while game.is_active():
    # move = bot.think(state, stats)
# discard bots

class Timer:
    game_start_time_ms: int = 1000
    increment_ms: int = 5
    ms_remaining: int = 1000 # time left for the current player
    opponent_ms_remaining: int = 1000 # time left for the opponent

    __turn_start_time_ms: int = -1

    @property
    def ms_elapsed_this_turn(self) -> int:
        return self.__perf_counter_ms() - self.__turn_start_time_ms if self.__turn_start_time_ms != -1 else 0

    @staticmethod
    def __perf_counter_ms() -> int:
        return perf_counter_ns() // 1_000_000

    def __enter__(self):
        self.__turn_start_time_ms = self.__perf_counter_ms()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ms_remaining -= self.__perf_counter_ms() - self.__turn_start_time_ms
        self.ms_remaining += self.increment_ms # increment after move
        self.__turn_start_time_ms = -1
        if self.ms_remaining < 0:
            raise TimeoutError("Bot exceeded its time limit")


class GameState():
    # TODO: implement basic functionality!
    pass


class Bot(ABC):
    @abstractmethod
    def think(self, state: GameState, timer: Timer):
        """Given the current game state and a timer, return the bot's next move."""
        pass
