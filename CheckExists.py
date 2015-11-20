'''
Created on 4 Nov 2015

@author: Sara
'''

class CheckExists(object):
    '''
    A class to check if there is already an entry in the database corresponding to this entry and if so skip execution
    of the rest of the code (designed to save time)
    '''
    
    def __init__(self,miseqrun_name,username,password):
        self.miseqrun_name = miseqrun_name
        import MySQLdb
        self.MySQLdb = MySQLdb
        import sys
        self.username = username
        self.password = password
        
        try:
            db = self.MySQLdb.connect("localhost",username,password, "ngsqc" ) #Pass username and password as command line arguments

        except:
            sys.exit("Enter correct username and password!")
    
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        
        self.db = db
        self.cursor = cursor
    
    
    def checkData(self):
        '''
        Checks if there is a matching entry in the database to be queried
        '''
        cmd = ('''SELECT ngsqc.miseqrun.miseqrunid
                    FROM ngsqc.miseqrun
                    WHERE ngsqc.miseqrun.miseqrunid = %s ''')
                                
        data = [self.miseqrun_name]
        
        self.cursor.executemany(cmd, [data])
        result = self.cursor.fetchall()
        if result:
            #print "not empty"
            return True
        else:
            #print "empty"
            return False
    