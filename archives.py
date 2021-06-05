import json


def get_archive(currency=None):
    archive_file = open("data/archives.json", "r")
    archive_data = json.load(archive_file)
    archive_file.close()

    if currency is None:
        return archive_data
    elif currency in archive_data.keys():
        return archive_data[currency]
    else:
        print("There is nothing to show")
        return {}


def archive(currency, transactions):
    archive_file = open("data/archives.json", "r")
    archive_data = json.load(archive_file)
    archive_file.close()

    if currency not in archive_data.keys():
        archive_data[currency] = list()

    for transaction in transactions:
        archive_data[currency].append(transaction)

    archive_file = open("data/archives.json", "w")
    json.dump(archive_data, archive_file)
    archive_file.close()