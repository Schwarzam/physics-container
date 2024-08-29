## Physics container

#### This is a container implementation to run nbody and corrfunc in a docker container 

### Building the container

First of all you need to install docker in your machine. You can follow the instructions in the official docker website. 

Follow the steps in this [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/) to install docker in your machine.

After installing docker, you can build the docker image by running the following command in the terminal. 

** Note ** If you want to install additional python packages just add them to the additional_packages.txt and run the build command. 

```bash
sudo docker build -f Dockerfile.dev -t physicscont .
```

After building the image, you can run the container by running the following command in the terminal. 

### Running the container

**It's important** to understand that the container has its own storage space and it's isolated from the host machine. You can mount the host machine's directory to the container by using the `-v` flag. 

Below are some examples of how to run the container. Please adapt the commands to your needs and also the paths to your files. 

The following command mounts the current directory to the container and opens a bash shell. 

```bash
sudo docker run -it --rm -v ./:/src physicscont /bin/bash 
```

The following command mounts the current directory to the container and runs the test.py file. 

```bash
sudo docker run -it --rm -v ./:/src/ physicscont python /src/test.py
```

The following command mounts the current directory to the container and runs a jupyter notebook. Then you may access it with the IP of the server/machine you are running it in: http://{MACHINE_IP}:8888 and then just paste the token showed on the server terminal. 

```bash
sudo docker run -it --rm -v ./:/src/ -p 8888:8888 physicscont python3 -m notebook --allow-root --ip=0.0.0.0 --port=8888 --allow-root --no-browser
```

