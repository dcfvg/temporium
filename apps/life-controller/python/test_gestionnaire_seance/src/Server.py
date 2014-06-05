import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

def seance_start(msg):
    print ("seance_start received : " + str(msg) )

def image_formation(msg):
    print ("image_formation received : " + str(msg) )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
    default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
    type=int, default=3333, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/debug", print)
    dispatcher.map("/seance_start", seance_start)
    dispatcher.map("/image_formation", image_formation )

    """test"""
    """dispatcher.map("/first_photo", print)
    dispatcher.map("/seance_end", print)"""


    server = osc_server.ThreadingOSCUDPServer(
            (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
    server.close(); 