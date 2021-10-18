# kitchen

## NP Laboratory 1

### RUN

$ # clone repository <br />
$ pip install -r imports.txt <br />
$ py main.py <br />

### with docker

$ docker build -t dining . # create kitchen image <br />
$ docker run -d --net pr_lab1 --name kitchen kitchen # run docker container on created network <br />
