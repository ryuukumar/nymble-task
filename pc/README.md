# PC Software

This part of the code is designed to run on any old PC with serial connectivity and Python support.

This utilises Python and the `pyserial` package to send/receive data. The speed is tracked automatically.

## Running the Script

First, please set the `serial_port` variable in Python to the appropriate port.

```bash
# Install serial package
pip install pyserial

# Run the i/o code
python sender.py
```

`sender.py` monitors the speed during transmission and receiving by sending the data in 'chunks' and tracking the time it takes for the chunk to be sent.

You may set the variable `bytes_per_update` to change how many bytes there are in each chunk. Higher values offer higher actual transfer speed, but slower live updates.
