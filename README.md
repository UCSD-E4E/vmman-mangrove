# vmman

```
__   ___ __ ___  _ __ ___   __ _ _ __  
\ \ / / '_ ' _ \| '_ ' _ \ / _' | '_ \ 
 \ V /| | | | | | | | | | | (_| | | | |
  \_/ |_| |_| |_|_| |_| |_|\__,_|_| |_|
                                         
```
**vmman** is a tool to quickly boot and view docker-based VMs running on a linux server through noVNC without ssh tunneling on another network.

## Usage

```
usage: vmman [-h] [-start START] [-stop STOP] [-list]

Start given docker containers, and give url for novnc.

optional arguments:
  -h, --help    show this help message and exit
  -start START  Starts the given docker container and gives url for novnc
  -stop STOP    Stops the given docker container
  -list         Lists all docker VMs and their current state
```

### Starting vm
```
#Starts container with # 0
vmman -start 0
```

If run correctly, you will then get something like this output

```
Starting Docker container 0 with ID 31602fa90aa9, getting VNC URL
NOTE: This url will only last for the current session, do not save this url or use it after you have stopped your container
URL for VNC access is: https://23........
```

If you click on the link, you should then be able to view the vm from your browser. 

![screenshot](https://user-images.githubusercontent.com/33649660/143733333-cd2eddd7-2260-4c02-95b7-5f7810f9dffd.png)



### Stopping vm
```
#Stops container with # 0
vmman -stop 0
```

### Listing all vms
```
#Lists containers
vmman -list
```


## Installation

Before using vmman, a proper installation of [docker](https://docs.docker.com/engine/install/ubuntu/) is required on the host linux machine. In addition, [Python 3 and pip3](https://www.python.org/downloads/) are required. These should be installed by default on your server, but they can be installed below with the following:

```
sudo apt install -y python3
sudo apt install -y python3-pip
```


Once docker is installed, you can create new docker containers for the image provided. Use this [docker image](https://hub.docker.com/repository/docker/dillhix/mangrove), it has noVNC and Anaconda ready for ML remote development. You can load and start a new docker container with:

```
sudo docker run -p 6080:80 -v /dev/shm:/dev/shm dillhix/mangrove:0.5
```

Do this for how many containers you want to be able to connect to, changing the port for each container (6080 to 6081, etc). 

Once the docker containers are setup, we can now get the id's with:

```
sudo docker ps -all
```

The output should look like this:

```
CONTAINER ID   IMAGE                  COMMAND         CREATED       STATUS                      PORTS     NAMES
31602fa90aa9   dillhix/mangrove:0.3   "/startup.sh"   5 hours ago   Exited (0) 33 minutes ago             kind_kepler
```


Next, copy over the container ID's of the containers that you want into the `container_ids.cfg` file with whatever # identifier you want that container to have. We do this step and manually get the IDs so we don't have the ability to start and stop containers that are not vm's for general use servers. This is useful for our server in particular because we will have web hosting and general usage ML training. 

The resulting config file should then look like this 


```
[ids]
#Don't worry about this - this isn't a key, just the id for reference
0 = 31602fa90aa9 
1 = .....
```

Now, with everything installed, we can install vmman by going into the same directory as `container_ids.cfg` and `vmman.py`, and type:

```
sudo bash install.sh
```

We can then use vmman anywhere in the server.
