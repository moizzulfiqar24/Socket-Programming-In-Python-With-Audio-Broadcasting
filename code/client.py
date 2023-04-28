# import the necessary libraries
import socket
import hashlib
import pyaudio

# define audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# calculate checksum of a file
def calculate_checksum(file_path):
    sha256_hash = hashlib.sha256()  # sha256 hash object
    with open(file_path, "rb") as f:  # open the file in binary read mode
        # iteratively read and update hash
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()  # return the hexadecimal value of the hash

# function to start the client
def start_client():
    host = 'localhost'  # define the host
    port = 12345  # define the port

    while True:
        # prompt the user to enter the operation mode or to exit
        mode = input('\nEnter operation mode (file/audio) or type "exit" to quit: ')

        if mode == 'file':
            start_file_client(host, port)
        elif mode == 'audio':
            start_audio_client(host, port)
        elif mode == 'exit':
            break
        else:
            print('Invalid mode. Please enter "file", "audio", or "exit"')

# function to start the file client
def start_file_client(host, port):
    file_path = input("Enter file name (please include extension too for example image.jpg, file.txt, video.mp4, etc) : ")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # create a new socket object
            try:
                s.connect((host, port))  # connect the socket to the host and port
            except socket.error as e:
                print(f"Could not connect to server: {e}")
                return

            checksum = calculate_checksum(file_path)  # calculate the checksum of the file
            s.send(checksum.encode('utf-8'))  # send the checksum to the server first

            with open(file_path, 'rb') as f:  # open the file in binary read mode
                s.sendfile(f)  # send the file to the server

            print('File sent to server.')
            print(f'Sent checksum: {checksum}')  # print the checksum that was sent

    except Exception as e:  # catch any exception that occurs during the file transfer
        print(f"Client error: {e}")

# function to start the audio client
def start_audio_client(host, port):
    # initialize PyAudio
    audio = pyaudio.PyAudio()

    # open a new audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # create a new socket object
            try:
                s.connect((host, port))  # connect the socket to the host and port
            except socket.error as e:
                print(f'Could not connect to server: {e}')
                return

            print('Receiving audio... Press Ctrl+C to stop (Will work in terminal only).')

            try:
                # continuously receive data from the server and write it to the audio stream
                while True:
                    data = s.recv(CHUNK)
                    stream.write(data)
            except KeyboardInterrupt:
                print('Stopped receiving audio.')  # print a message to indicate that the audio reception has been stopped

    except Exception as e:  # catch any exception that occurs during the audio reception
        print(f'Client error: {e}')

    finally:
        stream.stop_stream()  # stop the audio stream
        stream.close()  # close the audio stream
        audio.terminate()  # terminate the PyAudio

if __name__ == '__main__':
    start_client()  # start the client
