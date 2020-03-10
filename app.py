import psycopg2
from flask import Flask, request
import json
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

host = "localhost"
port = 5432
user = "postgres"
pw = "semmi"
db = "tornabarakony"

conn = psycopg2.connect(host=host, port=port,
                        user=user, dbname=db, password=pw)
cursor = conn.cursor(cursor_factory=RealDictCursor)


@app.route('/pois')
def get_all_pois():
    # print("FUT")
    query = '''SELECT
                id,
                name,
                type,
                condition,
                active,
                ST_X(ST_Transform(geom, 4326)) as x,
                ST_Y(ST_Transform(geom, 4326)) as y,
                extract(epoch from create_time) as create_time,
                extract(epoch from last_updated) as last_updated
            FROM pois'''
    cursor.execute(query)

    results = cursor.fetchall()
    return json.dumps(results)

@app.route('/pois/<int:id>')
def get_poi_by_id(id):

    cursor.execute('''SELECT
                id,
                name,
                type,
                condition,
                active,
                ST_X(ST_Transform(geom, 4326)) as x,
                ST_Y(ST_Transform(geom, 4326)) as y,
                extract(epoch from create_time) as create_time,
                extract(epoch from last_updated) as last_updated
            FROM pois WHERE id = {0}'''.format(id))
    result = cursor.fetchone()
    return result

@app.route('/create', methods=['POST'])
def insert_poi():

    name = request.args.get('name')
    type = request.args.get('type')
    condition = request.args.get('condition')
    active = request.args.get('active')
    x_coord = request.args.get('x_coord')
    y_coord = request.args.get('y_coord')

    insert = '''INSERT INTO pois (name, type, condition, active, geom) 
    VALUES 
    ('{0}', '{1}', {2}, {3}, ST_SetSRID(ST_MakePoint({4}, {5}), 23700))'''.format(
        name, type, condition, active, x_coord, y_coord
    )

    cursor.execute(insert)
    conn.commit()

    return '{"success":true}'

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_poi_by_id(id):

    delete = "DELETE FROM pois WHERE id = {0}".format(id)

    cursor.execute(delete)
    conn.commit()

    return '{"success":true}'

@app.route('/update/<int:id>', methods = ['PUT'])
def update_poi_by_id(id):

    name = request.args.get('name')
    type = request.args.get('type')
    condition = request.args.get('condition')
    active = request.args.get('active')
    x_coord = request.args.get('x_coord')
    y_coord = request.args.get('y_coord')

    update = '''
        UPDATE pois SET 
            name = '{0}',
            type = '{1}',
            condition = {2},
            active = {3},
            geom = ST_SetSRID(ST_MakePoint({4}, {5}), 23700),
            last_updated = NOW()
        WHERE
            id = {6}
    '''.format(name, type, condition, active, x_coord, y_coord, id)

    cursor.execute(update)
    conn.commit()

    return '{"success":true}'

# insert_poi("DTE", "university", 5, True, 800000, 230000)
# get_all_pois()
# poi3 = get_poi_by_id(7)
# print(poi3)
# delete_poi_by_id(3)
