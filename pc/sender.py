
#
#	SENDER.PY
#	Utility script to send some text over a serial port, verify whether it is
#	echoed correctly, and provide live speed statistics.
# 





### Imports

import serial
import time





### Defintions

text_file			= 'text.txt'		# source for the text (<1024 characters!)
serial_port			= '/dev/ttyACM0'	# arduino serial port
baud_rate			= 2400
bytes_per_update	= 16				# bytes to be sent between speed checks





### Function Definitions

# Calculates transfer speed based on start and end times and sends to stdout
def print_time_stat (start_time, end_time, chunk_size):
	time_taken = end_time - start_time
	transfer_speed = chunk_size * 8.0/time_taken
	print (f"\rSpeed: {transfer_speed} bits/second  ", end='', flush=True)
	return time_taken

# Sends a chunk to the serial device and returns the time taken
def send_data (arduino_connection, chunk):
	start_time = time.time()
	arduino_connection.write(chunk)
	end_time = time.time()
	time_taken = print_time_stat(start_time, end_time, len(chunk))
	return time_taken

# Receives a chunk of chunk_size and returns the time taken and contents of the chunk
def receive_chunk (arduino_connection, chunk_size):
	start_time = time.time()
	raw_response = arduino_connection.read(size=chunk_size)
	decoded_response = raw_response.decode()
	end_time = time.time()
	time_taken = print_time_stat(start_time, end_time, len(raw_response))
	return time_taken, decoded_response, len(raw_response)





### Code



# Read text file
text_to_send = ""
with open(text_file) as f:
	text_to_send = f.read()

if text_to_send == "":
	print ("Text file is empty! Aborting.")
	exit()

text_to_send += '\0'


	
# Establish connection with arduino
arduino_connection = None

print ("Attempting to establish connection... ", end='', flush=True)
try:
	arduino_connection = serial.Serial(serial_port, baud_rate)
except serial.SerialException as e:
	print ("failed to establish connection. Terminating.")
	exit()
print ("done.")

print ("Waiting for 5 seconds due to arduino reset... ", end='', flush=True)
time.sleep(5)
print ("done.")



# Send data
data_to_send = text_to_send.encode()
chunks_to_send = [data_to_send[i:i+bytes_per_update] for i in range(0, len(data_to_send), bytes_per_update)]

total_time = 0
print ("Sending data... ")
for chunk in chunks_to_send:
	time_taken = send_data(arduino_connection, chunk)
	total_time += time_taken
print ("\ndone.")
print (f"Average write speed: {len(data_to_send)*8.0/total_time} bits/second\n")



# Read response
time.sleep(1)

response = ""
total_time = 0
response_length = 0

print ("Receiving data... ")
for i in range(0, len(text_to_send), bytes_per_update):
	current_chunk_size = min(len(text_to_send), i+bytes_per_update)-i
	time_taken, iteration_response, iteration_response_length = receive_chunk(arduino_connection, current_chunk_size)
	total_time += time_taken
	response += iteration_response
	response_length += iteration_response_length

print ("\ndone.")
print (f"Average read speed: {response_length*8.0/total_time} bits/second\n")



# Verify response
if response == text_to_send:
	print ("Success! Message received is identical to message sent.")
print (f"Received message:\n{response}")
print (f"[{len(response)} characters]")





### EOF



