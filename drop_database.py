from database_control import *

load_mysql("localhost","root","user")

log_on_level("Enter database name to drop:",0)
db_name = str(raw_input())

drop_database(db_name)
