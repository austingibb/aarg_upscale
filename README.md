The aarg_upscale repo hosts a Python command-line wrapper designed to upscale video files based on [k4yt3x/video2x](https://github.com/k4yt3x/video2x).

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

## Usage

Upscale all .avi files in a directory to 1080p and convert them to .mp4, keeping the original files:
```
aarg_upscale -d some/directory -t 1080 -i .avi -o .mp4 -k
```

Upscale a single video file to 720p and convert it to .mp4, removing the original file:
```
aarg_upscale -p some/directory/video.avi -t 720 -o .mp4
```

## License
MIT License

Copyright (c) 2024 Austin Gibbons

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
