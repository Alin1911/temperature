from flask import Flask
import mysql.connector
import json
from datetime import datetime
from flask import request, jsonify, Response

app = Flask(__name__)


def connect_to_database():
    connection = mysql.connector.connect(host='db',
                                         database='db',
                                         port=3306,
                                         auth_plugin='mysql_native_password',
                                         user='user',
                                         password='password'
                                         )
    return connection

def close_connection(connection):
    connection.close()

#countries api
@app.route('/api/countries', methods=["POST"])
def postCountries():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        payload = request.get_json(silent=True)
        size = len(payload) - 1
        i = 0
        query = 'INSERT INTO Tari ('
        for key in payload.keys():
            if key == "nume":
                query += 'nume_tara'
            elif key == "lat":
                query += 'latitudine'
            elif key == "lon":
                query += 'longitudine '
                    
            if i < size:
                query +=','
            i += 1
        query += ') VALUES ('
        i = 0
        for value in payload.values():
            if isinstance(value, str):
                query +=  '"' + str(value) + '"'
            else:
                query +=  str(value)
            if i < size:
                query +=','
            i += 1
        query += ')'
        cursor.execute(query)
        connection.commit()

        cursor.execute('SELECT * FROM Tari WHERE nume_tara LIKE "' + str(payload['nume'] + '"'))
        results =  cursor.fetchone()

        cursor.close()
        close_connection(connection)
        return {"id" : str(results[0])}, 201
    except:
        return Response(status=400)

@app.route('/api/countries', methods=["GET"])
def getCountries():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM Tari')

        item = cursor.fetchone()
        re = []
        while item:
            re.append({
                'id' : str(item[0]),
                'nume': item[1],
                'lat': item[2],
                'lon': item[3]})
            item = cursor.fetchone()
        cursor.close()
        close_connection(connection)
        return  json.dumps(re), 200
    except:
        return Response(status=400)

@app.route('/api/countries/<int:id>', methods=["PUT"])
def putCountries(id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        payload = request.get_json(silent=True)

        query = 'UPDATE Tari SET '
        num = len(payload)
        if payload.get('id'):
            query += 'id=' + str(payload.get('id'))
            if num > 1:
                query +=', '
                num -= 1

        if payload.get('nume'):
            query += 'nume_tara="' + str(payload.get('nume')) + '"'
            if num > 1:
                query +=', '
                num -= 1

        if payload.get('lat'):
            query += 'latitudine=' + str(payload.get('lat')) + ' '
            if num > 1:
                query +=', '
                num -= 1
        if payload.get('lon'):
            query += 'longitudine=' + str(payload.get('lon')) + ' '
            if num > 1:
                query +=', '
                num -= 1
        query += 'WHERE id=' + str(id)

        cursor.execute(query)
        connection.commit()

        cursor.close()
        close_connection(connection)
        return Response(status=200)
    except:
        return Response(status=400)

@app.route('/api/countries/<int:id>', methods=["DELETE"])
def deleteCountries(id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        query = 'DELETE FROM Tari WHERE id='+ str(id)
        cursor.execute(query)
        connection.commit()

        cursor.close()
        close_connection(connection)
        return Response(status=200)
    except:
        return Response(status=400)

#Cities
@app.route('/api/cities', methods=["POST"])
def postCities():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        payload = request.get_json(silent=True)
        cursor.execute('SELECT 1 FROM Tari where id =' + str(payload.get('idTara')))
        if cursor.fetchone() == None:
            return Response(status=400)
        query = 'INSERT INTO Orase (nume_oras, id_tara, latitudine, longitudine) VALUES (%s, %s, %s, %s)'
        values = (str(payload.get('nume')), str(payload.get('idTara')), str(payload.get('lat')), str(payload.get('lon')))
        cursor.execute(query, values)
        connection.commit()

        cursor.execute('SELECT * FROM Orase WHERE nume_oras LIKE "' + str(payload.get('nume') + '"'))
        results =  cursor.fetchone()

        cursor.close()
        close_connection(connection)
        return {"id" : str(results[0])}, 201
    except:
        return Response(status=400)

@app.route('/api/cities', methods=["GET"])
def getCities():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM Orase')
        item = cursor.fetchone()
        re = []
        while item:
            re.append({
                'id' : str(item[0]),
                'idTara': item[1],
                'nume': item[2],
                'lat': item[3],
                'lon': item[4]
                })
            item = cursor.fetchone()
        cursor.close()
        close_connection(connection)
        return  json.dumps(re), 200
    except:
        return Response(status=400)


@app.route('/api/cities/country/<int:id>', methods=["GET"])
def getCitiesByCountry(id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM Orase where id_tara=' + str(id))
        item = cursor.fetchone()
        re = []
        while item:
            re.append({
                'id' : str(item[0]),
                'idTara': item[1],
                'nume': item[2],
                'lat': item[3],
                'lon': item[4]
                })
            item = cursor.fetchone()
        cursor.close()
        close_connection(connection)
        return  json.dumps(re), 200
    except:
        return Response(status=400)

@app.route('/api/cities/<int:id>', methods=["PUT"])
def putCities(id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        payload = request.get_json(silent=True)

        query = 'UPDATE Orase SET '
        num = len(payload)
        if payload.get('id'):
            query += 'id=' + str(payload.get('id'))
            if num > 1:
                query +=', '
                num -= 1
    
        if payload.get('idTara'):
            query += 'id_tara="' + str(payload.get('idTara')) + '"'
            if num > 1:
                query +=', '
                num -= 1

        if payload.get('nume'):
            query += 'nume_oras="' + str(payload.get('nume')) + '"'
            if num > 1:
                query +=', '
                num -= 1

        if payload.get('lat'):
            query += 'latitudine=' + str(payload.get('lat')) + ' '
            if num > 1:
                query +=', '
                num -= 1
        if payload.get('lon'):
            query += 'longitudine=' + str(payload.get('lon')) + ' '
            if num > 1:
                query +=', '
                num -= 1
        query += 'WHERE id=' + str(id)

        cursor.execute(query)
        connection.commit()

        cursor.close()
        close_connection(connection)
        return Response(status=200)
    except:
        return Response(status=400)

@app.route('/api/cities/<int:id>', methods=["DELETE"])
def deleteCities(id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        query = 'DELETE FROM Orase WHERE id='+ str(id)
        cursor.execute(query)
        connection.commit()

        cursor.close()
        close_connection(connection)
        return Response(status=200)
    except:
        return Response(status=400)

#Temperatures
@app.route('/api/temperatures', methods=["POST"])
def postTemperatures():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        payload = request.get_json(silent=True)
        cursor.execute('SELECT 1 FROM Orase where id =' + str(payload.get('idOras')))
        if cursor.fetchone() == None:
            return Response(status=400)

        query = 'INSERT INTO Temperaturi (valoare, id_oras) VALUES (%s, %s)'
        values = (str(payload['valoare']), str(payload['idOras']))
        cursor.execute(query, values)
        connection.commit()

        cursor.execute('SELECT * FROM Temperaturi WHERE id=(SELECT max(id) FROM Temperaturi)')
        results =  cursor.fetchone()

        cursor.close()
        close_connection(connection)
        return {"id" : str(results[0])}, 201
    except:
        return Response(status=400)

@app.route('/api/temperatures', methods=["GET"])
def getTemperatursByLonLat():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        
        num1 = 0
        num = 0
        lat = request.args.get('lat')
        if lat:
            num1 += 1
        lon = request.args.get('lon')
        if lon:
            num1 += 1
        fromm = request.args.get('from')
        if fromm and fromm != 'null':
            num += 1
        until = request.args.get('until')
        if until and until != 'null':
            num += 1
        query = "SELECT id, valoare, DATE_FORMAT(timestamp, '%Y-%m-%d') FROM Temperaturi where "
        query2 = "SELECT id FROM Orase where "
        if lat:
            query2 += 'latitudine=' + lat
            if num1 > 1:
                query2 +=' and '
                num1 -= 1

        if lon:
            query2 += 'longitudine=' + lon + ' '
            if num1 > 1:
                query2 +=' and '
                num1 -= 1

        if fromm and fromm != 'null':
            query += 'timestamp > "' + str(fromm) + '" '
            if num > 1:
                query +=' and '
                num -= 1
        
        if until and until != 'null':
            query += 'timestamp < "' + str(until) + '" '
            if num > 1:
                query +=' and '
                num -= 1
        if lat or lon:
            query += "id_oras in (" + query2 + ")"

        cursor.execute(query)
        item = cursor.fetchone()
        re = []
        while item:
            re.append({
                'id' : str(item[0]),
                'valoare': item[1],
                'timestamp': item[2]
                })
            item = cursor.fetchone()

        cursor.close()
        close_connection(connection)
        return  json.dumps(re), 200
    except:
        return Response(status=400)

@app.route('/api/temperatures/cities/<int:id>', methods=["GET"])
def getTemperatursByCities(id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        num = 0
        fromm = request.args.get('from')
        if fromm and fromm != 'null':
            num += 1
        until = request.args.get('until')
        if until and until != 'null':
            num += 1
        query = "SELECT id, valoare, DATE_FORMAT(timestamp, '%Y-%m-%d') FROM Temperaturi where "
        if fromm and fromm != 'null':
            query += 'timestamp > "' + str(fromm) + '" '
            if num > 1:
                query +=' and '
                num -= 1
        
        if until and until != 'null':
            query += 'timestamp < "' + str(until) + '" '
            if num > 1:
                query +=' and '
                num -= 1
        if num == 1:
            query += "and id_oras =" + str(id)
        else:
            query += " id_oras =" + str(id)
        
        cursor.execute(query)
        item = cursor.fetchone()
        re = []
        while item:
            re.append({
                'id' : str(item[0]),
                'valoare': item[1],
                'timestamp': item[2]
                })
            item = cursor.fetchone()

        cursor.close()
        close_connection(connection)
        return  json.dumps(re), 200
    except:
        return Response(status=400)

@app.route('/api/temperatures/countries/<int:id>', methods=["GET"])
def getTemperatursByCountries(id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        num = 0
        fromm = request.args.get('from')
        if fromm and fromm != 'null':
            num += 1
        until = request.args.get('until')
        if until and until != 'null':
            num += 1
        query = "SELECT id, valoare, DATE_FORMAT(timestamp, '%Y-%m-%d') FROM Temperaturi where "
        query2 = "SELECT id FROM Orase where id_tara=" + str(id)
        if fromm and fromm != 'null':
            query += 'timestamp > "' + str(fromm) + '" '
            if num > 1:
                query +=' and '
                num -= 1
        
        if until and until != 'null':
            query += 'timestamp < "' + str(until) + '" '
            if num > 1:
                query +=' and '
                num -= 1
        if num == 1:
            query += "and id_oras in (" + query2 + ")"
        else:
            query += " id_oras in (" + query2 + ")"
        
        cursor.execute(query)
        item = cursor.fetchone()
        re = []
        while item:
            re.append({
                'id' : str(item[0]),
                'valoare': item[1],
                'timestamp': item[2]
                })
            item = cursor.fetchone()

        cursor.close()
        close_connection(connection)
        return  json.dumps(re), 200
    except:
        return Response(status=400)

@app.route('/api/temperatures/<int:id>', methods=["PUT"])
def putTemperature(id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        payload = request.get_json(silent=True)

        query = 'UPDATE Temperaturi SET '
        num = len(payload)
        if payload.get('id'):
            query += 'id=' + str(payload.get('id'))
            if num > 1:
                query +=', '
                num -= 1
    
        if payload.get('idOras'):
            query += 'id_oras="' + str(payload.get('idOras')) + '"'
            if num > 1:
                query +=', '
                num -= 1

        if payload.get('valoare'):
            query += 'valoare=' + str(payload.get('valoare')) + ' '
            if num > 1:
                query +=', '
                num -= 1
        query += 'WHERE id=' + str(id)

        cursor.execute(query)
        connection.commit()

        cursor.close()
        close_connection(connection)
        return Response(status=200)
    except:
        return Response(status=400)

@app.route('/api/temperatures/<int:id>', methods=["DELETE"])
def deleteTemperature(id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        query = 'DELETE FROM Temperaturi WHERE id='+ str(id)
        cursor.execute(query)
        connection.commit()

        cursor.close()
        close_connection(connection)
        return Response(status=200)
    except:
        return Response(status=400)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)


