#!/usr/bin/python3

from multiprocessing import Pool
from functools import partial
import re
import socket
import time
import argparse
import requests
import random
import lists

def req(id, config):
    print(id)
    user_agent = 'User-Agent: Requestly\r\n".encode()'
    for i in config:
        url = f"https://{config['host']}{config['path']}"
        while time.time() <= config['t_end']:
            match config['type']:
                case "cache-bust":
                    hash = {"_":random.getrandbits(24)}
                    match config['method']:
                        case "GET":
                            r = requests.get(url, params=hash, headers={"X-CSOC-Client-IP":f"{random.choice(lists.attacking_ips)}","User-Agent": f"{random.choice(lists.attacking_user_agents)}"})
                        case "POST":
                            r = requests.post(url, params=hash, headers={"X-CSOC-Client-IP":f"{random.choice(lists.attacking_ips)}","User-Agent": f"{random.choice(lists.attacking_user_agents)}"})
                case "volume":
                    match config['method']:
                        case "GET":
                            r = requests.get(url, headers={"X-CSOC-Client-IP":f"{random.choice(lists.attacking_ips)}","User-Agent": f"{random.choice(lists.attacking_user_agents)}"})
                        case "POST":
                            r = requests.post(url, headers={"X-CSOC-Client-IP":f"{random.choice(lists.attacking_ips)}","User-Agent": f"{random.choice(lists.attacking_user_agents)}"}) 
                    #i = i + 1



def manager(config):
    print('''
  _____                            _   _       
 |  __ \                          | | | |      
 | |__) |___  __ _ _   _  ___  ___| |_| |_   _ 
 |  _  // _ \/ _` | | | |/ _ \/ __| __| | | | |
 | | \ \  __/ (_| | |_| |  __/\__ \ |_| | |_| |
 |_|  \_\___|\__, |\__,_|\___||___/\__|_|\__, |
                | |                       __/ |
                |_|                      |___/        
''')
    print(f"Starting Requests to {config['host']}:{config['port']}{config['path']} for {config['t_end']} seconds")
    t_end = time.time() + config['t_end']
    config['t_end'] = t_end
    with Pool(2) as p:
        path = partial(req, config=config)
        p.map(path, range(2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Traffic Generator",
    epilog='''

  _____                            _   _       
 |  __ \                          | | | |      
 | |__) |___  __ _ _   _  ___  ___| |_| |_   _ 
 |  _  // _ \/ _` | | | |/ _ \/ __| __| | | | |
 | | \ \  __/ (_| | |_| |  __/\__ \ |_| | |_| |
 |_|  \_\___|\__, |\__,_|\___||___/\__|_|\__, |
                | |                       __/ |
                |_|                      |___/ 
               
''')
    parser.add_argument('--host', help="Host", type=str)
    parser.add_argument('--path', help='Path', type=str)
    parser.add_argument('-p', help= 'port', type=int)
    parser.add_argument('-m', help= 'method', type=str)
    parser.add_argument('-t', help= 'time in seconds to run the traffic for', type=int)
    parser.add_argument('-ty', help= 'type of attack', type=str)
    args = parser.parse_args()
    if args.host is None: 
        print('Please provide a host')
        exit()
    
    config = {'host':args.host, 'path': args.path, 'method': str.upper(args.m),'type': str.lower(args.ty),'t_end': args.t, 'port': args.p}
    print(config)
    manager(config)
        
