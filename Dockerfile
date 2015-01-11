FROM base/archlinux:latest

MAINTAINER Elijah Caine McDade-Voigt

ENV APP_IP 0.0.0.0

# Update Arch
RUN pacman -Syyuu --noconfirm
RUN pacman-db-upgrade

# Install system dependencies
RUN pacman --noconfirm -S python python-pip gcc

# Install python requirements
WORKDIR /huRandom
COPY ./requirements.txt /huRandom/requirements.txt

RUN pip install -r requirements.txt

# Copy the version of the app in the host's current directory into the
# container
COPY . /huRandom

# Command to run
CMD ["python", "huRandom/huRandom.py"]
