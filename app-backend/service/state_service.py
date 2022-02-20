class StateService:
    def __init__(self):
        self.state = 1

    def change_state(self):
        if self.state >= 5:
            self.state = 1
        else:
            self.state += 1

    def set_state(self, value):
        self.state = value