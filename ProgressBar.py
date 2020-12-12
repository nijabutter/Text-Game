class ProgressBar:
    def __init__(self,maximum=100, value=0, width=100, empty="░", full="█"):
        self.width = width
        self.empty = empty
        self.full = full
        self.value = value
        self.maximum = maximum

    def get(self):
        percent = float(self.value) / float(self.maximum)
        fill = int(percent * self.width)
        if fill > self.width:
            fill = self.width
        return (self.full * fill) + (self.empty * (self.width-fill)) + " " + str(int(percent*100)) + "%"