def banner_bool_str(boolean: bool) -> str:
    return "1" if boolean else "0"


class BackgroundShapes:
    SOLID = 11


class ForegroundShapes:
    SQUARE = 505


class BannerObject:
    def __init__(self):
        self.shape = 0
        self.color1 = 0
        self.color2 = 0
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.stroke = False
        self.mirror = False
        self.rotation = 0

    def __str__(self):
        return ".".join(
            [
                str(self.shape),
                str(self.color1),
                str(self.color2),
                str(self.width),
                str(self.height),
                str(self.x),
                str(self.y),
                banner_bool_str(self.stroke),
                banner_bool_str(self.mirror),
                str(self.rotation)
            ]
        )


class BannerBackground(BannerObject):
    def __init__(self, shape=None):
        super().__init__()
        if shape:
            self.shape = shape
        else:
            self.shape = BackgroundShapes.SOLID


class BannerForegroundObject(BannerObject):
    def __init__(self, shape=None):
        super().__init__()
        if shape:
            self.shape = shape
        else:
            self.shape = ForegroundShapes.SQUARE
