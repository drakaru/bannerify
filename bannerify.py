import os
import sys
from math import ceil

from PIL import Image

from palette import get_closest_match
from banner import BannerBackground, BannerForegroundObject

# Turn an image into a bannerlord banner!
#
# M&B accepts banners in the form of codes.
#
# codes are dot separated values (ints) which form "objects", like so:
# shape.color1.color2.width.height.x.y.stroke.mirror.rotation

# banners are limited to 400 "objects", background inclusive.
object_limit = 400
# the first object is the background
#
# colors are paletted, with a 159 colors in total (see palette.py)

# defines the 740x740 area in the middle of the flag
# it can be extended horizontally on the flag and various contexts has differing UVs
# ie, shields, soldier icons, etc
start_x = 394
start_y = 394
end_x = 1134
end_y = 1134


def most_common(objects):
    """return the most common color present in a banner"""
    colors = {}
    for banner_object in objects[1:]:
        count = colors.get(banner_object.color1, 0)
        colors[banner_object.color1] = count+1
    highest = None
    count = 0
    for k, v in colors.items():
        if v > count:
            count = v
            highest = k
    return highest


def clamp(lower, upper, v):
    return max(min(v, upper), lower)


def lerp(start, end, t):
    t = clamp(0, 1, t)
    return start * (1 - t) + end * t


def bannerify(sampled_image):

    img_data = sampled_image.getdata()
    width, height = sampled_image.size

    pixels = list(img_data)
    pixels = [get_closest_match(rgb) for rgb in pixels]
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    objects = []
    background = BannerBackground()
    background.width = 1528  # end_x - start_x
    background.height = end_y - start_y
    background.x = start_x // 2 + end_x // 2
    background.y = start_y // 2 + end_y // 2 - 20
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
            banner_object.y = p1y - ceil(h/2)
            banner_object.width = w+2
            banner_object.height = h+2
            banner_object.rotation = 0
            objects.append(banner_object)

    pre_opt_objects = len(objects)

    # simplest optimisation
    # TODO : investigate better methods
    commonest_color = most_common(objects)
    objects = list(filter(lambda x: x.color1 != commonest_color, objects))
    objects[0].color1 = commonest_color
    objects[0].color2 = commonest_color

    post_opt_objects = len(objects)

    objects = objects if post_opt_objects < object_limit else None

    if objects:
        percent_saved = (pre_opt_objects - post_opt_objects) / pre_opt_objects * 100
        print(f"{width}x{height}: {post_opt_objects}: {percent_saved:0.2f}% saved.")
    else:
        print(f"{width}x{height}: {post_opt_objects}: failed.")

    return objects


def iterative_bannerify(image):
    width = 20
    height = 20
    final_banner = None
    while True:
        sampled_image = image.resize((width, height), Image.LANCZOS)
        candidate = bannerify(sampled_image)
        if not candidate:
            break
        final_banner = candidate
        if width == height:
            width = width + 1
        else:
            height = height + 1

    return final_banner


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
    banner = iterative_bannerify(image)

    code = ".".join([str(obj) for obj in banner])
    print()
    print(code)

    image_name = os.path.splitext(os.path.basename(image_path))[0]

    with open(f"{image_name}.banner", "w+") as fh:
        fh.write(code)
