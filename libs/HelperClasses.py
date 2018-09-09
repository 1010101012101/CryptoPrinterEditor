class Translator:
    def __init__(self, leftMin, leftMax, rightMin, rightMax):
        self.leftMin = leftMin
        self.leftMax = leftMax
        self.rightMin = rightMin
        self.rightMax = rightMax

    #https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another#1969274 thanks good sir
    def t(self, value):
        # Figure out how 'wide' each range is
        leftSpan = self.leftMax - self.leftMin
        rightSpan = self.rightMax - self.rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - self.leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return self.rightMin + (valueScaled * rightSpan)