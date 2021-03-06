from tcpsockets import server, logger
from typing import List
import pickle

srvr = server.ParallelServer()
chat_buffer: List[str] = []


@srvr.client_handler
def handler(clnt: server.Client):
    global chat_buffer
    while srvr.running:
        req = clnt.receive(byte_converter=pickle.loads)
        if req == "GET":
            clnt.send(chat_buffer, pickle.dumps)
        elif req == "POST":
            chat_buffer.extend(clnt.receive())
        elif req == "QUIT":
            clnt.close()
            return
        else:
            logger.log(f"Client {clnt.client_connection_id} sent illegal request '{req}'.")
            clnt.close()
            return


srvr.start()

while input() != "q":
    pass
srvr.stop_running()
