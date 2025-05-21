class ISO8583Error(ValueError):
    def __init__(self, bit, length, position, message="ISO 8583 Error"):
        errmsg = f"{message}: bit {bit}, position {position}"
        ValueError.__init__(self, errmsg)
        self.bit = bit
        self.length = length
        self.position = position

    def __str__(self):
        return f"{self.args[0]}: Bit {self.bit}, Length {self.length}, Position {self.position}"
# end class ISO8583Error