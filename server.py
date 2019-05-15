from flask import Flask, jsonify, request, Response
from flaskext.mysql import MySQL
from flask_cors import CORS, cross_origin
import requests

SteamKey = '21C5CFC0D481BE7C44CEBCAFCE909614'  # Pi SteamKey
PortNumber = 5011  # Pi port number
HostURL = 'cs2s.yorkdc.net' #URL of server
#SteamID = '76561198058093131' #My Steam ID


restServer = Flask(__name__)
CORS(restServer) #Allows CORS
mysql = MySQL()
#Database details
restServer.config['MYSQL_DATABASE_USER'] = 'oscar.reid'
restServer.config['MYSQL_DATABASE_PASSWORD'] = '6wfCwA7O'
restServer.config['MYSQL_DATABASE_DB'] = 'oscarreid_aWeb'
restServer.config['MYSQL_DATABASE_HOST'] = 'cs2s.yorkdc.net'
restServer.config['MYSQL_DATABASE_PORT'] = 3306
restServer.config['MYSQL_DATABASE_CHARSET'] = 'utf8'
mysql.init_app(restServer)
#Connecting to server
conn = mysql.connect()
cursor = conn.cursor()

#Headers to allow CORS
@restServer.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

#Default route used for testing
@restServer.route("/")
def test():
    return "Hello"


#Takes data from API call and inserts it into CoD table
@restServer.route("/sendCoD/<playerID>/<mapID>/<gameModeID>/<kills>/<deaths>/<assists>/<accuracy>", methods=['GET'])
def sendCoD(playerID, mapID, gameModeID, kills, deaths, assists, accuracy):
    #Checks playerId is valid
    #Then Checks all other values are valid
    if(int(playerID) > 0):
        if (mapID != "Containers" and mapID != "Village" and mapID != "Ocean Vila"):
            return "Invalid Map"
        elif (gameModeID != "Team Death Match" and gameModeID !="Free For All" and gameModeID !="Infected"):
            return "Invalid Gamemode"
        elif (int(kills) > 100 or int(kills) < 0):
            return "Kills value is impossible. Must be between 0 and 100"
        elif (int(deaths) > 100 or int(deaths) < 0):
            return "Deaths value is impossible. Must be between 0 and 100"
        elif (int(assists) > 100 or int(assists) < 0):
            return "Assists value is impossible. Must be between 0 and 100"
        elif (int(accuracy) > 100 or int(accuracy) < 0):
            return "Accuracy value is impossible. Must be between 0 and 100"
        else:
            cursor.execute("INSERT INTO CoD (playerID, mapID, gameModeID, kills, deaths, assists, accuracy) VALUES (%s, %s, %s, %s, %s, %s, %s)", (playerID, mapID, gameModeID, kills, deaths, assists, accuracy))
            conn.commit()
            return "Success"
    else:
        return "Invalid playerID"#If PlayerID was Invalid returns this

#Delete Entry From CoD Table providing authcode matches
@restServer.route("/delCoD/<EntryID>/<AuthCode>", methods=['POST'])
def delCoD(EntryID, AuthCode):
    #Checks EntryID is Valid
    #Then Checks Authorisation code
    #If either are incorrect it returns what the problem
    #If succesful Return Deleted entry EntryID
    if(int(EntryID) > 0):
        if AuthCode == "123":#Check the authcode matches
            intEntryID = int(EntryID)#Converts data to a int
            queryResult = cursor.execute("SELECT * FROM CoD WHERE entryID='" + EntryID + "'")
            if queryResult > 0:
                cursor.execute("DELETE FROM CoD WHERE EntryID=" + EntryID)#Executes the command to delete Entry from table
                conn.commit()
                return "Deleted Entry " + EntryID
            else:
                return "Entry doesn't exist"
        else:
            return "Incorrect AuthCode"
    else:
        return "Invalid EntryID"


#Returns all data in CoD table in JSON format
@restServer.route("/getCoD", methods=['GET'])
def getCoD():
    resultList = []
    records = []
    queryResult = cursor.execute("SELECT * FROM CoD")#Gets all rows from CoD
    #Checks that there are results in table CoD. If table is empty returns "no results found"
    if queryResult > 0:
        result = cursor.fetchall()
        for i in result:#for each result
        #Creates Key Value pairs
            statList = {'entryID': i[0], 'playerID': i[1], 'mapID': i[2], 'gameModeID': i[3], 'kills': i[4], 'deaths': i[5], 'assists': i[6], 'accuracy': i[7]}
            resultList.append(statList) #adds it to list
            records = {'results': resultList}
        return jsonify(records) #return list of records in JSON format
    else:
        return "No results found"


#Retuns specified player data from CoD table in JSON format
@restServer.route("/getCoD/<playerID>", methods=['GET'])
def getCoDWithID(playerID):
    if(int(playerID) > 0):
        resultList = []
        records = []
        queryResult = cursor.execute("SELECT * FROM CoD WHERE playerID='" + playerID + "'")
        if queryResult > 0:
            result = cursor.fetchall()
            for i in result:
                #Creates Key Value pairs
                statList = {'entryID': i[0], 'playerID': i[1], 'mapID': i[2], 'gameModeID': i[3], 'kills': i[4], 'deaths': i[5], 'assists': i[6], 'accuracy': i[7]}
                resultList.append(statList)
                records = {'results': resultList}
            return jsonify(records)
        else:
            return "No results found"
    else:
        return "Invalid PlayerID"


#Retuns specified player where map is specified data from CoD table in JSON format
@restServer.route("/getCoD/<playerID>/<gameMode>", methods=['GET'])
def getCoDWithIDMap(playerID, gameMode):
    if(int(playerID) > 0):
        if (gameMode != "Team Death Match" and gameMode !="Free For All" and gameMode !="Infected"):
            return "Invalid Gamemode"
        else:
            resultList = []
            records = []
            queryResult = cursor.execute("SELECT * FROM CoD WHERE playerID='" + playerID + "' AND gameModeID='" + gameMode +"'")
            #cursor.execute("SELECT * FROM CoD WHERE mapID='Village' AND playerID='13'")
            if queryResult > 0:
                result = cursor.fetchall()
                for i in result:
                    #Creates Key Value pairs
                    statList = {'entryID': i[0], 'playerID': i[1], 'mapID': i[2], 'gameModeID': i[3], 'kills': i[4], 'deaths': i[5], 'assists': i[6], 'accuracy': i[7]}
                    resultList.append(statList)
                    records = {'results': resultList}
                return jsonify(records)
            else:
                return "No results found"
    else:
        return "Invalid PlayerID"





#Takes data from API call and inserts in into Destiny 2 table to MySQL DB
@restServer.route("/sendD2/<playerID>/<mapID>/<MotesDeposited>/<HostilesDefeated>/<GuardiansDefeated>/<MotesLost>/<PrimevalHealed>", methods=['GET'])
def sendD2(playerID, mapID, MotesDeposited, HostilesDefeated, GuardiansDefeated, MotesLost, PrimevalHealed):
    #Checks playerId is valid
    #Then Checks all other values are valid
    if(int(playerID) > 0):
        if (mapID != "Kell's Grave" and mapID != "Legion's Folly" and mapID != "Catherdral of Scars" and mapID != "Emerald Coast"):
            return "Invalid Map"
        elif (int(MotesDeposited) > 225 or int(MotesDeposited) < 0):
            return "Motes Bank value is impossible. Must be between 0 and 225"
        elif (int(HostilesDefeated) > 500 or int(HostilesDefeated) < 0):
            return "Hostile Kills value is impossible. Must be between 0 and 500"
        elif (int(GuardiansDefeated) > 100 or int(GuardiansDefeated) < 0):
            return "Player Kills value is impossible. Must be between 0 and 100"
        elif (int(MotesLost) > 500 or int(MotesLost) < 0):
            return "Motes Lost value is impossible. Must be between 0 and 500"
        elif (int(PrimevalHealed) > 100 or int(PrimevalHealed) < 0):
            return "Healed value is impossible. Must be between 0 and 100"
        else:
            cursor.execute("INSERT INTO D2 (playerID, mapID, MotesDeposited, HostilesDefeated, GuardiansDefeated, MotesLost, PrimevalHealed) VALUES (%s, %s, %s, %s, %s, %s, %s)", (playerID, mapID, MotesDeposited, HostilesDefeated, GuardiansDefeated, MotesLost, PrimevalHealed))
            conn.commit()
            return "Success"
    else:
        return "Invalid PlayerID"

#Deletes a entry from D2 table providing authcode matches
@restServer.route("/delD2/<EntryID>/<AuthCode>", methods=['POST'])
def delD2(EntryID, AuthCode):
    #Checks EntryID is Valid
    #Then Checks Authorisation code
    #If either are incorrect it returns what the problem
    #If succesful Return Deleted entry EntryID
    if(int(EntryID) > 0):
        if AuthCode == "123":#Check the authcode matches
            intEntryID = int(EntryID)#Converts data to a int
            queryResult = cursor.execute("SELECT * FROM D2 WHERE entryID='" + EntryID + "'")
            if queryResult > 0:
                cursor.execute("DELETE FROM D2 WHERE EntryID=" + EntryID)#Executes the command to delete Entry from table
                conn.commit()
                return "Deleted Entry " + EntryID
            else:
                return "Entry doesn't exist"
        else:
            return "Incorrect AuthCode"
    else:
        return "Invalid EntryID"

#Returns all data in D2 table in JSON format
@restServer.route("/getD2", methods=['GET'])
def getD2():
    resultList = []
    records = []
    queryResult = cursor.execute("SELECT * FROM D2")
    #Checks there are results in table D2. If table is empty returns "no results found"
    if queryResult > 0:
        result = cursor.fetchall()
        for i in result:
            #Creates Key Value pairs
            statList = {'EntryID': i[0], 'playerID': i[1], 'mapID': i[2], 'MotesDeposited': i[3], 'HostilesDefeated': i[4], 'GuardiansDefeated': i[5], 'MotesLost': i[6], 'PrimevalHealed': i[7]}
            resultList.append(statList)
            records = {'results': resultList}
        return jsonify(records)
    else:
        return "No results found"

#Retuns specified player data from D2 table in JSON format
@restServer.route("/getD2/<playerID>", methods=['GET'])
def getD2WithID(playerID):
    if (int(playerID) > 0):
        resultList = []
        records = []
        queryResult = cursor.execute("SELECT * FROM D2 WHERE playerID='" + playerID + "'")
        if queryResult > 0:
            result = cursor.fetchall()
            for i in result:
                #Creates Key Value pairs
                statList = {'EntryID': i[0], 'playerID': i[1], 'mapID': i[2], 'MotesDeposited': i[3], 'HostilesDefeated': i[4], 'GuardiansDefeated': i[5], 'MotesLost': i[6], 'PrimevalHealed': i[7]}
                resultList.append(statList)
                records = {'results': resultList}
            return jsonify(records)
        else:
            return "No results found"
    else:
        return "Invalid Player ID"


#Uses Steam ID from API call to call Steam API to retrieve list of games associated with that account
@restServer.route("/getSteamGames/<steamID>", methods=['GET'])
def getSteamGames(steamID):
    if (int(steamID) <= 99999999999999999 and int(steamID) >= 10000000000000000):#Valid Steam IDs are between these numbers
        api_url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' + SteamKey + '&steamid=' + steamID +'&format=json'
        response = requests.get(api_url)
        if response.status_code == 200:
            #Returns list of games in JSON format
            return (response.content)
        else:
            return "Invalid Steam ID"
    else:
        return "Steam ID is incorrect length"

#Uses Steam game ID to call Steam API to retrieve a description of that game ID
@restServer.route("/getSteamGameDes/<gameID>", methods=['GET'])
def getSteamGameDes(gameID):
    if (int(gameID) > 0):#Valid Steam game IDs are all positive
        api_url = 'http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key=' + SteamKey + '&appid=' + gameID
        response = requests.get(api_url)
        if response.status_code == 200:
            return (response.content)
        else:
            return "Invalid Steam Game ID"
    else:
        return "Fail"

#Uses Steam Player ID to call Steam API to retrieve a list of Steam ID that are friends with the provided Steam ID
@restServer.route("/getSteamFriends/<steamID>", methods=['GET'])
def getSteamFriends(steamID):
    if (int(steamID) <= 99999999999999999 and int(steamID) >= 10000000000000000):#Valid Steam IDs are between these numbers
        api_url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=' + SteamKey + '&steamid=' + steamID + '&relationship=friend'
        response = requests.get(api_url)
        if response.status_code == 200:
            return (response.content)
        else:
            return "Invalid Steam ID"
    else:
        return "Steam ID is incorrect length"

#Uses Steam ID to call Steam API to retrieve a JSON object of that IDs Steam profile
@restServer.route("/getSteamProfile/<steamID>", methods=['GET'])
def getSteamProfile(steamID):
    if (int(steamID) <= 99999999999999999 and int(steamID) >= 10000000000000000):#Valid Steam IDs are between these numbers
        api_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + SteamKey + '&steamids=' + steamID
        response = requests.get(api_url)
        if response.status_code == 200:
            return (response.content)
        else:
            return "Invalid Steam ID"
    else:
        return "Steam ID is incorrect length"



if __name__ == '__main__':
    print("== Running in debug mode ==")
    restServer.run(host=HostURL, port=PortNumber, debug=True, threaded=True)
