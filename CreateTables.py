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
           "ReagentKit","MiSeqRun","LinkMiSeqRunRds","QualityMetrics","ExtractionMetrics",
           "CorrectedIntMetrics","ErrorMetrics","TileMetrics","IndexMetricsMSR"]

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

cursor.execute(""" CREATE TABLE QualityMetrics (
        LaneID TINYINT UNSIGNED NOT NULL,
        TileID SMALLINT UNSIGNED NOT NULL,
        CycleID SMALLINT UNSIGNED NOT NULL,
        MiSeqRunID VARCHAR(50) NOT NULL,
        Q01 MEDIUMINT UNSIGNED,
        Q02 MEDIUMINT UNSIGNED,
        Q03 MEDIUMINT UNSIGNED,
        Q04 MEDIUMINT UNSIGNED,
        Q05 MEDIUMINT UNSIGNED,
        Q06 MEDIUMINT UNSIGNED,
        Q07 MEDIUMINT UNSIGNED,
        Q08 MEDIUMINT UNSIGNED,
        Q09 MEDIUMINT UNSIGNED,
        Q10 MEDIUMINT UNSIGNED,
        Q11 MEDIUMINT UNSIGNED,
        Q12 MEDIUMINT UNSIGNED,
        Q13 MEDIUMINT UNSIGNED,
        Q14 MEDIUMINT UNSIGNED,
        Q15 MEDIUMINT UNSIGNED,
        Q16 MEDIUMINT UNSIGNED,
        Q17 MEDIUMINT UNSIGNED,
        Q18 MEDIUMINT UNSIGNED,
        Q19 MEDIUMINT UNSIGNED,
        Q20 MEDIUMINT UNSIGNED,
        Q21 MEDIUMINT UNSIGNED,
        Q22 MEDIUMINT UNSIGNED,
        Q23 MEDIUMINT UNSIGNED,
        Q24 MEDIUMINT UNSIGNED,
        Q25 MEDIUMINT UNSIGNED,
        Q26 MEDIUMINT UNSIGNED,
        Q27 MEDIUMINT UNSIGNED,
        Q28 MEDIUMINT UNSIGNED,
        Q29 MEDIUMINT UNSIGNED,
        Q30 MEDIUMINT UNSIGNED,
        Q31 MEDIUMINT UNSIGNED,
        Q32 MEDIUMINT UNSIGNED,
        Q33 MEDIUMINT UNSIGNED,
        Q34 MEDIUMINT UNSIGNED,
        Q35 MEDIUMINT UNSIGNED,
        Q36 MEDIUMINT UNSIGNED,
        Q37 MEDIUMINT UNSIGNED,
        Q38 MEDIUMINT UNSIGNED,
        Q39 MEDIUMINT UNSIGNED,
        Q40 MEDIUMINT UNSIGNED,
        Q41 MEDIUMINT UNSIGNED,
        Q42 MEDIUMINT UNSIGNED,
        Q43 MEDIUMINT UNSIGNED,
        Q44 MEDIUMINT UNSIGNED,
        Q45 MEDIUMINT UNSIGNED,
        Q46 MEDIUMINT UNSIGNED,
        Q47 MEDIUMINT UNSIGNED,
        Q48 MEDIUMINT UNSIGNED,
        Q49 MEDIUMINT UNSIGNED,
        Q50 MEDIUMINT UNSIGNED,
        Primary key(LaneID,TileID,CycleID),
        Foreign key(MiSeqRunID) References MiSeqRun(MiSeqRunID)
        )""")
print "QualityMetrics table created"

cursor.execute(""" CREATE TABLE ExtractionMetrics (
        LaneID TINYINT UNSIGNED NOT NULL,
        TileID SMALLINT UNSIGNED NOT NULL,
        CycleID SMALLINT UNSIGNED NOT NULL,
        MiSeqRunID VARCHAR(50) NOT NULL,
        FWHM_A DECIMAL(8),
        FWHM_C DECIMAL(8),
        FWHM_G DECIMAL(8),
        FWHM_T DECIMAL(8),
        Intensity_A SMALLINT(3) UNSIGNED,
        Intensity_C SMALLINT(3) UNSIGNED,
        Intensity_G SMALLINT(3) UNSIGNED,
        Intensity_T SMALLINT(3) UNSIGNED,
        Date DATE,
        Time TIME,
        Primary key(LaneID,TileID,CycleID),
        Foreign key(MiSeqRunID) References MiSeqRun(MiSeqRunID)
        )""")
print "ExtractionMetrics table created"

cursor.execute(""" CREATE TABLE CorrectedIntMetrics (
        LaneID TINYINT UNSIGNED NOT NULL,
        TileID SMALLINT UNSIGNED NOT NULL,
        CycleID SMALLINT UNSIGNED NOT NULL,
        MiSeqRunID VARCHAR(50) NOT NULL,
        AverageIntensity SMALLINT(5) UNSIGNED,
        AverageCorrectedIntensity_A SMALLINT(5) UNSIGNED,
        AverageCorrectedIntensity_C SMALLINT(5) UNSIGNED,
        AverageCorrectedIntensity_G SMALLINT(5) UNSIGNED,
        AverageCorrectedIntensity_T SMALLINT(5) UNSIGNED,
        AverageCorrectedIntensityCalledClusters_A SMALLINT(5) UNSIGNED,
        AverageCorrectedIntensityCalledClusters_C SMALLINT(5) UNSIGNED,
        AverageCorrectedIntensityCalledClusters_G SMALLINT(5) UNSIGNED,
        AverageCorrectedIntensityCalledClusters_T SMALLINT(5) UNSIGNED,
        NumNoCalls SMALLINT UNSIGNED,
        NUM_A MEDIUMINT UNSIGNED,
        NUM_C MEDIUMINT UNSIGNED,
        NUM_G MEDIUMINT UNSIGNED,
        NUM_T MEDIUMINT UNSIGNED,
        Signal2NoiseRatio DECIMAL(8),
        Primary key(LaneID,TileID,CycleID),
        Foreign key(MiSeqRunID) References MiSeqRun(MiSeqRunID)
        )""")
print "CorrectedIntensityMetrics table created"

cursor.execute(""" CREATE TABLE ErrorMetrics (
        LaneID TINYINT UNSIGNED NOT NULL,
        TileID SMALLINT UNSIGNED NOT NULL,
        CycleID SMALLINT UNSIGNED NOT NULL,
        MiSeqRunID VARCHAR(50) NOT NULL,
        ErrorRate DECIMAL(8),
        NumPerfectRds SMALLINT(8) UNSIGNED,
        NumSingleError SMALLINT(8) UNSIGNED,
        NumDoubleError SMALLINT(8) UNSIGNED,
        NumTripleError SMALLINT(8) UNSIGNED,
        NumQuadrupleError SMALLINT(8) UNSIGNED,
        Primary key(LaneID,TileID,CycleID),
        Foreign key(MiSeqRunID) References MiSeqRun(MiSeqRunID)
        )""")
print "ErrorMetrics table created"

cursor.execute(""" CREATE TABLE TileMetrics (
        LaneID TINYINT UNSIGNED NOT NULL,
        TileID SMALLINT UNSIGNED NOT NULL,
        CodeID SMALLINT UNSIGNED NOT NULL,
        MiSeqRunID VARCHAR(50) NOT NULL,
        Value DECIMAL(8),
        Primary key(LaneID,TileID,CodeID),
        Foreign key(MiSeqRunID) References MiSeqRun(MiSeqRunID)
        )""")
print "TileMetrics table created"

cursor.execute(""" CREATE TABLE IndexMetricsMSR (
        LaneID TINYINT UNSIGNED NOT NULL,
        TileID SMALLINT UNSIGNED NOT NULL,
        ReadNum TINYINT(2) UNSIGNED NOT NULL,
        MiSeqRunID VARCHAR(50) NOT NULL,
        IndexName VARCHAR(50),
        NumControlClusters MEDIUMINT UNSIGNED,
        SampleName VARCHAR(20),
        ProjectName VARCHAR(50),
        Primary key(LaneID,TileID,ReadNum),
        Foreign key(MiSeqRunID) References MiSeqRun(MiSeqRunID)
        )""")
print "IndexMetricsMSR table created"