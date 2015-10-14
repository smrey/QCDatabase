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
tablist = ["InstrumentType","Instrument","Pipeline","Rds","Chemistry","FlowCell","PR2Bottle",
           "ReagentKit","MiSeqRun","LinkMiSeqRunRds"]

for table in tablist[::-1]: #Have to drop tables in the reverse order from where they were created
    #time.sleep(0.5)
    sqlsyntax = "DROP TABLE IF EXISTS "+table
    #print sqlsyntax
    cursor.execute(sqlsyntax)

#Create tables
#Where a relationship exists, tables must be created in the order parent and then child
cursor.execute(""" CREATE TABLE InstrumentType (
        InstrumentTypeID TINYINT UNSIGNED AUTO_INCREMENT NOT NULL,
        InstrumentType VARCHAR(10) NOT NULL,
        Primary key(InstrumentTypeID)
        )""")
print "InstrumentType table created"

cursor.execute(""" CREATE TABLE Instrument (
        InstrumentID TINYINT UNSIGNED AUTO_INCREMENT NOT NULL,
        IlluminaInstrumentIdentifier VARCHAR(15) NOT NULL,
        InstrumentType TINYINT UNSIGNED NOT NULL,
        Primary key(InstrumentID),
        Foreign key(InstrumentType) References InstrumentType(InstrumentTypeID)
        )""")
print "Instrument table created"

cursor.execute(""" CREATE TABLE Pipeline (
        PipelineID SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
        PipelineName VARCHAR(30),
        PipelineVersion TINYINT(2),
        Primary key(PipelineID)
        )""")
print "Pipeline table created"

cursor.execute(""" CREATE TABLE Rds (
        ReadID BIGINT UNSIGNED AUTO_INCREMENT NOT NULL,
        ReadNumber VARCHAR(15) NOT NULL,
        Indexed TINYINT(1),
        NumberOfCycles SMALLINT UNSIGNED NOT NULL,
        Primary key(ReadID)
        )""")
print "Reads table created"

cursor.execute(""" CREATE TABLE Chemistry (
        ChemistryID SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
        ChemistryType VARCHAR(15),
        Primary key(ChemistryID)
        )""")
print "Chemistry table created"

cursor.execute(""" CREATE TABLE FlowCell (
        FlowCellID INT(15) UNSIGNED,
        FlowCellPartID VARCHAR(25),
        FlowCellExpiry DATE,
        Primary key(FlowCellID)
        )""")
print "FlowCell table created"

cursor.execute(""" CREATE TABLE PR2Bottle (
        PR2BottleID INT(15) UNSIGNED,
        PR2BottlePartID VARCHAR(25),
        PR2BottleExpiry DATE,
        Primary key(PR2BottleID)
        )""")
print "PR2Bottle table created"

cursor.execute(""" CREATE TABLE ReagentKit (
        ReagentKitID INT(15) UNSIGNED,
        ReagentKitPartID VARCHAR(25),
        ReagentKitExpiry DATE,
        Primary key(ReagentKitID)
        )""")
print "ReagentKit table created"

cursor.execute(""" CREATE TABLE MiSeqRun (
        MiSeqRunID VARCHAR(50) NOT NULL,
        RunStartDate DATE NOT NULL,
        FieldProgrammableGateArrayVersion VARCHAR(10) NOT NULL,
        MiSeqControlSoftwareVersion VARCHAR(10) NOT NULL,
        RealTimeAnalysisSoftwareVersion VARCHAR(10) NOT NULL,
        KitVersionNumber TINYINT(2) NOT NULL,
        ExperimentName VARCHAR(15),
        Operator VARCHAR(5),
        ChemistryID SMALLINT UNSIGNED NOT NULL,
        PipelineID SMALLINT(5) UNSIGNED NOT NULL,
        FlowCellID INT(15) UNSIGNED,
        PR2BottleID INT(15) UNSIGNED,
        ReagentKitID INT(15) UNSIGNED,
        Primary key(MiSeqRunID),
        Foreign key(ChemistryID) References Chemistry(ChemistryID),
        Foreign key(PipelineID) References Pipeline(PipelineID),
        Foreign key(FlowCellID) References FlowCell(FlowCellID),
        Foreign key(PR2BottleID) References PR2Bottle(PR2BottleID),
        Foreign key(ReagentKitID) References ReagentKit(ReagentKitID)
        )""")
print "MiSeqRun table created"

cursor.execute(""" CREATE TABLE LinkMiSeqRunRds (
        LinkMiSeqRunRdsID SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
        MiSeqRunID VARCHAR(50) NOT NULL,
        ReadID BIGINT UNSIGNED NOT NULL,
        Primary key(LinkMiSeqRunRdsID),
        Foreign key(MiSeqRunID) References MiSeqRun(MiSeqRunID),
        Foreign key(ReadID) References Rds(ReadID)
        )""")
print "LinkMiSeqRunRds table created"
