import os
import sys
from PIL import Image
from palette import get_closest_match


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
        self.width = end_x - start_x
        self.height = end_y - start_y
        self.x = start_x // 2 + end_x // 2
        self.y = start_y // 2 + end_y // 2
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


start_x = 394
start_y = 394
end_x = 1134
end_y = 1134

w = 740
h = 740

if __name__ == '__main__':
    try:
        image_path = sys.argv[1]
    except IndexError:
        print("Missing argument: image_path")
        sys.exit(1)

    if not os.path.exists(image_path):
        print(f"input image {image_path} does not exist.")
        sys.exit(1)

    img = Image.open(image_path)
    img_data = img.getdata()
    width, height = img.size
    pixels = list(img_data)
    pixels = [pixels[idx] for idx in range(0, len(list(img_data)), 2)]
    pixels = [get_closest_match(rgb) for rgb in pixels]
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    width = width // 2
    height = height // 2
    from math import ceil
    cell_width = ceil(w / width)
    cell_height = ceil(h / height)

    objects = [BannerBackground()]

    for y in range(0, height, 6):
        for x in range(0, width, 6):
            banner_object = BannerForegroundObject()
            banner_object.color1 = pixels[y][x]
            banner_object.color2 = pixels[y][x]
            banner_object.x = start_x + cell_width * 3 + (x * (cell_width-1))
            banner_object.y = start_y + cell_height * 3 + (y * (cell_height-1))
            banner_object.width = cell_width * 6
            banner_object.height = cell_height * 6
            banner_object.rotation = 0
            objects.append(banner_object)

    print(".".join([str(obj) for obj in objects]))

    image_name = os.path.splitext(os.path.basename(image_path))[0]

    with open(f"{image_name}.banner", "w+") as fh:
        fh.write(".".join([str(obj) for obj in objects]))
