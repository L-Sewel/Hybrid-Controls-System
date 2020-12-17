import socket
import queue


class NoConnection(Exception):
    """
    A custom exception raised when attempting to utilize the server when no connection has been made
    """
    pass


class InvalidIp(Exception):
    """
    A custom exception raised when an invalid IP is provided when creating the server
    """
    pass


class Server:

    def __init__(self, host, port):
        """
        Initializes the server object
        Creates an address tuple from the given host and port
        :param host: The IP of the server, will be received form the GUI
        :param port: The port that the socket will be connecting on, is hard coded to 9999
        """
        self.HOST = host  # the host IP
        self.PORT = port  # the host port
        self.address = (self.HOST, self.PORT)  # a tuple used by the socket object
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # the server socket object
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # allows the server and client to reconnect
        self.client = None  # just a placeholder for now, becomes the client when a successfully connected
        self.c_address = None  # just a placeholder for now, becomes the client when a successfully connected
        self.feedback_queue = queue.Queue()  # used to store feedback from client


    def initialize_connection(self):
        """
        Binds the server socket to the address
        Attempts to connect to the client
        Once connected self.client refers to the client socket
        self.c_address is the address of the client
        :return:
        """
        try:
            self.server.bind(self.address)  # binds the server object to the HOST and PORT

        except socket.gaierror: # this is an exception raised if the ip is invalid
            raise InvalidIp
        self.server.listen(5)  # waits for a connection from the client
        self.client, self.c_address = self.server.accept()  # when a successful connection is made

    def end_connection(self):
        """
        cleans up the sockets when we are done with them, leaving them open can cause problems
        :return: nothing
        """
        self.server.close()
        self.client.close()

        self.server = None
        self.client = None

    def send_states(self, data):
        """
        Send state to client, used when input is received from GUI
        :param data: The state being sent
        :return: nothing
        """

        self.client.sendall(data.encode())

    def receive_states(self):
        """
        Receive data from client and tokenize it, then add it to the instruction queue
        :return: nothing
        """
        if self.client is None:
            raise NoConnection
        try:
            data = self.client.recv(1024).decode()  # receives data which it decodes() into a string
            print(data)
            data = data.split(" ")  # splits string into a list using spaces as the delimiter
            data = tuple(data)
            self.feedback_queue.put(data)  # adds each list entry to the queue
        except Exception as e:
            print(f'line 92 {e}')
