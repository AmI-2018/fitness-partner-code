import configparser


def config_write():

    config = configparser.ConfigParser()

    config['DEFAULT'] = {'minSdkVersion': '15',
                         'targetSdkVersion': '24',
                         'versionName': '1.0.0',
                         'server action': (0, 0, 0)}

    config['luzhuo.me'] = {}
    config['luzhuo.me']['user'] = 'luzhuo'

    config['mysql'] = {}
    topsecret = config['mysql']
    topsecret['ip'] = '127.0.0.1'
    topsecret['port'] = '3306'

    with open('config.ini', 'w') as configfile:
        config.write(configfile)


config = configparser.ConfigParser()
config.read('config.ini')

# config.set("LIGHT COLOR", "aerobic_color_range", str([102, 51, 204]))
config.set("LIGHT COLOR", "aerobic_color_range", str([102, 51, 204]))
config.write(open("config.ini", "w"))

print(config['LIGHT COLOR']['default_color'], type(list(config['LIGHT COLOR']['default_color'])))

for item in eval(config['LIGHT COLOR']['default_color']):
    print(item, type(item))

# If the key don't have a value, the result will be '', not None

print(int(''))