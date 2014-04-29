#LRI-B

##DESCRIPTION
LRI-B is a backend that stores learning resources and educational standards from the Learning Registry.

##SYSTEM REQUIREMENTS
LRI-B has been built and tested on Ubuntu 12.04 LTS. You'll need JDK 7 installed, a great set of instructions for installing Oracle's JDK can be found at [Web Upd8](http://www.webupd8.org/2012/01/install-oracle-java-jdk-7-in-ubuntu-via.html to install JDK 7 "JDK 7 Install Instructions")

##INSTALLATION
Starting from a fresh install of Ubuntu 12.04 LTS with JDK 7 installed:

	sudo apt-get update
	sudo apt-get install memcached python-dev python-memcache build-essential sqlite3-doc uwsgi-plugins-all uwsgi-extra uwsgi unzip python-pip python-yaml nginx
	pip install py2neo==1.4.5
	pip install web.py

Unzip the LRI-B package and move to /opt.

Make sure the directory is accessible by nginx.
Customize the following files to reflect your installation:

- /opt/lri-b/wsgi_config.json: Fix the paths for "wsgi-file" and "pyargv"


##CONTRIBUTE
Interested in helping to improve the ? Great! You can take look at the backlog on our [Jira issue tracker](https://support.inbloom.org "Jira"). Browse existing issues, or contribute your own ideas for improvement and new features.

Looking to interact with other developers interested in changing the future of education? Check out our [community forums](https://forums.inbloom.org/ "Forums"), and join the conversation!

##LICENSING
LRI-B is licensed under the Apache License, Version 2.0. See LICENSE-2.0.txt for full license text.