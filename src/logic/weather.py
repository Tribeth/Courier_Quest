import random


class Weather:
    def __init__(
            self,
            initial_state: str,
            transition: dict[str, dict[str, float]]):
        self.state = initial_state
        self.transition = transition

    def next_state(self) -> str:
        probabilities = self.transition[self.state]
        states = list(probabilities.keys())
        weights = list(probabilities.values())
        self.state = random.choices(states, weights=weights)[0]
        return self.state