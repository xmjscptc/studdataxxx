#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  studfrontend.py
#  
#  Copyright 2021 xmjs_cptc <xmjs_cptc@xmjscptc-VirtualBox>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

TABLE_NAME = "studdatatbl"
from flask import *
import os
import sqlite3

con = sqlite3.connect("studdata.db")
print("Database opened successfully")
TABLE_NAME = "studdatatbl"

con.execute(" CREATE TABLE IF NOT EXISTS " + TABLE_NAME + " (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,\
 email TEXT UNIQUE NOT NULL, address TEXT NOT NULL)")
print("Table created successfully")
con.close() 

app = Flask(__name__)
@app.route("/")
def index():
	return render_template("./index.html")
@app.route("/add")
def add():
	return render_template("./add.html")
@app.route("/savedetails",methods = ["POST","GET"])
def saveDetails():
	msg = "msg"
	if request.method == "POST":
		try:
			name = request.form["name"]
			email = request.form["email"]
			address = request.form["address"]
			with sqlite3.connect("studdata.db") as con:
				cur = con.cursor()
				cur.execute("INSERT into  " + TABLE_NAME + "  (name, email, address) values (?,?,?)",(name,email,address))
				con.commit()
			msg = "Student successfully Added"
		except:
			msg = "We can not add the Student to the list"
		finally:
			return render_template("./success.html",msg = msg)
			con.close()
@app.route("/view")
def view():
	con = sqlite3.connect("studdata.db")
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	cur.execute("select * from  " + TABLE_NAME )
	rows = cur.fetchall()
	return render_template("./view.html",rows = rows)
@app.route("/delete")
def delete():
	return render_template("./Delete.html")
@app.route("/deleterecord",methods = ["POST"])
def deleterecord():
	id = request.form["id"]
	with sqlite3.connect("studdata.db") as con:
		try:
			cur = con.cursor()
			cur.execute("delete from  " + TABLE_NAME + " where id = ?",id)
			msg = "record successfully deleted"
		except:
			msg = "can't be deleted"
		finally:
			return render_template("./delete_record.html",msg = msg)
if __name__== "__main__":
	app.run(debug = True)