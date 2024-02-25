aarg_upscale is a Python command-line wrapper designed to upscale video files based on [k4yt3x/video2x](https://github.com/k4yt3x/video2x).

## Features

- Easy to use wrapper for video2x.
- Option to keep the original files after upscaling.
- Process an entire directory of video files or a single file.

## Prerequisites

- Docker installed and running on your system.
- Sudo privileges for running Docker commands.
- Python 3.6 or newer.

## Installation

### Ubuntu / Nvidia
1. If not installed already, install docker on ubuntu following the [official docs](https://docs.docker.com/engine/install/ubuntu/).
   * Check installation with ```sudo docker run hello-world```
2. Install nvidia container toolkit using the [official guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html). This allows gpu acceleration inside of the docker container.
3. Pull latest docker image (see releases [here](https://github.com/k4yt3x/video2x/pkgs/container/video2x)).
    * At the time of writing ```docker pull ghcr.io/k4yt3x/video2x:5.0.0-beta6```

### Other OS / GPUs
To be added later, as of now not supported. May be possible to do any combination of [MacOS|Windows|Arch] OS and [AMD|Intel|Nvidia] GPU.
