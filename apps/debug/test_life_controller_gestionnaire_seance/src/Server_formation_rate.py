import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

def image_capture(msg):
    print ("image_capture received : " + str(msg) )

def seance_end(msg):
    print ("seance_end received : " + str(msg) )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
    default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
    type=int, default=3335, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/image_capture", image_capture)
    """dispatcher.map("/seance_end", seance_end )"""


    """test"""
    """dispatcher.map("/first_photo", print)
    dispatcher.map("/seance_end", print)"""


    server = osc_server.ThreadingOSCUDPServer(
            (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
    server.close(); 