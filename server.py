from flask import Flask, jsonify, request, Response
from flaskext.mysql import MySQL
from flask_cors import CORS, cross_origin
#import requests

SteamKey = '292172823FD068B48FCEEE13D17EDF5C'  # Pi SteamKey
PortNumber = 5011  # Pi port number
#HostURL = 'http://cs2s.yorkdc.net'
#HostURL = 'cs2s.yorkdc.net'
HostURL = '192.168.0.32'
SteamID = '76561198058093131'

restServer = Flask(__name__)
CORS(restServer)
mysql = MySQL()

restServer.config['MYSQL_DATABASE_USER'] = 'oscar.reid'
restServer.config['MYSQL_DATABASE_PASSWORD'] = '6wfCwA7O'
restServer.config['MYSQL_DATABASE_DB'] = 'oscarreid_aWeb'
restServer.config['MYSQL_DATABASE_HOST'] = 'cs2s.yorkdc.net'
restServer.config['MYSQL_DATABASE_PORT'] = 3306
restServer.config['MYSQL_DATABASE_CHARSET'] = 'utf8'
mysql.init_app(restServer)
conn = mysql.connect()
cursor = conn.cursor()


@restServer.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@restServer.route("/")
def test():
    return "Hello"


@restServer.route("/sendCoD/<playerID>/<mapID>/<gameModeID>/<kills>/<deaths>/<assists>/<accuracy>", methods=['GET'])
def sendCoD(playerID, mapID, gameModeID, kills, deaths, assists, accuracy):
    cursor.execute("INSERT INTO CoD (playerID, mapID, gameModeID, kills, deaths, assists, accuracy) VALUES (%s, %s, %s, %s, %s, %s, %s)", (playerID, mapID, gameModeID, kills, deaths, assists, accuracy))
    conn.commit()
    return "Success"

#Delete Entry From CoD Table
@restServer.route("/delCoD/<EntryID>/<AuthCode>", methods=['POST'])
def delCoD(EntryID, AuthCode):
    if AuthCode == "123":
        intEntryID = int(EntryID)
        #cursor.execute("DELETE FROM D2 (EntryID) VALUES (%d)", (intEntryID))
        cursor.execute("DELETE FROM CoD WHERE EntryID=" + EntryID)
        conn.commit()
        return "Success"
    else:
        return "Incorrect AuthCode"


@restServer.route("/getCoD", methods=['GET'])
def getCoD():
    resultList = []
    records = []
    cursor.execute("SELECT * FROM CoD")
    result = cursor.fetchall()
    for i in result:
        statList = {'entryID': i[0], 'playerID': i[1], 'mapID': i[2], 'gameModeID': i[3], 'kills': i[4], 'deaths': i[5], 'assists': i[6], 'accuracy': i[7]}
        resultList.append(statList)
    records = {'results': resultList}
    return jsonify(records)


@restServer.route("/getCoD/<playerID>", methods=['GET'])
def getCoDWithID(playerID):
    resultList = []
    records = []
    cursor.execute("SELECT * FROM CoD WHERE playerID='" + playerID + "'")
    result = cursor.fetchall()
    for i in result:
        statList = {'entryID': i[0], 'playerID': i[1], 'mapID': i[2], 'gameModeID': i[3], 'kills': i[4], 'deaths': i[5], 'assists': i[6], 'accuracy': i[7]}
        resultList.append(statList)
    records = {'results': resultList}
    return jsonify(records)


#Send Destiny 2 data to MySQL DB
@restServer.route("/sendD2/<playerID>/<mapID>/<MotesDeposited>/<HostilesDefeated>/<GuardiansDefeated>/<MotesLost>/<PrimevalHealed>", methods=['GET'])
def sendD2(playerID, mapID, MotesDeposited, HostilesDefeated, GuardiansDefeated, MotesLost, PrimevalHealed):
    cursor.execute("INSERT INTO D2 (playerID, mapID, MotesDeposited, HostilesDefeated, GuardiansDefeated, MotesLost, PrimevalHealed) VALUES (%s, %s, %s, %s, %s, %s, %s)", (playerID, mapID, MotesDeposited, HostilesDefeated, GuardiansDefeated, MotesLost, PrimevalHealed))
    conn.commit()
    return "Success"

#Send Destiny 2 data to MySQL DB
@restServer.route("/delD2/<EntryID>/<AuthCode>", methods=['POST'])
def delD2(EntryID, AuthCode):
    if AuthCode == "123":
        intEntryID = int(EntryID)
        #cursor.execute("DELETE FROM D2 (EntryID) VALUES (%d)", (intEntryID))
        cursor.execute("DELETE FROM D2 WHERE EntryID=" + EntryID)
        conn.commit()
        return "Success"
    else:
        return "Incorrect AuthCode"


@restServer.route("/getD2", methods=['GET'])
def getD2():
    resultList = []
    records = []
    cursor.execute("SELECT * FROM D2")
    result = cursor.fetchall()
    for i in result:
        statList = {'EntryID': i[0], 'playerID': i[1], 'mapID': i[2], 'MotesDeposited': i[3], 'HostilesDefeated': i[4], 'GuardiansDefeated': i[5], 'MotesLost': i[6], 'PrimevalHealed': i[7]}
        resultList.append(statList)
    records = {'results': resultList}
    return jsonify(records)


@restServer.route("/getD2/<playerID>", methods=['GET'])
def getD2WithID(playerID):
    resultList = []
    records = []
    cursor.execute("SELECT * FROM D2 WHERE playerID='" + playerID + "'")
    result = cursor.fetchall()
    for i in result:
        statList = {'EntryID': i[0], 'playerID': i[1], 'mapID': i[2], 'MotesDeposited': i[3], 'HostilesDefeated': i[4], 'GuardiansDefeated': i[5], 'MotesLost': i[6], 'PrimevalHealed': i[7]}
        resultList.append(statList)
    records = {'results': resultList}
    return jsonify(records)



if __name__ == '__main__':
    print("== Running in debug mode ==")
    restServer.run(host='192.168.0.32', port=5011, debug=True)
    #restServer.run(host='cs2s.yorkdc.net', port=5011, debug=True)
