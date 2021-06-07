from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image


def calculate_percent_diff(maxi, mini):

    if maxi == mini:
        return 100.0
    try:
        return (maxi / mini) * 100.0 - 100
    except ZeroDivisionError:
        return 0


def clear_older_data(*lists_to_clear, trigger_list, threshold):

    if len(trigger_list) >= threshold:

        del trigger_list[0]
        for list_to_clear in lists_to_clear:
            del list_to_clear[0]


def get_icons(*icon_names, transparent=True):

    processed_list = []
    for icon_name in icon_names:

        path = Path.cwd() / 'icons' / f'{icon_name}-256p.png'
        icon_image = Image.open(path)

        if transparent:
            alpha_channel = icon_image.getchannel('A')
            with_alpha = alpha_channel.point(lambda a: 32 if a > 0 else 0)
            icon_image.putalpha(with_alpha)

        processed_list.append(icon_image)

    return processed_list


def get_unix_time(timeframe):

    now = datetime.now()
    delta = timedelta(minutes=timeframe)

    return int((now - delta).timestamp()) * 1000
