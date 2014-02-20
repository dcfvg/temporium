import OSC
import argparse

parser = argparse.ArgumentParser(description='Send an OSC Message.')
parser.add_argument('host',help='IP Address')
parser.add_argument('port',help='Port')
parser.add_argument('message',help='Message')
args = parser.parse_args()

ip_address = args.host
port = int(args.port)

msg = OSC.OSCMessage("/exposeFlashCommander")
msg.extend(args.message)

oscClient = OSC.OSCClient()
oscClient.sendto(msg,(ip_address,port))