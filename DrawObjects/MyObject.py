class MyObject:
    def __init__(self):
        self.myObj = None

    def getAndDraw(self):
        self.myObj.Draw()
        self.setAttributes()
        return self.myObj

    def setAttributes(self):
        pass
