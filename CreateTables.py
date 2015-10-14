'''
Created on 12 Oct 2015

@author: Sara
'''
import MySQLdb
import sys

# Open database connection
try:
    db = MySQLdb.connect("localhost",sys.argv[1],sys.argv[2], "ngsqc" ) #Pass username and password as command line arguments

except:
    sys.exit("Enter correct username and password!")
    
print "Success so far"

# prepare a cursor object using cursor() method
cursor = db.cursor()

#Drop tables prior to creation in here, to avoid conflicts
table = "Run"
sqlsyntax = "DROP TABLE IF EXISTS "+table
#print sqlsyntax
cursor.execute(sqlsyntax)

#Create tables
#Where a relationship exists, tables must be created in the order parent and then child
cursor.execute(""" CREATE TABLE Run (
        RunID 
        PatientID BIGINT UNSIGNED AUTO_INCREMENT NOT NULL,
        NHSNumber VARCHAR(10),
        FirstName VARCHAR(25),
        LastName VARCHAR(25) NOT NULL,
        PreviousLastName VARCHAR(25),
        DateOfBirth DATE,
        GENDER VARCHAR(1) NOT NULL,
        Primary key(RunID)
        )""")
print "Run table created"

