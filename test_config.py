import configparser


def read_ini(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)

    return config

cin = read_ini('config.ini')
print(cin['WINDOW']['TIME'])
