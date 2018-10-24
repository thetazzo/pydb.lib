"""Databese working

TODO:
    <+> command LIBRARY
    <->
"""

class User(object):
    """[summary]
    Arguments:
        object {[type]} -- [description]
    """

    def __init__(self, data):
        self.data = data

CREATE_DATABASE = "CREATE DATABASE IF NOT EXISTS "
DROP_DATABASE = "DROP DATABASE "

def show_database_like(db_name):
    """Rerurns the command
    Arguments:
        db_name {string} -- [description]
    Returns:
        string -- [description]
    """
    return "SHOW DATABASES LIKE '" + db_name+ "'"

def show_table_like(table_name):
    """Rerurns the command
    Arguments:
        db_name {string} -- [description]
    Returns:
        string -- [description]
    """
    return "SHOW TABLES LIKE '" + table_name+ "'"

CREATE_TABLE = "CREATE TABLE "
USE = "USE "
INSERT_INTO = "INSERT INTO "


import MySQLdb

###########################SETUP DATABASE#######################################
DB = None
CUR = None

def load_database(hst,usr,pswd,lg_lvl=1):
 	global DB
 	global CUR
	global log_level
 	DB = MySQLdb.connect(host=hst,user=usr,passwd = pswd)
 	CUR = DB.cursor()
	log_level = lg_lvl
 	log_on_level("Database " + hst + " loaded!",2)


ATTRIB = {}
USERS = []

log_level = 1

#### LOG LEVELS #####
Database_Commands = 0
User_Output = 1
Nothing= 2
Debug = 3

###############################################################################

def set_log_level(lgl):
	global log_level
	log_level = lgl

def check():
	if(DB ==  None):
		log("ERROR: No database loaded!!")
		return False
	return True

def log(msg):
		print msg

def log_on_level(msg,lvl):
	if(log_level == lvl or lvl == 2 or log_level == 3):
		log(msg)

def var_char(_x=0):
    """Creats a string version of VARCHAR function
    Arguments:
        x {integer} -- [description]
    Returns:
        string -- [description]
    """
    return "VARCHAR(" + str(_x) + ")"

def db_exists(db_name=""):
    """Checks if database exists
    Keyword Arguments:
        db_name {str} -- name of the database (default: {""})
    Returns:
        boolean -- result if database exists or not
    """
    result = CUR.execute(show_database_like(db_name))
    if result:
        return True

    return False

def table_exists(db_name,table_name):
	if db_exists(db_name):
		CUR.execute(USE + db_name)
		result = CUR.execute(show_table_like(table_name))
		if result:
			return True
	return False

def create_database(db_name):
    """Creates a database
    Arguments:
        db_name {string} -- name of the database
    """
    if db_exists(db_name):
        log("DATABASE: " + db_name + " already exists!")
    else:
        CUR.execute(CREATE_DATABASE + db_name)
        log_on_level("Database created: " + db_name,0)

def drop_database(db_name):
    """Destorys the database
    Arguments:
        db_name {string} -- database name
    """
    if db_exists(db_name):
        CUR.execute(DROP_DATABASE + db_name)
        log_on_level("Database dropped: " + db_name,0)
    else:
        log_on_level("DATABASE: "  + db_name + " does not exist!",2)

def generate_attributes(attributes):
    """Generates the string with attributes for parameters for creating a table
    Keyword Arguments:
        attributes {dict} -- stores raw attribute data (default: {{}})
    Returns:
        string -- generated a string to insert into create table
    """
    tmp = 0
    res = ""
    for _x in range(len(attributes)):
        if _x != tmp:
            res += ","
        tmp = _x
        for _y in range(len(attributes[_x])):
            res += attributes[_x][_y]
            if (_y + 1) < len(attributes[_x]):
                res += " "
    return res

def create_table(db_name, table_name, attributes):
    """Creates a table inside the specified database
    Arguments:
        db_name {string} -- name of the database
        table_name {string} -- name of the table
        attributes {dict} -- a dictionary that contaisn attributes of the table
    """
    if db_exists(db_name):
        CUR.execute(USE + db_name)
        log_on_level("USING: " + db_name,0)
        CUR.execute(CREATE_TABLE + table_name + "(" + generate_attributes(attributes) + ")")
        log_on_level(CREATE_TABLE + table_name + "(" + generate_attributes(attributes) + ")",0)
    else:
        log_on_level("DATABASE: "  + db_name + " does not exist!",2)

def insert_into_table(db_name, table_name, users_array, attributes):
    if db_exists(db_name):
        CUR.execute(USE + db_name)
        log_on_level("USING: " + db_name,0)
        if table_exists(db_name,table_name):
            res = INSERT_INTO + table_name + "("
            _x = 0
            for _x in attributes.keys():
                for _y in attributes[_x]:
                    if _y == "AUTO_INCREMENT":
                        attributes.pop(_x)
            for _x in attributes.keys():
                res += str(attributes[_x][0])
                if (_x + 1) in attributes.keys():
                    res += ","
            res += ") values("

            for a in attributes:
                for u in users_array:
                    for aa in attributes[a]:
                        if aa == "PRIMARY KEY":
                            if(check_if_value_exists(db_name,table_name,attributes[a][0],u.data[a])):
                                users_array.remove(u)


            for usr in users_array:
                temp = ""
                i = 0
                for user_data in usr.data:
                    temp += str("'" + user_data + "'")
                    i += 1
                    if i < len(usr.data) - 1:
                        temp += ','

                log_on_level(res  + temp + ")",0)
                CUR.execute(res  + temp + ")")
                DB.commit()
        else:
            log_on_level("TABLE: " + table_name + " does not exit!",2)
    else:
        log_on_level("DATABASE: "  + db_name + " does not exist!",2)

def create(db_name,table_name):
	if(db_exists(db_name) == False):
		create_database(db_name)

	if(table_exists(db_name,table_name) == False):
		create_table(db_name,table_name,ATTRIB)

	insert_into_table(db_name,table_name,USERS,ATTRIB)


def get_data(db_name,tb_name,key,index):
	if db_exists(db_name):
		CUR.execute(USE + db_name)
		if table_exists(db_name,tb_name):
			if(index == -1):
				CUR.execute("SELECT * FROM " + tb_name)
			else:
				CUR.execute("SELECT * FROM " + tb_name + " where " + key + " = " + str(index))

			s = CUR.fetchall()
			return s

def log_data(db_name,tb_name,key,index,dindex):
    if table_exists(db_name,tb_name):
        d = get_data(db_name,tb_name,key,index)
        res = ""
        if  dindex == -1:
            for v in d:
                c = 0;
                for k in v:
                    res += str(k) + " "
                    c = c + 1
                    if c == 2:
                        res += "\n"
                    else:
                        res = ""
            log_on_level("Values for attribute "  + "'" +key + "':",1)
            for v in d:
                res = v[dindex]
                log_on_level(res,1)


def check_if_value_exists(db_name,tb_name,attrib_name,value):
    if db_exists(db_name):
        CUR.execute(USE + db_name)
        if table_exists(db_name,tb_name):
            log_on_level("SELECT * from " + tb_name + " where " + attrib_name + " = " + "'" + value + "'",0)
            CUR.execute("SELECT * from " + tb_name + " where " + attrib_name + " = " + "'" + value + "'")
            s = CUR.fetchall()
            if(len(s) > 0):
                log_on_level(value + " exists in " + tb_name,2)
                return True
    return False
def add_attribute(a):
    global ATTRIB
    ATTRIB[len(ATTRIB)] = a

def add_user(user):
	USERS.append(user)
