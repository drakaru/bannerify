import os
import sys
from math import ceil, floor

from PIL import Image
from PIL.Image import LANCZOS

from palette import get_closest_match
from banner import BannerBackground, BannerForegroundObject


# Bannerlord hardcaps to 400 objects, including the background.
object_limit = 400


start_x = 394
start_y = 394
end_x = 1134
end_y = 1134

w = 740
h = 740


def most_common(objects):
    colours = {}
    for object in objects[1:]:
        count = colours.get(object.color1, 0)
        colours[object.color1] = count+1
    highest = None
    count = 0
    for k,v in colours.items():
        if v > count:
            count = v
            highest = k
    return highest


def clamp(lower, upper, v):
    return max(min(v, upper), lower)


def lerp(start, end, t):
    t = clamp(0, 1, t)
    return start * (1 - t) + end * t


if __name__ == '__main__':
    try:
        image_path = sys.argv[1]
    except IndexError:
        print("Missing argument: image_path")
        sys.exit(1)

    if not os.path.exists(image_path):
        print(f"input image {image_path} does not exist.")
        sys.exit(1)

    image = Image.open(image_path)

    sampled_image = image.resize((20, 20), Image.LANCZOS)
    img_data = sampled_image.getdata()
    width, height = sampled_image.size

    pixels = list(img_data)
    pixels = [get_closest_match(rgb) for rgb in pixels]
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    cell_width = ceil(w / width)
    cell_height = ceil(h / height)

    objects = []
    background = BannerBackground()
    background.width = end_x - start_x
    background.height = end_y - start_y
    background.x = start_x // 2 + end_x // 2
    background.y = start_y // 2 + end_y // 2
    objects.append(background)

    for y in range(0, height):
        for x in range(0, width):
            x1t = 0 if x == 0 else x/width
            y1t = 0 if y == 0 else y/height
            x2t = (x+1) / width
            y2t = (y+1) / height

            p1x = ceil(lerp(start_x, end_x, x1t))
            p1y = ceil(lerp(start_y, end_y, y1t))
            p2x = ceil(lerp(start_x, end_x, x2t))
            p2y = ceil(lerp(start_y, end_y, y2t))
            w = p2x - p1x
            h = p2y - p1y

            banner_object = BannerForegroundObject()
            banner_object.color1 = pixels[y][x]
            banner_object.color2 = pixels[y][x]
            banner_object.x = p1x + ceil(w/2)
            banner_object.y = p1y + ceil(h/2)
            banner_object.width = w+2
            banner_object.height = h+2
            banner_object.rotation = 0
            objects.append(banner_object)

    print(len(objects))

    commonest_colour = most_common(objects)
    objects = list(filter(lambda x: x.color1 != commonest_colour, objects))
    objects[0].color1 = commonest_colour
    objects[0].color2 = commonest_colour

    print(len(objects))

    code = ".".join([str(obj) for obj in objects])
    print(len(code))
    print(code)

    image_name = os.path.splitext(os.path.basename(image_path))[0]

    with open(f"{image_name}.banner", "w+") as fh:
        fh.write(code)
