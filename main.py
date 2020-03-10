import psycopg2

host = "localhost"
port = 5432
user = "postgres"
pw = "semmi"
db = "tornabarakony"

conn = psycopg2.connect(host=host, port=port, user=user, dbname=db, password=pw)
cursor = conn.cursor()

def get_all_pois():

    cursor.execute("SELECT * FROM pois")
    results = cursor.fetchall()
    return results

def get_poi_by_id(id):

    cursor.execute("Select * FROM pois WHERE id = {0}".format(id))
    result = cursor.fetchone()
    return result

def insert_poi(name, type, condition, active, x_coord, y_coord):

    insert = '''INSERT INTO pois (name, type, condition, active, geom) 
    VALUES 
    ('{0}', '{1}', {2}, {3}, ST_SetSRID(ST_MakePoint({4}, {5}), 23700))'''.format(
        name, type, condition, active, x_coord, y_coord
    )

    cursor.execute(insert)
    conn.commit()

def delete_poi_by_id(id):

    delete = "DELETE FROM pois WHERE id = {0}".format(id)

    cursor.execute(delete)
    conn.commit()

def update_poi_by_id(id, name, type, condition, active, x_coord, y_coord):

    update = '''
        UPDATE pois SET 
            name = '{0},
            type = '{1}',
            condition = {2},
            active = {3},
            geom = ST_SetSRID(ST_MakePoint({4}, {5}), 23700))
        WHERE
            id = {6}
    '''.format(name, type, condition, active, x_coord, y_coord, id)

    cursor.execute(update)
    conn.commit()

insert_poi("DTE", "university", 5, True, 800000, 230000)
get_all_pois()
poi3 = get_poi_by_id(7)
print(poi3)
delete_poi_by_id(3)

