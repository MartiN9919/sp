# -*- coding: utf-8 -*-

###########################################
# СПИСОК ДОСТУПНЫХ СКРИПТОВ
###########################################
from lib.db.connect import connect_mysql

def script_list(id):
	sqlRequest = "Select id, name, variables from sys_script where parent_id = " + str(id) + ";"
	listScripts = connect_mysql.db_sql(sqlRequest)

	dictList = []

	for row in listScripts:
		dictList.append({"id":row[0],"text":row[1],"variables":row[2]})

	return dictList
