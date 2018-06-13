import configparser


def config_write(title, key, value):
    config = configparser.ConfigParser()
    config.read('config.ini')

    config[title][key] = str(value)

    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def config_read(title, key):
    config = configparser.ConfigParser()
    config.read('config.ini')

    return config[title][key]


def reset_config():
    # [LIGHT COLOR]
    config_write("LIGHT COLOR", "default_color", "")
    config_write("LIGHT COLOR", "anaerobic_color", "")
    config_write("LIGHT COLOR", "maximum_color", "")
    config_write("LIGHT COLOR", "aerobic_color_range", "")
    config_write("LIGHT COLOR", "anaerobic_color_range", "")

    # [BODY INFO]
    config_write("BODY INFO", "rest_heartbeat_rate", "")
    config_write("BODY INFO", "aerobic_start", "")
    config_write("BODY INFO", "maximum_heart_beat", "")

    # [SPORT INFO]
    config_write("SPORT INFO", "warm_up_time", "")
    config_write("SPORT INFO", "rest_time", "")

    # [FITBIT ACCOUNT]
    config_write("FITBIT ACCOUNT", "fitbit_is_initialized", "")
    config_write("FITBIT ACCOUNT", "fitbit_user_secret", "")
    config_write("FITBIT ACCOUNT", "fitbit_user_id", "")


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    # config.set("LIGHT COLOR", "aerobic_color_range", str([102, 51, 204]))
    config.set("LIGHT COLOR", "aerobic_color_range", str([102, 51, 204]))
    config.write(open("config.ini", "w"))

    print(config['LIGHT COLOR']['default_color'], type(list(config['LIGHT COLOR']['default_color'])))

    for item in eval(config['LIGHT COLOR']['default_color']):
        print(item, type(item))

    # If the key don't have a value, the result will be '', not None

