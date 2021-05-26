from PIL import Image
from pathlib import Path


def calculate_percent_diff(maxi, mini):
    if maxi == mini:
        return 100.0
    try:
        return (maxi / mini) * 100.0 - 100
    except ZeroDivisionError:
        return 0


def get_icons(*icon_names, transparent=True):

    processed_list = []
    for icon_name in icon_names:

        path = Path.cwd() / 'icons' / f'{icon_name}-256p.png'
        icon_image = Image.open(path)

        if transparent:
            alpha_channel = icon_image.getchannel('A')
            with_alpha = alpha_channel.point(lambda i: 32 if i > 0 else 0)
            icon_image.putalpha(with_alpha)

        processed_list.append(icon_image)

    return processed_list

