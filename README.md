Oscar Reid's Advanced Web 3CB109 Project
Student ID: 169063841
Assigned port number: 5011

On CS2S Server the files are located at: /home/oscar.reid/htdocs
Server File is called: server.py
Client File is called: index.html


URL of Web Client is: cs2s.yorkdc.net/~oscar.reid/
URL for Web Server is: cs2s.yorkdc.net:5011


The Port Number and Server URL can be easily changed by modifying the values titled PortNumber and HostURL at the top of server.py

External Sources:
jQuery was used for querying the server - https://jquery.com/
Bootstrap 4 was used for styling - https://getbootstrap.com/docs/4.0/getting-started/introduction/
Steam APIs were used for the Find Game page - https://developer.valvesoftware.com/wiki/Steam_Web_API#GetNewsForApp_.28v0001.29

Install instructions:
The server requires several prerequisite libraries to run:
sudo apt-get install pip
pip install flask
pip install flask-mysql
pip install -U flask-cors
pip install requests

To run the server type "python server.py" while in the directory where the files are stored in the console


Database Username: oscar.reid
Database Password: 6wfCwA7O
Database name: oscarreid_aWeb

Database Tables:
CoD table name: CoD
8 Columns:
EntryID, Player ID, Map Name, Game mode, Kills, Deaths, Assists, Accuracy
int AUTO_INCREMENT, varchar, varchar, varchar, varchar, varchar, varchar, varchar



Destiny 2 table name: D2
8 Columns:
EntryID, Player ID, Map Name, Game mode, Kills, Deaths, Assists, Accuracy
int AUTO_INCREMENT, varchar, varchar, varchar, varchar, varchar, varchar, varchar


Server Guide:
When the client asks for games stats the server queries the database
It then uses the returned data and formats it into key value pairs
This data is passed into jsonify and returned to the client

API Calls and what they do:

CoD page API calls
Send stats to Database
/sendCoD/playerID/mapID/gameModeID/kills/deaths/assists/Accuracy  ---GET

Delete stats from database AuthCode is 123 will fail if code is not used
/delCoD/EntryID/AuthCode  ---POST

Get all CoD stats from database
/getCoD    ---GET

Get CoD stats for particular player
/getCoD/playerID   ---GET

Get CoD stats for particular player and gamemode
/getCoD/playerID/gameMode   ---GET


Destiny 2 API calls
Send stats to Database
/sendD2/playerID/mapID/MotesDeposited/HostilesDefeated/GuardiansDefeated/MotesLost/sendPrimevalHealed

Delete stats from database AuthCode is 123 will fail if code is not used
/delD2/EntryID/AuthCode

Get all Destiny 2 stats from database
/getD2

Get Destiny 2 stats for particular player
/getD2/playerID


Steam API calls
These calls go to the python server which then uses requests to call a Steam API

Get full profile details of a Steam ID
/getSteamFriends/steamID
This calls the Steam API
'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + SteamKey + '&steamids=' + steamID
returns JSON object of Steam profile details

Get all Steam friends of a Steam ID
/getSteamFriends/steamID
This calls the Steam API
'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=' + SteamKey + '&steamid=' + steamID + '&relationship=friend'
returns JSON object of Steam IDs

Get all Steam Games belonging to a Steam ID
/getSteamGames/steamID
This calls the Steam API
'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' + SteamKey + '&steamid=' + steamID +'&format=json'
returns a JSON object of Steam game IDs

Get Steam game description using a game ID
/getSteamGameDes/gameID
This calls the Steam API
'http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key=' + SteamKey + '&appid=' + gameID
returns a JSON object of a Steam game description

Client Guide and advanced features:
Below are the instructions for how each feature on the client works and the method it uses and if it is a mashup or not

Input and result validation:
The Client checks that all input fields are filled before submitting a request to the server
The server checks the inputs are correct such as the map is from the list of options
The server also checks that the values submitted are possible within the game such as the max possible CoD Kills is 100 any value over will return Kills value is impossible
Before the server returns results from the database it checks that there are results in it
If not it will return "No results found" which the client displays

CoD and Destiny 2 Pages
Submit Stats - GET:
Input values into the fields and click submit
Values must be legitimate values these are
CoD:
Kils between 0 - 100, Deaths 0 - 100, Assists 0 - 100, Accuracy 0 - 100
D2:
Motes Bank 0 - 225, Hostile Kills 0 - 500, Player Kills 0 - 100, Motes Lost 0 - 500, Healed 0 - 100
This calls a function that fetches the values from the fields
It then calls the sendCoD or sendD2 API using jQuery GET with the values in the API call
For CoD the calls is /sendCoD/<playerID>/<mapID>/<gameModeID>/<kills>/<deaths>/<assists>/<accuracy>
For Destiny 2 the call is /sendD2/<playerID>/<mapID>/<MotesDeposited>/<HostilesDefeated>/<GuardiansDefeated>/<MotesLost>/<PrimevalHealed>
The server then inserts the values into the database using SQL

Delete Stats - POST:
Enter a EntryID and the Authorisation code (123) and click submit
Entry IDs can be found by search for stats without a specified player ID
This calls a function that fetches the values from the fields
It then calls /delCoD/<EntryID>/<AuthCode> or /delD2/<EntryID>/<AuthCode> API using jQuery POST with the values in the API call
The server then checks the authorisation code is correct and if it is searches for that entry ID and deletes the entry from the database table

Search for Stats - GET:
This input field can be left blank or you can enter a player ID (12 or 13 have prefilled entries or make your own by submitting stats)
If left blank it will call the server using /getCoD or /getD2 if given a ID it will use /getCoD/<ID> or /getD2/<ID>
If left blank the server will return a JSON object of all the entries
If given a ID it will return a JSON object of just the entries relating to the ID provided
The client will then display the results in the table below the input fields

Compare Stats - GET, Mashup:
Enter two IDs and for CoD you can specify a gamemode
The client will then make two API requests to the server /getCoD/<playerID> or /getD2/<playerID> to retrieve the stats for both IDs
These calls are made consecutively
The client then calculates the average stats for both players
Then adds them to the table below the input field

Find Game Page
Find Friends - GET, Mashup:
Enter a Steam ID and click submit
This calls the server /getSteamFriends/<steamID> which then calls the Steam API which returns a JSON object consisting of Steam IDs of friends
The client then calls the server /getSteamProfile/<steamID> again for each ID which calls the Steam API to retrieve the name belonging to each ID
The client then displays the Steam ID and the name belonging to it in a table below the input field

Find game owned by both IDs - GET, Mashup:
This feature finds games that are owned by both provided Steam IDs
Enter two Steam IDs and click submit for testing use 76561198058093131 and 76561197983520575 or find Steam IDs using the find friends feature
This calls the server /getSteamGames/<steamID> which calls Steams API which returns a JSON object of all games associated with that Steam ID this is done for both IDs
The lists are then compared to find matching Game IDs
The server /getSteamGameDes/<gameID> is called with each game ID which calls a Steam API to return a description of that game in JSON format
The client then finds the name of the game from the JSON object
Providing the name isn't null which is the case with deleted games or SteamTestApp which is a test game it is added to the matching games table
Then table displays the names of all the games owned by both IDs
