FROM base/archlinux:latest

MAINTAINER Elijah Caine McDade-Voigt, elijahcainemv@gmail

ENV APP_IP 0.0.0.0

# Update Arch
RUN pacman -Syyuu --noconfirm
RUN pacman-db-upgrade

# Install system dependencies
RUN pacman --noconfirm -S python2 python2-pip python2-setuptools gcc sqlite

# Set environment variables
RUN cp /huRandom/huRandom/config.py.dist /huRandom/huRandom/config.py
ENV HURANDOM_SETTINGS=/huRandom/huRandom/config.py

# Install python requirements
WORKDIR /huRandom
COPY ./requirements.txt /huRandom/requirements.txt

RUN pip2.7 install -r requirements.txt

# Copy the version of the app in the host's current directory into the
# container
COPY . /huRandom
RUN ln /usr/bin/python2.7 /usr/bin/python

# Initialize database
RUN python /huRandom/huRandom/init.py

# Command to run
CMD ["python", "huRandom/huRandom.py"]
