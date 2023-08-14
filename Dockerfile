FROM nvidia/cuda:11.8.0-base-ubuntu22.04

RUN apt-get update

# Install Python 3.8
RUN apt-get install -y \
    python3 \
    python3-dev \
    python3-pip

# Install PyTorch 1.13
RUN pip3 install torch==1.13.0+cu116 torchvision==0.14.0+cu116 torchaudio==0.13.0 --extra-index-url https://download.pytorch.org/whl/cu116


# Copy  and install other requirements
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app
COPY requirements.txt /app
COPY *.py /app/
COPY models /app/models
RUN pip3 install -r ./requirements.txt
RUN apt-get install ffmpeg libsm6 libxext6  -y


# final configuration
CMD python3 inference.py


