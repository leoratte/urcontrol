import threading
import time

class UR44C_mock():
    def __init__(self):
        self.data = {}
        self.num_inputs = 6


    def SetParameterByName(self, unit, name, value, input=0):
        param_num, min_val, max_val, def_val, val_descr, notes = getattr(unit, name)
        assert min_val <= value <= max_val
        assert 0 <= input <= 5
        self.data[param_num] = value
        return True


    def GetParameterByName(self, unit, name, input=0):
        param_num, min_val, max_val, def_val, val_descr, notes = getattr(unit, name)
        assert 0 <= input <= 5
        if param_num not in self.data:
            self.data[param_num] = def_val
        return self.data[param_num]
