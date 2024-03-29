'''
Created on 5 Nov 2015

@author: Sara
'''

class ParseInterOpMetrics(object):
    '''
    A series of methods to parse the Index Metrics binary file generated by the MiSeqReporter software_version
    '''
    #Class variables (i.e. not specific to a single instance)- similar but not the same as static variables in java
    #http://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide
    
    def __init__(self,filehandle):
        #global ENDIANNESS
        #global ENCODING_DICTIONARY
        import struct as s
        self.s = s
        import datetime as dt
        self.dt = dt
        import math
        self.math = math
        self.Y = 6 #Known index of Y in the bytearray- could attempt to retrieve this better another time
        self.YV = 4 #Known size of YV- could attempt to retrieve this better another time
        self.file_handle = filehandle
        self.ENDIANNESS = "<"
        self.ENCODING_DICTIONARY = {"x":1,"c":1,"b":1,"B":1,"?":1,"h":2,"H":2,"i":4,"I":4,"l":4,"L":4,"q":8,"Q":8,"f":4,"d":8,"s":1,"p":1,"P":1}
    
    def open_file_to_bytearray(self,filehandle):
        values = bytearray()
        with open(filehandle, "rb") as f:
            for line in f:
                for b in line:
                    values.append(b)
        return values #This is the bytearray of the data
    
    def convert_bytes_index(self,the_bytearray,supported_version_number):
        for index in xrange(len(the_bytearray)):
            byte_start = (index) #This will be where I will want to start the next readout from
            if index < 1:
                value = self.s.unpack_from(self.ENDIANNESS + "B",the_bytearray,index)
                if value[0] != supported_version_number:
                    raise Exception("Unsupported file version")
            else:
                #return get_chunk_len(byte_start,the_bytearray)
                #print byte_start
                return byte_start
            
    def get_Y(self,readout_start,the_bytearray,offset=0):
        ind_Y = self.Y
        index_bytes_length = self.ENCODING_DICTIONARY.get("H",None)
        Y = self.s.unpack_from(self.ENDIANNESS + "H",the_bytearray[(offset+readout_start+ind_Y):(offset+readout_start+ind_Y+index_bytes_length)],0)
        return Y[0]
    
    def get_V(self,readout_start,the_bytearray,offset=0):
        ind_Y = self.Y
        ind_YV = self.YV
        index_bytes_length = self.ENCODING_DICTIONARY.get("H",None)
        Y = self.s.unpack_from(self.ENDIANNESS + "H",the_bytearray[(offset+readout_start+ind_Y):(offset+readout_start+ind_Y+index_bytes_length)],0)
        ind_V = ind_Y + index_bytes_length + Y[0] + ind_YV
        V = self.s.unpack_from(self.ENDIANNESS + "H",the_bytearray[(offset+readout_start+ind_V):(offset+readout_start+ind_V+index_bytes_length)],0)
        return V[0]
    
    def get_W(self,readout_start,the_bytearray,offset=0):
        ind_Y = self.Y
        ind_YV = self.YV
        index_bytes_length = self.ENCODING_DICTIONARY.get("H",None)
        Y = self.s.unpack_from(self.ENDIANNESS + "H",the_bytearray[(offset+readout_start+ind_Y):(offset+readout_start+ind_Y+index_bytes_length)],0)
        ind_V = ind_Y + index_bytes_length + Y[0] + ind_YV
        V = self.s.unpack_from(self.ENDIANNESS + "H",the_bytearray[(offset+readout_start+ind_V):(offset+readout_start+ind_V+index_bytes_length)],0)
        ind_W = ind_V + index_bytes_length + V[0]
        W = self.s.unpack_from(self.ENDIANNESS + "H",the_bytearray[(offset+readout_start+ind_W):(offset+readout_start+ind_W+index_bytes_length)],0)
        return W[0]
    
    def get_entry_len_ind(self,readout_start,the_bytearray,offset=0):
        '''
        This function reads out the size of the 'chunk' of the bytearray
        '''
        ind_Y = self.Y
        ind_YV = self.YV
        index_bytes_length = self.ENCODING_DICTIONARY.get("H",None)
        Y = self.s.unpack_from(self.ENDIANNESS + "H",the_bytearray[(offset+readout_start+ind_Y):(offset+readout_start+ind_Y+index_bytes_length)],0)
        ind_V = ind_Y + index_bytes_length + Y[0] + ind_YV
        V = self.s.unpack_from(self.ENDIANNESS + "H",the_bytearray[(offset+readout_start+ind_V):(offset+readout_start+ind_V+index_bytes_length)],0)
        ind_W = ind_V + index_bytes_length + V[0]
        W = self.s.unpack_from(self.ENDIANNESS + "H",the_bytearray[(offset+readout_start+ind_W):(offset+readout_start+ind_W+index_bytes_length)],0)
        return (ind_W + index_bytes_length + W[0])
    
    def get_array_segment(self,readout_start,the_bytearray,entry_length,offset):
        '''
        This function reads out the array segment for de-encoding (i.e. the bit which corresponds to a single row)
        '''
        byte_start = readout_start + offset
        return the_bytearray[byte_start:(byte_start+entry_length)]
    
    def get_encoding_string_var(self,Y,V,W,encoding):
        '''
        Necessary function to cope with when the encoding string codes for variable values indicating the length of the
        subsequent string
        '''
        encoding_constants = (Y,V,W)
        let = []
        count = 0
        for letter in encoding:
            if letter != 's':
                let.append(letter)
            elif letter == 's':
                #print "arr_start is " + str(arr_start)
                let.pop() #Pop from the stack (pop always pops from the end of a stack)
                let.append(letter*encoding_constants[count])
                encoding_string = "".join(let)
                count += 1
        return encoding_string
    
    def get_values_simple(self,encoding_string,array_segment):
        return self.s.unpack_from(self.ENDIANNESS + encoding_string,array_segment)
    
    def handle_nan(self,lst):
        new_list = []
        for entry in lst:
            #print entry
            #print type(entry)
            if self.math.isnan(entry):
                new_list.append(0)
            else:
                new_list.append(entry)
        return new_list
                
            
    
    def get_datetime(self,encoding_string,array_segment):
        size = 0
        for enc in encoding_string:
            enc_size = self.ENCODING_DICTIONARY.get(enc,None)
            size += enc_size
        #return size
        dt_bytes = array_segment[size:len(array_segment)]
        bitlst = []
        for b in dt_bytes:
            for i in (xrange(8)): #reversed(xrange(8)): The reversed here doesn't work as it is byte order reversed as well as bit order within bytes
                bitlst.append((b >> i) & 1)
        bitlst[((len(dt_bytes)*8)-1)] = 0
        bitlst[((len(dt_bytes)*8)-2)] = 0
        binary = ''.join(str(c) for c in bitlst)[::-1] #Reversed as is little endian
        ticks = int(binary,2)
        datetime = self.dt.datetime(1, 1, 1) + self.dt.timedelta(microseconds = ticks/10)
        return str(datetime)
    
    def get_s(self,encoding):
        '''
        Find the positions of the s's in the encoding string.
        Pass in the result of the encoding_string function, NOT the raw encoding string.
        '''
        s_indices = []
        for index,letter in enumerate(encoding):
            if letter == 's' and encoding[index-1] != 's': #Index of first s each time
                s_indices.append(index)   
        return s_indices
    
    def get_formatted_values(self,Y,V,W,s_indices,raw_result):
        '''
        Join together the strings so that each one is not a new entry.
        Also remove the numbers encoding the string lengths as they are not useful data.
        '''        
        #Create a list for the new data
        formatted = []
        for entry in raw_result[0:(s_indices[0]-1)]: #-1 removes the entry denoting the string length
            formatted.append(entry)
        formatted.append("".join(raw_result[s_indices[0]:((s_indices[0])+Y)]))
        for entry in raw_result[((s_indices[0])+Y):(s_indices[1]-1)]: #-1 removes the entry denoting the string length
            formatted.append(entry)
        formatted.append("".join(raw_result[s_indices[1]:((s_indices[1])+V)]))
        if len(s_indices) < 3:
            formatted.append(' ')
        else:
            for entry in raw_result[((s_indices[1])+V):(s_indices[2]-1)]: #-1 removes the entry denoting the string length
                formatted.append(entry)
            formatted.append("".join(raw_result[s_indices[2]:((s_indices[2])+W)]))
        return formatted
        for entry in raw_result[((s_indices[1])+V):(s_indices[2]-1)]: #-1 removes the entry denoting the string length
            formatted.append(entry)
        formatted.append("".join(raw_result[s_indices[2]:((s_indices[2])+W)]))
        return formatted
    
    
    def convert_bytes(self,the_bytearray,supported_version_number):
        for index in xrange(len(the_bytearray)):
            byte_start = (index) #This will be where I will want to start the next readout from
            if index < 2: #FIX HERE SEE OTHER PARSER
                value = self.s.unpack_from(self.ENDIANNESS + "B",the_bytearray,index)
                if (index == 0) and value[0] != supported_version_number:
                    raise Exception("Unsupported file version")
            else:
                #return get_chunk_len(byte_start,the_bytearray)
                return byte_start
    
    
    
    def get_entry_len(self,the_bytearray):
        for index in xrange(len(the_bytearray)):
            if index == 1: #First byte is the length of the record
                value = self.s.unpack_from(self.ENDIANNESS + "B",the_bytearray,index)
                return value[0]
                #return value
            
            #else:
                #return get_chunk_len(byte_start,the_bytearray)
                #return byte_start
        
        
        
        
        
        

    def sillytest(self,encoding):
        for index,char in enumerate(encoding):
            #print index
            if char == 'Y':
                #-1 because the Y is actually the entry after where the type for Y is encoded
                #and we a priori know that all the entries are H (see encoding string)
                print encoding[0:index-1]
                print (index-1) * self.ENCODING_DICTIONARY.get("H",None) 
            elif char == 'V':
                print encoding[index-2]
            elif char == 'W':
                print index
    