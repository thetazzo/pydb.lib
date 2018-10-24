import database_control as dbc
from database_control import User

print "Set log level:"
lvl = input()


dbc.load_mysql("localhost","root","user",int(lvl))

if(dbc.check() == False):
	exit()

database_name = "tilcinet"
dbc.load_database(database_name)

table_name = "users"

dbc.add_attribute(["id","INT","NOT NULL PRIMARY KEY","AUTO_INCREMENT"])
dbc.add_attribute(["ime",dbc.var_char(20),"NOT NULL"])

if(dbc.check_if_value_exists(table_name,"ime","Tilen O.") != True):
    dbc.add_user(dbc.User(["Tilen O."]))

if(dbc.check_if_value_exists(table_name,"ime","Ulrih A.") != True):
    dbc.add_user(dbc.User(["Ulrih A."]))

if(dbc.check_if_value_exists(table_name,"ime","Martin K.") != True):
    dbc.add_user(dbc.User(["Martin K."]))

if(dbc.check_if_value_exists(table_name,"ime","Tilen P.") != True):
    dbc.add_user(dbc.User(["Tilen P."]))

dbc.create(table_name)


dbc.log_data(table_name,"id",-1,-1)


dbc.DB.close()
