# Socket Programming In Python
This project is a simple implementation of file and audio streaming between a client and a server using Python's socket and threading libraries, and PyAudio for audio streaming. The program allows the client to send a file to the server, which then saves the file to disk. The server can also broadcast audio to the client.

# Getting Started
### Prerequisites
- Python 3
- PyAudio
- A file to send 

# Usage
The project consists of two scripts: server.py and client.py.
1. Run server.py first. It will ask for the operation mode. Type 'file' for file transfer or 'audio' for audio streaming. The server then waits for a client to connect.
2. Run client.py. Similar to the server, it will ask for the operation mode. Type 'file' for file transfer or 'audio' for audio streaming.

For 'file' mode:
- The client will prompt you for the file name. Enter the full name of the file (including the extension).
- The client calculates the checksum of the file and sends it to the server.
- The client sends the file to the server.
- The server receives the file and saves it to disk.
- The server calculates the checksum of the received file and compares it to the checksum received from the client to verify the integrity of the file.

For 'audio' mode:

- The server starts broadcasting audio from its microphone.
- The client receives the audio and plays it through its speakers.
- Press Ctrl+C in the client terminal to stop receiving audio.

# How The Code Actually Works
### File Transfer
- The server.py script starts by creating a socket object using the socket.socket() function and binding it to a specific host and port using the s.bind() function. The script then listens for incoming connections using the s.listen() function.
- The client.py script also creates a socket object and connects to the server using the s.connect() function.
- When the client enters the 'file' mode, it prompts the user for the file name, calculates the checksum of the file using the calculate_checksum() function, and sends it to the server using the s.send() function.
- The client then opens the file in binary read mode and sends the file to the server using the s.sendfile() function.
- The server receives the connection using the s.accept() function, calculates the received file's checksum using the calculate_checksum() function, and compares it to the checksum sent by the client to verify the integrity of the file. If the checksums match, the server saves the file to disk.
- The server and client scripts both implement error handling to ensure that files are transferred correctly. The try-except block in the handle_file_client() function of server.py catches any errors that occur during the file transfer, and the try-except block in the start_file_client() function of client.py catches any errors that occur during the transfer.
### Audio Streaming
- When the server enters the 'audio' mode, it initializes PyAudio using the pyaudio.PyAudio() function and opens a new audio stream using the audio.open() function. The server then starts broadcasting audio using a loop that continuously reads data from the audio stream and sends it to the client using the conn.sendall() function.
- When the client enters the 'audio' mode, it also initializes PyAudio and opens a new audio stream using the audio.open() function. The client then connects to the server using the s.connect() function and starts receiving audio using a loop that continuously reads data from the server using the s.recv() function and writes it to the audio stream using the stream.write() function. The client can stop receiving audio by pressing Ctrl+C in the terminal.
- Both the server and client scripts implement error handling to ensure that audio is transmitted correctly. The try-except block in the handle_audio_client() function of server.py catches any errors that occur during the audio broadcast, and the try-except block in the start_audio_client() function of client.py catches any errors that occur during the audio reception.
### Checksum Calculation
- The checksum of the file is calculated using the SHA-256 algorithm, which is a secure hash function that generates a 256-bit (32-byte) hash value. The calculate_checksum() function opens the file in binary read mode and iteratively reads and updates the hash value using the sha256_hash.update() function. The function then returns the hexadecimal value of the hash using the sha256_hash.hexdigest() function.
### Error Handling
- Both the server and client scripts implement error handling to ensure that files and audio are transferred correctly. The try-except block in the handle_file_client() function of server.py catches any errors that occur during the file transfer, and the try-except block in the start_file_client() function of client.py catches any errors that occur during the transfer. Similarly, the try-except block in the handle_audio_client() function of server.py catches any errors that occur during the audio broadcast, and the try-except block in the start_audio_client() function of client.py catches any errors that occur during the audio reception

# Notes
- For 'audio' mode, the server uses its microphone to broadcast audio, and the client uses its speakers to play the received audio. Therefore, the server and client machines should have a working microphone and speakers, respectively.
