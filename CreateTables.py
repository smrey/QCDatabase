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
tablist = ["Pipeline","Rds","Chemistry","MiSeqRun"]

for table in tablist[::-1]: #Have to drop tables in the reverse order from where they were created
    #time.sleep(0.5)
    sqlsyntax = "DROP TABLE IF EXISTS "+table
    #print sqlsyntax
    cursor.execute(sqlsyntax)

#Create tables
#Where a relationship exists, tables must be created in the order parent and then child
cursor.execute(""" CREATE TABLE Rds (
        ReadID BIGINT UNSIGNED AUTO_INCREMENT NOT NULL,
        ReadNumber VARCHAR(15) NOT NULL,
        Indexed TINYINT(1),
        NumberOfCycles SMALLINT UNSIGNED NOT NULL,
        Primary key(ReadID)
        )""")
print "Reads table created"

cursor.execute(""" CREATE TABLE Pipeline (
        PipelineID SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
        PipelineName VARCHAR(30),
        PipelineVersion TINYINT(2),
        Primary key(PipelineID)
        )""")
print "Pipeline table created"

cursor.execute(""" CREATE TABLE Chemistry (
        ChemistryID SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
        ChemistryType VARCHAR(15),
        Primary key(ChemistryID)
        )""")
print "Chemistry table created"

cursor.execute(""" CREATE TABLE MiSeqRun (
        MiSeqRunID VARCHAR(50) NOT NULL,
        RunStartDate DATE NOT NULL,
        FieldProgrammableGateArrayVersion VARCHAR(10) NOT NULL,
        MiSeqControlSoftwareVersion VARCHAR(10) NOT NULL,
        RealTimeAnalysisSoftwareVersion VARCHAR(10) NOT NULL,
        KitVersionNumber TINYINT(2) NOT NULL,
        ExperimentName VARCHAR(15),
        Operator VARCHAR(5),
        PipelineID SMALLINT(5) UNSIGNED NOT NULL,
        Primary key(MiSeqRunID)
        )""")
print "MiSeqRun table created"
