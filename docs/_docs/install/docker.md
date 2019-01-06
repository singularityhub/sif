---
title: SIF Python in Docker
category: Installation
order: 2
---

To use the Docker container, you should first ensure that you have
 [installed Docker](https://www.docker.com/get-started) on your computer.

For the container we will use, we currently provide a container hosted 
at [singularityhub/sif](http://hub.docker.com/r/singularityhub/sif) that you can use to 
quickly run deid without any installation of other dependencies
or compiling on your host. 

When you are ready, try running {{ site.title }} using it. This first command will
shell you inside the container to use python interactively:

```bash
$ docker run {{ site.docker }}

SIF Python v0.0.11
usage: sif [-h] [--debug] [--quiet] [--version] {shell} ...

SIF Python

optional arguments:
  -h, --help  show this help message and exit
  --debug     use verbose logging to debug.
  --quiet     show SIF Python verison and exit
  --version   suppress additional output.

actions:
  actions for SIF Python

  {shell}     sif python actions
    shell     shell into a session a client.
```

It might also be desired to shell into the container (bash)

```bash
$ docker run -it --entrypoint bash {{ site.docker }} 
bash-4.4#
```

To get the interactive shell for your container, you need to bind it as a volume.

```bash
$ docker run -it --volume $PWD:/data singularityhub/sif shell /data/boxes.simg
```

You can also go right into Python:

```bash
$ docker run -it --entrypoint ipython singularityhub/sif
```
