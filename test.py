import database_control as dbc
from database_control import User


dbc.load_mysql("localhost","root","user")

database_name = "tilcinet"
table_name = "users"

dbc.load_database(database_name)

dbc.insert_into_table(table_name,User(["Mark M."]))

##res = dbc.get_table_attributes(table_name)

##t = {}

##for r in range(len(res)):
##  for k in res[r]:
##    if k is "auto_increment":
##      r = r + 1
##  t = res[r]
  
##print t
dbc.DB.close()
