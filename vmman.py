#!/usr/bin/python3


import docker
import argparse
import configparser
import json
import time
from tabulate import tabulate
import sys


class DockerAutomation():

    @staticmethod 
    def start_container(container_ind, client):
        print(config["ids"][container_ind])
        container = client.containers.get(config["ids"][container_ind])
        if container.attrs["State"]["Running"]:
            print("Docker container {} with ID {} already running, getting VNC URL".format(container_ind, container.attrs["Config"]["Hostname"]))
            output = container.exec_run("curl -s localhost:4040/api/tunnels | jq -r .tunnels[0].public_url")
            url = json.loads(output.output)["tunnels"][0]["public_url"]
            print("URL for VNC access is: {}".format(url))

        else:
            print("Starting Docker container {} with ID {}, getting VNC URL".format(container_ind, container.attrs["Config"]["Hostname"]))
            
            container.start()
            container.exec_run("ngrok http 80", stdout=False, stream=True )
            time.sleep(5)
            output = container.exec_run("curl -s localhost:4040/api/tunnels | jq -r .tunnels[0].public_url")
            url = json.loads(output.output)["tunnels"][0]["public_url"]
            print("NOTE: This url will only last for the current session, do not save this url or use it after you have stopped your container")
            print("URL for VNC access is: {}".format(url))

    @staticmethod
    def stop_container(container_ind, client):
        container = client.containers.get(config["ids"][container_ind])
        if container.attrs["State"]["Running"]:
            print("Stopping container {} with ID {}".format(container_ind, container.attrs["Config"]["Hostname"]))
            container.stop()
            
        else:
            print("Docker container {} with ID {} is not running".format(container_ind, container.attrs["Config"]["Hostname"]))
            
    @staticmethod
    def list_container(client):
        table_list = [["#","ID", "Name", "Status", "Image"]]
        for id in config["ids"]:
            container = client.containers.get(config["ids"][id])
            row = [id, container.short_id, container.name, container.status, container.image.tags[0]]
            table_list.append(row)
        print(tabulate(table_list))




if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("/home/container_ids")

    parser = argparse.ArgumentParser(description='Start given docker containers, and give url for novnc.')
    
    parser.add_argument('-start',  
                        help='Starts the given docker container and gives url for novnc', nargs=1, default= None)
    parser.add_argument('-stop', 
                        help='Stops the given docker container', nargs=1, default= None)
    parser.add_argument('-list', 
                        help='Lists all docker VMs and their current state', action='store_true')


    args = parser.parse_args()
    client = docker.from_env()
    if len(sys.argv)==1:
        # display help message when no args are passed.
        print("Please enter a valid id for a docker VM")
        parser.print_help()
        sys.exit(1)

    if args.start != None:
        assert args.start[0] in config["ids"], "ID not in container config file"
        DockerAutomation.start_container(args.start[0], client)

    elif args.stop != None:
        assert args.stop[0] in config["ids"], "ID not in container config file"
        DockerAutomation.stop_container(args.stop[0], client)
    elif args.list == True:
        DockerAutomation.list_container(client)
