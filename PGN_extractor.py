'''
@author: Ahmed Amokrane

This is a script that listens on a CAN interface and extracts the PGNs from the packets.
    
@Requires: This requires can-utils and python-can to be installed

@How_it_works:
It listens on a CAN interface (physical or virtual) and extracts the PGNs (J1939 and related standards).

'''

import can
import xlrd


bustype = 'socketcan_ctypes'
channel = 'vcan0'
timeout = 1 #Timeout in seconds

#Open the CAN interface
bus = can.interface.Bus(channel=channel, bustype=bustype)

while True:
        can_message = bus.recv(timeout)
        if can_message is None:
            break;
           
        #Extract and display the PGN
	timestamp = can_message.timestamp
	priority = (can_message.arbitration_id>> 26) % 8
	reserved = (can_message.arbitration_id >> 25) % 2
	data_page = (can_message.arbitration_id >> 24) % 2
	pdu_format = (can_message.arbitration_id >> 16) % 256
	pdu_specific = (can_message.arbitration_id >> 8) % 256
	source_addr = can_message.arbitration_id % 256
	
	data = can_message.data
	dlc = can_message.dlc
	is_remote_frame = can_message.is_remote_frame
	is_error_frame = can_message.is_error_frame
	
	print '\n********************'
	print 'New frame received '
	print '********************'
	
	#PGN construction from the parameters 
	pgn = pdu_specific + pdu_format*256 + data_page*256*256 + reserved*256*256*2
	
	#print the received PGN and parameters
	fields_str = ["Priority: " + str(priority)]
        fields_str.append("reserved: "+str(reserved))
        
        fields_str.append("DLC: {0:d}".format(dlc))
        
        data_pg = "Data Page: {0:02x}".format(data_page)
        fields_str.append(data_pg.rjust(12, " "))
        
        pdu_fmt = "PDU Format: {0:02x}".format(pdu_format)
        fields_str.append(pdu_fmt.rjust(12, " "))
        
        if(pdu_format < 240):
	        pdu_sp = "Destination Address: {0:02x}".format(pdu_specific)
        	fields_str.append(pdu_sp.rjust(12, " "))
        else:
        	pdu_sp = "Group Extension: {0:02x}".format(pdu_specific)
        	fields_str.append(pdu_sp.rjust(12, " "))
        
        sa = "Source Address: {0:02x}".format(source_addr)
        fields_str.append(sa.rjust(12, " "))
        
        fields_str.append(str(pgn).rjust(12, " "))
        
        print fields_str
        
        
