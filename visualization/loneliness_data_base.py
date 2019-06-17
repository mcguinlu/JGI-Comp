import pymysql
import requests
import xlrd
from ipython_genutils.py3compat import xrange
from geopy.geocoders import Nominatim
import time
import json
sql_db = None


def get_geoloc_data(post_code):
    with open("geo.data") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for item in content:
        temp = item.replace(']', '').replace('[', '').replace('\'', '').split(',')
        if len(temp) == 5:
            item = [temp[0]+","+temp[1]+","+temp[2], temp[3], temp[4]]
        if len(temp) == 4:
            item = [temp[0] + "," + temp[1], temp[2], temp[3]]
        if post_code in item[0]:
            f.close()
            result = [str(item[0]), float(item[1]), float(item[2])]
            print(result)
            return result

    URL = "https://api.opencagedata.com/geocode/v1/json"
    #9db9eeeac8664464b08912ea7f3d1cd1
    key = "0c3808834cef4078812f6cd9e4ca9d6a"
    PARAMS = {'key': key, 'q': post_code+"country_code=gb"}
    print(PARAMS)
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    result = None
    if len(data["results"]) == 0:
        URL = "https://api.opencagedata.com/geocode/v1/json"
        PARAMS = {'key': key, 'q': post_code.split(' ')[0]}
        print(PARAMS)
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()
        result = None

    for elem in data["results"]:
        # print(elem["components"]["country_code"])
        if elem["components"]["country_code"] != 'gb':
            continue
        result = [str(elem["formatted"]), float(elem["geometry"]["lat"]), float(elem["geometry"]["lng"])]

    print(result)
    with open('geo.data', 'a') as outfile:
        outfile.write("[%s]" % ','.join([str(x) for x in result]))
        outfile.write('\n')
    outfile.close()

    return result


def get_geoloc_data_migration(place):
    URL = "https://api.opencagedata.com/geocode/v1/json"
    #9db9eeeac8664464b08912ea7f3d1cd1
    key = "0c3808834cef4078812f6cd9e4ca9d6a"
    PARAMS = {'key': key, 'q': place}
    print(PARAMS)
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    result = None

    for elem in data["results"]:
        result = [str(elem["formatted"]), float(elem["geometry"]["lat"]), float(elem["geometry"]["lng"])]
        print(result)

    return result


def execute_sql_query(query, records=None, log_enabled=False):
    try:
        global sql_db
        cursor = sql_db.cursor()
        if records is not None:
            if log_enabled:
                print("SQL Query: %s" % query, records[0])
            cursor.executemany(query, records)
        else:
            if log_enabled:
                print("SQL Query: %s" % query)
            cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            if log_enabled:
                print("SQL Answer: %s" % row)
        return rows
    except Exception as e:
        print("Exeception occured:{}".format(e))


def sql_db_flush():
    global sql_db
    sql_db.commit()


def drop_table(table_name):
    print("drop %s..." % table_name)
    execute_sql_query("DROP TABLE `%s`" % table_name)


def drop_all_tables(db_name):
    print("drop all tables in db...")
    tables = execute_sql_query("SHOW TABLES")
    for table in tables:
        name = table["Tables_in_%s" % db_name]
        execute_sql_query("DROP TABLE `%s`" % name)


def create_sql_table(name):
    print("creating sql table %s" % name)
    execute_sql_query("CREATE TABLE `%s` ("
                      "id INT AUTO_INCREMENT PRIMARY KEY,"
                      "pcstrip VARCHAR(8),"
                      "year INT,"
                      "number_of_patients FLOAT,"
                      "sha VARCHAR(4),"
                      "ptc VARCHAR(4),"
                      "oseast1m INT,"
                      "osnrth1m INT,"
                      "lsoa11 VARCHAR(9),"
                      "msoa11 VARCHAR(9),"
                      "ru11ind VARCHAR(2),"
                      "rgn VARCHAR(9),"
                      "laua VARCHAR(9),"
                      "imd INT,"
                      "depression_perc FLOAT,"
                      "alzheimers_perc FLOAT,"
                      "blood_pressure_perc FLOAT,"
                      "hypertension_perc FLOAT,"
                      "diabetes_perc FLOAT,"
                      "cardiovascular_disease_perc FLOAT,"
                      "insomnia_perc FLOAT,"
                      "addiction_perc FLOAT,"
                      "social_anxiety_perc FLOAT,"
                      "loneliness_perc FLOAT,"
                      "depression_zscore FLOAT,"
                      "alzheimers_zscore FLOAT,"
                      "blood_pressure_zscore FLOAT,"
                      "hypertension_zscore FLOAT,"
                      "diabetes_zscore FLOAT,"
                      "cardiovascular_disease_zscore FLOAT,"
                      "insomnia_zscore FLOAT,"
                      "addiction_zscore FLOAT,"
                      "social_anxiety_zscore FLOAT,"
                      "loneliness_zscore FLOAT,"
                      "loneills FLOAT,"
                      "place_name VARCHAR(255),"
                      "latitude FLOAT,"
                      "longitude FLOAT"
                      ")" % name)


def create_sql_table_student_migration(name):
    print("creating sql table %s" % name)
    execute_sql_query("CREATE TABLE `%s` ("
                      "id INT AUTO_INCREMENT PRIMARY KEY,"
                      "4_way_domicile VARCHAR(255),"
                      "domicile VARCHAR(255),"
                      "level_of_study VARCHAR(255),"
                      "mode_of_study VARCHAR(255),"
                      "academic_year INT,"
                      "region_of_he_provider VARCHAR(255),"
                      "number INT,"
                      "domicile_lat FLOAT,"
                      "domicile_long FLOAT,"
                      "region_of_he_provider_lat FLOAT,"
                      "region_of_he_provider_long FLOAT"

                      ")" % name)


def insert_record_to_sql_table(table_id, records):
    print("inserting %d records to table %s" % (len(records), table_id))
    query = "INSERT INTO `" + table_id + "` (pcstrip, year, number_of_patients, sha, ptc, oseast1m, osnrth1m, lsoa11, msoa11, " \
                                         "ru11ind, rgn, laua, imd, depression_perc, alzheimers_perc, blood_pressure_perc, " \
                                         "hypertension_perc, diabetes_perc, cardiovascular_disease_perc, insomnia_perc, " \
                                         "addiction_perc, social_anxiety_perc, loneliness_perc, depression_zscore, " \
                                         "alzheimers_zscore, blood_pressure_zscore, hypertension_zscore, diabetes_zscore, " \
                                         "cardiovascular_disease_zscore,insomnia_zscore, addiction_zscore, social_anxiety_zscore, " \
                                         "loneliness_zscore, loneills, place_name," \
                                         " latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                                         " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                                         " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    execute_sql_query(query, records)


def insert_record_to_sql_table_student_migration(table_id, records):
    print("inserting %d records to table %s" % (len(records), table_id))
    query = "INSERT INTO `" + table_id + "` (4_way_domicile, domicile, level_of_study, mode_of_study, academic_year," \
                                         " region_of_he_provider, number, domicile_lat, domicile_long," \
                                         " region_of_he_provider_lat," \
                                         " region_of_he_provider_long) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    execute_sql_query(query, records)


def create_and_connect_to_sql_db(db_name):
    print("CREATE DATABASE %s..." % db_name)
    # Create a connection object
    db_server_name = "localhost"
    db_user = "axel"
    db_password = "Mojjo@2015"
    char_set = "utf8mb4"
    cusror_type = pymysql.cursors.DictCursor
    global sql_db
    sql_db = pymysql.connect(host=db_server_name, user=db_user, password=db_password)
    execute_sql_query('CREATE DATABASE IF NOT EXISTS %s' % db_name)
    connect_to_sql_database(db_server_name, db_user, db_password, db_name, char_set, cusror_type)


def connect_to_sql_database(db_server_name, db_user, db_password, db_name, char_set, cusror_type):
    print("connecting to db %s..." % db_name)
    global sql_db
    sql_db = pymysql.connect(host=db_server_name, user=db_user, password=db_password,
                             db=db_name, charset=char_set, cursorclass=cusror_type)


def format_postcode(input):
    array = list(input)
    array.insert(len(input)-3, ' ')
    result = ''.join(array)
    return result


def generate_data_table_from_xlsx(path):
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(1)
    data = []
    print("reading file...")
    for row_index in xrange(0, sheet.nrows):
        if row_index == 0:
            continue
        row = [sheet.cell(row_index, col_index).value for col_index in xrange(0, sheet.ncols)]
        postal_code = format_postcode(row[0].strip())
        geo_data = get_geoloc_data(postal_code)
        row.extend(geo_data)
        data.append(tuple(row))

    print("finished reading. start appending SQL database...")
    insert_record_to_sql_table("final_data", data)
    sql_db_flush()


def clean(input):
    return input.replace(' not otherwise specified', '').replace('Antarctica and ', '').replace(', Banbridge and Craigavon', '').replace(' (Except Middle East)', '').replace(' [Bolivia, Plurinational State of]', '').replace('[Brunei Darussalam]', '').replace(' [Myanmar]', '').replace(' (European Union)', '').replace(' [Timor Leste]', '').replace(' (Non-European Union)', '').replace(' [Iran, Islamic Republic of]', '').replace(' [Korea, Democratic People\'s Republic of]', '').replace(' [Macedonia, The Former Yugoslav Republic of]', '').replace(' [Micronesia, Federated States of]', '').replace(' [Korea, Republic of]', '').replace(' (district council area unknown)', '').replace(' [Russian Federation]', '').replace(' (French Part) [St Martin]', '').replace(' [Syrian Arab Republic]', '').replace(' (council area unknown)', '').replace(' [Virgin Islands, U. S.]', '').replace(' [Viet Nam]', '').replace(' (unitary authority unknown)', '').replace(' [Tanzania, United Republic of]', '').replace(' [Holy See (Vatican City State)]', '').replace(' [Venezuela, Bolivarian Republic of]', '').replace('Occupied Palestinian Territories [Palestine, State of]', 'Palestine').replace('Pitcairn, Henderson, Ducie and Oeno Islands [Pitcairn]', 'Pitcairn').replace(' (county/unitary authority unknown)', '').replace(' (Special Administrative Region of China) [Hong Kong]', '').replace(' (Special Administrative Region of China) [Macao]', '').replace(' [Virgin Islands, British]', '')


def generate_student_migation_data_table_from_xlsx(path):
    print('generate_student_migation_data_table_from_xlsx')
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(0)
    data = []
    region_of_he_provider_list = []
    domicile_list = []
    geolocator = Nominatim(user_agent=__name__)

    print("reading file...")
    for row_index in xrange(0, sheet.nrows):
        if row_index < 18:
            continue
        row = [sheet.cell(row_index, col_index).value for col_index in xrange(0, sheet.ncols)]
        a_way_domicile = row[0]
        domicile = row[1]
        domicile_list.append(clean(domicile))
        level_of_study = row[2]
        mode_of_study = row[3]
        academic_year = int(row[4].split('/')[0])
        region_of_he_provider = row[5]
        if 'Total England' in region_of_he_provider:
            region_of_he_provider = 'England'

        if 'Total United Kingdom' in region_of_he_provider:
            region_of_he_provider = 'United Kingdom'
        region_of_he_provider_list.append(region_of_he_provider)
        number = int(row[6])
        data.append([a_way_domicile, domicile, level_of_study, mode_of_study, academic_year, region_of_he_provider, number])

    region_of_he_provider_list = list(set(region_of_he_provider_list))
    region_of_he_provider_list.sort()
    domicile_list = list(set(domicile_list))
    domicile_list.sort()

    with open("geolocator.data") as f:
        content = f.readlines()
    latitudes_longitudes_dom = [json.loads(x.strip()) for x in content][0]

    for place in domicile_list:
        print(place)
        if place not in latitudes_longitudes_dom:
            location = geolocator.geocode(place, timeout=None)
            latitudes_longitudes_dom[place] = {'lat': location.latitude, 'long': location.longitude}
            print('cache...')
            with open('geolocator.data', 'w') as outfile:
                outfile.write(json.dumps(latitudes_longitudes_dom))
            outfile.close()
            time.sleep(1.1)
        else:
            print(place, latitudes_longitudes_dom[place])
            # get_geoloc_data_migration(place)

    latitudes_longitudes_he = {}
    for place in region_of_he_provider_list:
        if 'Total England' in place:
            place = 'England'

        if 'Total United Kingdom' in place:
            place = 'United Kingdom'

        # get_geoloc_data_migration(place)
        location = geolocator.geocode(place + ' , UK', timeout=None)
        print(place, '-', location)
        latitudes_longitudes_he[place] = {'lat': location.latitude, 'long': location.longitude}
        time.sleep(1.1)

    final_data = []
    for item in data:
        place = item[5]
        if 'Total England' in place:
            place = 'England'
        if 'Total United Kingdom' in place:
            place = 'United Kingdom'
        dom_c = latitudes_longitudes_dom[clean(item[1])]
        item.append(dom_c['lat'])
        item.append(dom_c['long'])
        he_c = latitudes_longitudes_he[clean(place)]
        item.append(he_c['lat'])
        item.append(he_c['long'])
        item[1] = clean(item[1])
        if 'Caribbean' in item[1]:
            print(item)
        final_data.append(tuple(item))


    print("finished reading. start appending SQL database...")
    insert_record_to_sql_table_student_migration("student_migration", final_data)
    sql_db_flush()


if __name__ == '__main__':
    print("start...")
    print(__name__)
    db_name = "loneliness"
    create_and_connect_to_sql_db(db_name)
    drop_table('student_migration')
    create_sql_table_student_migration('student_migration')
    generate_student_migation_data_table_from_xlsx("C:/Users/fo18103/PycharmProjects/loneliness/src/table-11.xlsx")
    # drop_all_tables(db_name)
    # create_sql_table("final_data")
    # generate_table_from_xlsx("C:/Loneliness/final_data.xlsx")

