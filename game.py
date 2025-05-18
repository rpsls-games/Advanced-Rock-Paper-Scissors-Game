import random
from enum import IntEnum
from abc import ABC, abstractmethod
from typing import List, Type, TypeVar
from collections import Counter
from pydantic import BaseModel

# ---------------------------------------
# TYPE VAR FOR ACTION ENUMS
# ---------------------------------------

TAction = TypeVar("TAction", bound=IntEnum)

# ---------------------------------------
# ACTION ENUMS
# ---------------------------------------


class Action(IntEnum):
    Rock = 0
    Paper = 1
    Scissors = 2
    Lizard = 3
    Spock = 4


class FireWaterAction(IntEnum):
    # example of new actions for new game rules
    Rock = 0
    Paper = 1
    Scissors = 2
    Fire = 3
    Water = 4

# ---------------------------------------
# RULE SETS
# ---------------------------------------


victories_classic = {
    Action.Rock: [Action.Scissors],
    Action.Paper: [Action.Rock],
    Action.Scissors: [Action.Paper],
}

victories_extended = {
    Action.Scissors: [Action.Paper, Action.Lizard],
    Action.Paper: [Action.Spock, Action.Rock],
    Action.Rock: [Action.Scissors, Action.Lizard],
    Action.Lizard: [Action.Spock, Action.Paper],
    Action.Spock: [Action.Scissors, Action.Rock],
}

# example of new game rules
victories_fire_water = {
    FireWaterAction.Rock: [FireWaterAction.Scissors, FireWaterAction.Fire],
    FireWaterAction.Paper: [FireWaterAction.Rock, FireWaterAction.Water],
    FireWaterAction.Scissors: [FireWaterAction.Paper, FireWaterAction.Water],
    FireWaterAction.Fire: [FireWaterAction.Scissors, FireWaterAction.Paper],
    FireWaterAction.Water: [FireWaterAction.Fire, FireWaterAction.Rock],
}


class RuleSet:
    def __init__(self, victories: dict):
        self.victories = victories

    def get_valid_actions(self) -> List[TAction]:
        return sorted(self.victories.keys(), key=lambda a: a.value)

    def defeats(self, a1: TAction, a2: TAction) -> bool:
        return a2 in self.victories.get(a1, [])

# ---------------------------------------
# STRATEGY CONTEXTS
# ---------------------------------------


class StrategyContext(BaseModel):
    pass


class RandomStrategyContext(StrategyContext):
    pass


class HumanHistoryContext(StrategyContext):
    human_moves: List[TAction] = []
    computer_moves: List[TAction] = []
    round_number: int = 0

# ---------------------------------------
# ABSTRACT STRATEGY
# ---------------------------------------


class AbstractStrategy(BaseModel, ABC):
    name: str

    @abstractmethod
    def select_action(self, valid_actions: List[TAction]) -> TAction:
        pass

    def update_context(self, human_action: TAction, computer_action: TAction):
        pass

# ---------------------------------------
# STRATEGY IMPLEMENTATIONS
# ---------------------------------------


class RandomStrategy(AbstractStrategy):
    name: str = "RandomStrategy"
    context: RandomStrategyContext = RandomStrategyContext()

    def select_action(self, valid_actions: List[TAction]) -> TAction:
        return random.choice(valid_actions)


class PredictiveStrategy(AbstractStrategy):
    name: str = "PredictiveStrategy"
    context: HumanHistoryContext = HumanHistoryContext()

    def select_action(self, valid_actions: List[TAction]) -> TAction:
        if not self.context.human_moves:
            return random.choice(valid_actions)

        # Find the player's most common move
        most_common = Counter(self.context.human_moves).most_common(1)[0][0]
        
        # Choose a move that would beat the player's most common move
        for action in valid_actions:
            if most_common in victories_extended.get(action, []):
                return action

        return random.choice(valid_actions)

    def update_context(self, human_action: TAction, computer_action: TAction):
        self.context.human_moves.append(human_action)
        self.context.computer_moves.append(computer_action)
        self.context.round_number += 1

# ---------------------------------------
# PLAYER CLASSES
# ---------------------------------------


class HumanPlayer:
    def __init__(self, action_enum: Type[TAction], name="You"):
        self.name = name
        self.action_enum = action_enum

    def select_action(self, valid_actions: List[TAction]) -> TAction:
        print("\nChoose your move:")
        for action in valid_actions:
            print(f"{action.name} [{action.value}]")
        while True:
            try:
                choice = int(input("Enter choice: "))
                action = self.action_enum(choice)
                if action in valid_actions:
                    return action
                print("Invalid for this game.")
            except Exception:
                print("Invalid input. Try again.")


class ComputerPlayer:
    def __init__(self, name: str, strategy: AbstractStrategy):
        self.name = name
        self.strategy = strategy

    def select_action(self, valid_actions: List[TAction]) -> TAction:
        return self.strategy.select_action(valid_actions)

    def update(self, human_action: TAction, computer_action: TAction):
        self.strategy.update_context(human_action, computer_action)

# ---------------------------------------
# GAME LOOP
# ---------------------------------------


class Game:
    def __init__(self, rule_set: RuleSet, human: HumanPlayer, computer: ComputerPlayer, mode: str, target: int):
        self.rule_set = rule_set
        self.human = human
        self.computer = computer
        self.mode = mode
        self.target = target
        self.rounds_played = 0
        self.scores = {self.human.name: 0, self.computer.name: 0}

    def play_round(self):
        valid_actions = self.rule_set.get_valid_actions()
        human_action = self.human.select_action(valid_actions)
        computer_action = self.computer.select_action(valid_actions)

        print(f"\n{self.human.name} chose {human_action.name}")
        print(f"{self.computer.name} chose {computer_action.name}")

        if human_action == computer_action:
            print("It's a tie!")
        elif self.rule_set.defeats(human_action, computer_action):
            print("You win this round!")
            self.scores[self.human.name] += 1
        else:
            print("Computer wins this round!")
            self.scores[self.computer.name] += 1

        self.computer.update(human_action, computer_action)
        self.rounds_played += 1

    def is_game_over(self) -> bool:
        if self.mode == "first_to":
            return any(score >= self.target for score in self.scores.values())
        elif self.mode == "fixed":
            return self.rounds_played >= self.target
        return False

    def play(self):
        while not self.is_game_over():
            self.play_round()
            print(
                f"Score: {self.human.name} {self.scores[self.human.name]} - {self.computer.name} {self.scores[self.computer.name]}")

        print("\n--- Game Over ---")
        human_score = self.scores[self.human.name]
        computer_score = self.scores[self.computer.name]

        if human_score > computer_score:
            print("You won the game!")
        elif human_score < computer_score:
            print("Computer won the game!")
        else:
            print("It's a draw!")

# ---------------------------------------
# MAIN FUNCTION
# ---------------------------------------


def main():
    print("Welcome to Rock, Paper, Scissors!")

    while True:
        print("\nChoose game type:")
        print("1. Classic (Rock, Paper, Scissors)")
        print("2. Extended (Rock, Paper, Scissors, Lizard, Spock)")
        print("3. Fire-Water Variant")
        try:
            game_type = int(input("Enter choice (1/2/3): "))
            if game_type == 1:
                rules = RuleSet(victories_classic)
                action_enum = Action
                break
            elif game_type == 2:
                rules = RuleSet(victories_extended)
                action_enum = Action
                break
            elif game_type == 3:
                rules = RuleSet(victories_fire_water)
                action_enum = FireWaterAction
                break
            else:
                print("Invalid option.")
        except ValueError:
            print("Please enter a valid number.")

    while True:
        print("\nSelect strategy for the computer:")
        print("1. Random Strategy")
        print("2. Predictive Strategy")
        try:
            strategy_choice = int(input("Enter choice (1 or 2): "))
            if strategy_choice == 1:
                strategy = RandomStrategy()
                break
            elif strategy_choice == 2:
                strategy = PredictiveStrategy()
                break
            else:
                print("Invalid option.")
        except ValueError:
            print("Please enter a valid number.")

    while True:
        print("\nSelect game mode:")
        print("1. First to N wins")
        print("2. Fixed number of rounds")
        try:
            mode_choice = int(input("Enter choice (1 or 2): "))
            if mode_choice == 1:
                mode = "first_to"
                target = int(input("Enter N: "))
                break
            elif mode_choice == 2:
                mode = "fixed"
                target = int(input("Enter number of rounds: "))
                break
            else:
                print("Invalid option.")
        except ValueError:
            print("Please enter a valid number.")

    human = HumanPlayer(action_enum)
    computer = ComputerPlayer("Computer", strategy)
    game = Game(rules, human, computer, mode, target)
    game.play()


if __name__ == "__main__":
    main()
