class Color:
    AllColors = []
    
    def __init__(self, RightAngle, LeftAngle):
        self.LeftAngle = LeftAngle
        self.RightAngle = RightAngle
        self.PixelCount = 0
        self.__AddColorToAllColors()

    #private
    def __AddColorToAllColors(self): 
        Color.AllColors.append(self)

    def PrintAllColors():
        print(Color.AllColors)

    def PrintPixelCount(self):
        print('total pixelcount is', self.PixelCount)

    def PrintLeftAngle(self):
        print('LeftAngle is :', self.LeftAngle)

    def PrintRightAngle(self):
        print('RightAngle is : ', self.RightAngle)



















    

        


