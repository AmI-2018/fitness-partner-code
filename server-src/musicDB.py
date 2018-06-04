import pymysql
import os
import eyed3


def connect_to_db():
    # connect to data base
    conn = pymysql.connect(host='localhost'
                           , user='root'
                           , passwd='root'
                           , db='musicList')
    conn.set_charset('utf8')
    return conn


def select_music(HBR):
    # connect to data base
    conn = connect_to_db()

    # prepare a cursor object using cursor() method
    cursor = conn.cursor()

    get_word = "SELECT * FROM {table} ORDER BY RAND() LIMIT 1"

    if HBR < 100:
        table = "bpm_90_to_100"
    elif 100 <= HBR < 110:
        table = "bpm_100_to_110"
    elif 110 <= HBR < 120:
        table = "bpm_110_to_120"
    elif 120 <= HBR < 130:
        table = "bpm_120_to_130"
    elif 130 <= HBR < 140:
        table = "bpm_130_to_140"
    elif 140 <= HBR < 150:
        table = "bpm_140_to_150"
    elif 150 <= HBR < 160:
        table = "bpm_150_to_160"
    elif 160 <= HBR < 170:
        table = "bpm_160_to_170"
    elif 170 <= HBR < 180:
        table = "bpm_170_to_180"
    elif 180 <= HBR < 190:
        table = "bpm_180_to_190"
    else:
        table = "bpm_190_to_200"

    cursor.execute(get_word.format(table=table))
    result = cursor.fetchone()
    music_id = result[0]
    music_location = result[1]
    music_name = result[2]

    # print("id=%d, music_location=%s, music_name=%s" %
    #       (music_id, music_location, music_name))

    # disconnect from server
    cursor.close()

    return music_location, music_name


def scan_music(location):
    # connect to data base
    conn = connect_to_db()


    # prepare a cursor object using cursor() method
    cursor = conn.cursor()

    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    add_word = ("INSERT INTO {table} "
                "(id, music_location, music_name) "
                "VALUES (%(id)s, %(music_location)s, %(music_name)s)")

    truncate_table = "TRUNCATE TABLE {table}"

    for root, dirs, files in os.walk(location):
        for name in dirs:
            music_direction = os.path.join(root, name)
            table = name
            data_word = {}
            print(music_direction)
            print(table)
            cursor.execute(truncate_table.format(table=table))

            files = os.listdir(music_direction)
            music_id = 1
            for file in files:
                data_word["id"] = str(music_id)

                music_location = os.path.join(music_direction, file)
                data_word["music_location"] = music_location

                audio_file = eyed3.load(music_location)
                data_word["music_name"] = audio_file.tag.title

                music_id += 1
                print(data_word)

                # Execute the command
                cursor.execute(add_word.format(table=table), data_word)

                # Update to database
                conn.commit()

    # disconnect from server
    cursor.close()


if __name__ == "__main__":

    scan_music("C:\AMI\music")

    a, b = select_music(175)

    print(a, b)
