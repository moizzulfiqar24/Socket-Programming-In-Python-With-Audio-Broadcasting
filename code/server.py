# import the necessary libraries
import socket
import threading
import hashlib
import struct
import pyaudio

# define audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# calculate checksum of a file
def calculate_checksum(file_path):
    sha256_hash = hashlib.sha256()  # sha256 hash object (for checksum)
    with open(file_path,"rb") as f:  # open the file in binary read mode
        # iteratively read and update hash
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()  # return the hexadecimal value of the hash

# handle different clients based on mode (file or audio)
def handle_client(conn, addr, mode):
    if mode == 'file':
        handle_file_client(conn, addr)
    elif mode == 'audio':
        handle_audio_client(conn, addr)

# global counter to track received files (to save files)
count = 1

# handle file transfer from client
def handle_file_client(conn, addr):
    global count  # global variable
    print(f'Connected client by {addr}')
    name = "received_file " + str(count)  # create a unique name for the received file

    # begin the try-except block to catch any errors during the file transfer
    try:
        # receive the checksum of the file from the client
        received_checksum = conn.recv(64).decode('utf-8')

        # open the file in binary write mode
        with open(name, 'wb') as f:
            # continuously receive data from the client and write it to the file
            while True:
                data = conn.recv(1024)
                if not data:  # if no data is received, break the loop
                    break
                f.write(data)

        # print the successful reception of the file
        print('File received and saved to disk.')

        # calculate the checksum of the received file
        checksum = calculate_checksum(name)

        # print the received and calculated checksums
        print(f'Received checksum: {received_checksum}')
        print(f'Calculated checksum: {checksum}')

        # verify the received file by comparing checksums
        if received_checksum == checksum:
            print('Checksums match, file transferred correctly.')
        else:
            print('Checksums do not match, error during file transfer.')

        count += 1  # increment file counter

    except Exception as e:  # catch any exception that occurs during the file transfer
        print(f"Error while receiving file: {e}")

    finally:
        conn.close()  # close the connection

# function to handle audio stream from client
def handle_audio_client(conn, addr):
    print(f'Connected client by {addr}')

    # initialize PyAudio
    audio = pyaudio.PyAudio()

    # open a new audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print('Broadcasting audio...')

    try:
        # continuously read data from the audio stream and send it to the client
        while True:
            data = stream.read(CHUNK)
            conn.sendall(data)

    except BrokenPipeError:
        print(f'Broadcasting stopped.')

    except Exception as e: # catch any exception that occurs during the audio broadcast
        print(f'Error broadcasting audio: {e}')

    finally:
        stream.stop_stream()  # stop the audio stream
        stream.close()  # close the audio stream
        audio.terminate()  # terminate PyAudio
        conn.close()  # close the connection


# function to start the server
def start_server():
    host = 'localhost'  # define the host
    port = 12345  # define the port

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # create a new socket object
            s.bind((host, port))  # bind the socket to the host and port
            s.listen()  # enable the server to accept connections

            while True:
                mode = input('\nEnter operation mode (file/audio): ')  # prompt the user to enter the operation mode
                print("Waiting for client to join")

                conn, addr = s.accept()  # accept a new connection
                thread = threading.Thread(target=handle_client,
                                          args=(conn, addr, mode))  # create a new thread for the client
                thread.start()  # start the new thread
                thread.join()  # wait for the thread to finish

    except Exception as e:  # catch any exception that occurs during the server operation
        print(f'Server error: {e}')


if __name__ == '__main__':
    start_server()  # start server