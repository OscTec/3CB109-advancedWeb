Oscar Reid's Advanced Web 3CB109 Project
Student ID: 169063841

On CS2S Server the files are located at: /home/oscar.reid/htdocs
Server File is called: server.py
Client File is called: index.html
jQuery File is called: jquery-3.3.1.min.js


URL of Web Client is: http://cs2s.yorkdc.net/~oscar.reid/
URL for Web Server is: http://cs2s.yorkdc.net:5011
Assigned port number: 5011

Install instructions
The server requires several prerequisite libraries to run:
sudo apt-get install pip
pip install flask
pip install flask-mysql
pip install -U flask-cors
Pip install requests

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


Destiny 2 API calls
Send stats to Database
/sendD2/playerID/mapID/MotesDeposited/HostilesDefeated/GuardiansDefeated/MotesLost/sendPrimevalHealed

Delete stats from database AuthCode is 123 will fail if code is not used
/delD2/EntryID/AuthCode

Get all Destiny 2 stats from database
/getD2

Get Destiny 2 stats for particular player
/getD2/playerID


Complete Guide to the Client:
Do this it gives this ect.



Advanced features:


Giving Credit:
JavaScript wait() acquired from http://www.endmemo.com/js/pause.php

Moodle hand in requires:
server.py
index.html
jquery-3.3.1.min.js
README.md



To Do List:
Compare Stats for two players
Add a PUT API
Find 2 player games from Steam for 2 players
Validate inputs
More stuff
Perfect things

Write up:
Complete Guide written
Reference all code from external sources in code and write up
