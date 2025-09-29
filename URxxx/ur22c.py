from URxxx.ur44c import UR44C

class UR22C(UR44C):
    def __init__(self, midi_in, midi_out):
        super().__init__(midi_in, midi_out)
        self.num_inputs = 2
