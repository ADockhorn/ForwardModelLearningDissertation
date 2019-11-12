
class ObjectGameState:
    def __init__(self, next_state_lists, width, height):
        self.state = next_state_lists
        self.width = width
        self.height = height
        self.string = self.get_observation_string()

    def get_observation_string(self):
        return "\n".join([",".join([" ".join([str(element["itype"])for element in self.state[row][col]]) for row in range(len(self.state))]) for col in range(len(self.state[0]))])