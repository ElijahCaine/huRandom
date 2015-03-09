HuRandom
========
*A project about 'random' numbers*

![Main Page Preview Screenshot](http://share.elijahcaine.me/hurandom_main.png)

Installation
------------
HuRandom is developed and tested on Arch Linux with `python --version` 3.4.2 or
2.7.9, and `flask.__version__` 0.10.1. Your mileage may vary.

Status
------
Fully functional! Live at http://hurandom.elijahcaine.me

Development [with Docker]
-------------------------
First edit the config file
```shell
$ cp huRandom/config.py.dist huRandom/config.py
$ <text-editor> huRandom/config.py
$ Edit config settings appropriately
```

To build an image, run:
```shell
$ docker build -t elijahcaine/hurandom .
```

To run the container, use:
```shell
$ docker run -p 5000:5000 elijahcaine/hurandom
```

To develop in the container:
```shell
$ docker run -i -t elijahcaine/hurandom /bin/bash
```

Development [without Docker]
----------------------------
To develop without Docker run:
```shell
$ cp huRandom/config.py.dist huRandom/config.py
$ <text-editor> huRandom/config.py  # create and edit the config file
Edit config settings appropriately
$ export HURANDOM_SETTINGS=huRandom/config.py # add settings to your env
$ virtualenv huRandom               # create a python virtualenv
$ soruce huRandom/bin/activate      # source the virtualenv 
$ pip install -r requirements.txt   # install python pacakges
$ python huRandom/init.py           # sets up database
$ python huRandom/huRandom.py       # run the application!
```

You may also need to install sqlite3 and/or python3.

Goals
-----
1. To study the relationship between people and randomness through crowdsourced
information e.g., 'Please think of a random number and enter it in the text box
below.'
2. To share this information with users with easily accessible data.
3. To learn

More Information
----------------
If you would like to know more about the project or contact the author of
HuRandom ping pop on irc.freenode.net or email elijahcainemv@gmail.

HuRandom is licenced under the MIT Licence (MIT)
Copyright © 2015 Elijah Caine McDade-Voigt

Contributors
------------
Elijah Caine
Ian Kronquist
