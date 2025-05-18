# Advanced Rock, Paper, Scissors Game

This project is a modular, extensible, and type-safe implementation of the classic Rock, Paper, Scissors game — built with support for:


## Features

- **Multiple Game Variants**:
  - Classic (Rock, Paper, Scissors)
  - Extended (Rock, Paper, Scissors, Lizard, Spock)
  - Fire-Water Variant (Rock, Paper, Scissors, Fire, Water)

- **Customizable Strategies**:
  - Random Strategy: Makes completely random choices
  - Predictive Strategy: Choose a move that would beat the player's most common move

- **Game Modes**:
  - First to N wins: Play until someone reaches the target score
  - Fixed rounds: Play a predetermined number of rounds

- **Clean architecture and code design**

## How to Play

1. Run the game: `python game.py`
2. Follow the prompts to select:
   - Game variant
   - Computer strategy
   - Game mode and target score/rounds

## Game Rules

### Classic Rules
- Rock crushes Scissors
- Paper covers Rock
- Scissors cut Paper

### Extended Rules (Rock, Paper, Scissors, Lizard, Spock)
- Scissors cut Paper
- Paper covers Rock
- Rock crushes Lizard
- Lizard poisons Spock
- Spock smashes Scissors
- Scissors decapitate Lizard
- Lizard eats Paper
- Paper disproves Spock
- Spock vaporizes Rock
- Rock crushes Scissors

### Fire-Water Variant
- Rock crushes Scissors and puts out Fire
- Paper covers Rock and floats on Water
- Scissors cut Paper and cut through Water
- Fire burns Scissors and Paper
- Water extinguishes Fire and erodes Rock

## Extensibility

The game is designed to be easily extensible with:

1. **New Game Variants**: Create a new `IntEnum` class and victory ruleset:

```python
class MyCustomAction(IntEnum):
    Action1 = 0
    Action2 = 1
    # Add more actions...

my_custom_victories = {
    MyCustomAction.Action1: [MyCustomAction.Action2],
    # Define other victory relationships...
}
```

2. **New Strategies**: Extend the `AbstractStrategy` class:

```python
class MyCustomStrategy(AbstractStrategy):
    name: str = "MyCustomStrategy"
    context: MyCustomContext = MyCustomContext()

    def select_action(self, valid_actions: List[TAction]) -> TAction:
        # Your custom logic here
        return chosen_action

    def update_context(self, human_action: TAction, computer_action: TAction):
        # Update any information you need for your strategy
        pass
```

### Example: Predictive Strategy Implementation

The existing Predictive Strategy demonstrates how strategies can be esily implemented:

```python
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
```

### Example: Fire-Water Variant Implementation

The Fire-Water variant shows how to implement new game rules:

```python
class FireWaterAction(IntEnum):
    Rock = 0
    Paper = 1
    Scissors = 2
    Fire = 3
    Water = 4

victories_fire_water = {
    FireWaterAction.Rock: [FireWaterAction.Scissors, FireWaterAction.Fire],
    FireWaterAction.Paper: [FireWaterAction.Rock, FireWaterAction.Water],
    FireWaterAction.Scissors: [FireWaterAction.Paper, FireWaterAction.Water],
    FireWaterAction.Fire: [FireWaterAction.Scissors, FireWaterAction.Paper],
    FireWaterAction.Water: [FireWaterAction.Fire, FireWaterAction.Rock],
}
```

## 🛠 Requirements
* Python 3.8+

* pydantic for context validation

```python
pip install pydantic
```
