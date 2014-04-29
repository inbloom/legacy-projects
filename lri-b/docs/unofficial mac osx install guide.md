# Development Installation Instructions (using OS X Mountain Lion)

This document is an amalgamation of the AMI SLC LRI Administrator Guide and the steps required to install on a development box that is not prepared for the lri-b environment.  This setup is assuming a factory installation of OS X Mountain Lion on a Mac system.  Your milage may vary.  Please feel free to update doc, or send update requests with any changes you find are necessary to get the LRI-b running for local development.

You will need the [Command Line Tools for XCode](https://developer.apple.com/downloads/index.action#) if you are using a Mac.

This is a bare minimum guide, and at this time does not include memcached support.

## Neo4j

Download Neo4j Stable Release 1.9 from: [http://www.neo4j.org/download](http://www.neo4j.org/download)

Untar it into a location of your choosing we'll call `$DBDIR`

## Setup lri-b

Create a new directory for the lri-b to live.  We'll refer to this place as `$LIRDIR`

Place the lri-b source into the `$LIRDIR`

### Configure lri-b
  
Update the `lri_config.json` file as follows:

    {
        "host":"127.0.0.1",
        "port":8888,
        "neo4j_dir":"$DBDIR",
        "neo4j_server_host":"127.0.0.1",
        "neo4j_server_port":7474,
        "slc_server_host":"api.sandbox.slcedu.org",
        "slc_token_check_path":"/api/rest/system/session/check",
        "bootstrap_filenames":[
            "$LIRDIR/lri_schema/bootstrap.json",
            "$LIRDIR/lri_schema/cc_schema.json",
            "$LIRDIR/lri_schema/schema.org_fixed.json",
            "$LIRDIR/lri_schema/lrmi_fixed.json"
        ],
        "default_creator_guid":"LRI_TEST_CREATOR",
        "admin_passwd":"changeme",
        "use_cache":true,
        "admin_access_tokens":{
            "regtest":"regtest",
            "letmein":"LRI_ADMIN_USER_0"
        },
        "delegate_tokens":[
            "DELEGATE_0"
        ]
    }

IMPORTANT: Change `$DBDIR` to your neo4j path.  Also, configure passwords, etc as needed.

### Setup Java

If you have java, great, if not, stop and [get it here](http://support.apple.com/kb/dl1572).  You'll need it installed for the lri-b to run.

Now setup `java_home` fun.

    export JAVA_HOME=$(/usr/libexec/java_home)

## Python

Factory installation of Mountain Lion included Python 2.7.2.  You will need 2.7.x to make this work.

### Install PIP

Install `pip` (A tool for installing and managing Python packages).  We'll need this to install python dependencies

    sudo easy_install -U pip

#### Use pip to install dependencies

    sudo pip install pyyaml
    sudo pip install httplib2
    sudo pip install neo4j-embedded
    sudo pip install py2neo==1.4.6
    sudo pip install pyweb
    sudo pip install web.py

## Install nginx

First, create a place for all the source code files (if you don't already have a place like this), then change to that directory.

    mkdir -p /usr/local/src
    cd /usr/local/src

Now, download the nginx and its dependencies.  If you don't have wget, you can [install it](http://osxdaily.com/2012/05/22/install-wget-mac-os-x/), or just use your browser.

    wget 'http://download.icu-project.org/files/icu4c/49.1.2/icu4c-49_1_2-src.tgz'
    wget 'http://nginx.org/download/nginx-1.2.2.tar.gz'
    wget 'http://ftp.cs.stanford.edu/pub/exim/pcre/pcre-8.31.tar.gz'
    
Untar them

    tar xfz pcre-8.31.tar.gz
    tar xfz icu4c-49_1_2-src.tgz
    tar xfz nginx-1.2.2.tar.gz
    
Start by installing pcre

    cd /usr/local/src/pcre-8.31
    ./configure --enable-unicode-properties --enable-utf8
    make
    sudo make install
    cd ..
    rm -rf pcre-8.31

ICU is next

    cd /usr/local/src/icu
    sh source/configure --prefix=/usr/local
    gnumake
    sudo make install
    cd ..
    rm -rf icu
    
Finally nginx

    cd /usr/local/src/nginx
    ./configure --sbin-path=/usr/local/sbin/nginx --conf-path=/usr/local/nginx/nginx.conf --with-http_ssl_module --with-pcre=../pcre-8.31
    make
    sudo make install
    cd ..
    rm -rf nginx

### Configure nginx

Open `/usr/local/nginx/nginx.conf` in a text editor and modify to look like this:

    worker_processes  1;

    events {
      worker_connections  1024;
    }


    http {
      include       mime.types;
      default_type  application/octet-stream;

      sendfile        on;

      keepalive_timeout  65;

      server {
        listen 8000;
        server_name 127.0.0.1;
        location / {
          include uwsgi_params;
          uwsgi_pass unix:/tmp/wsgi.sock;
          uwsgi_param UWSGI_CHDIR $LIRDIR;
          uwsgi_param UWSGI_SCRIPT webapp;
        }
      }
    }

IMPORTANT: Change `$LIRDIR` to your lri-b path.

### nginx Basics

To start:

    sudo /usr/local/sbin/nginx
  
To stop:

    /usr/local/sbin/nginx -s stop
    
To reload:

    /usr/local/sbin/nginx -s reload
  
## Install JPype

Download [JPype-0.5.4.2.zip](http://sourceforge.net/projects/jpype/files/JPype/0.5.4/JPype-0.5.4.2.zip/downloads) via your browser.

    cd /usr/local/src/
    unzip ~/Downloads/JPype-0.5.4.2.zip
    cd JPype-0.5.4.2/
    
NOTE: If you are running Mac OS X Mountain Lion, you'll probably have issues with your JPype install.  Maybe others OSes/distros have this problem also. These instructions, from [this blog post](http://blog.y3xz.com/blog/2011/04/29/installing-jpype-on-mac-os-x/) work for Mountain Lion, other updates may be needed for your specific OS.

Open `setup.py` in your favorite text editor.

In function `setupMacOSX()`, set:

    self.javaHome = '/Developer/SDKs/MacOSX10.6.sdk/System/Library/Frameworks/JavaVM.framework/Versions/1.6.0/'

and:

    self.libraryDir = [self.javaHome + "/Libraries"]

In function `setupInclusion()`, set:

    self.javaHome + "/Headers",

and:

    self.javaHome + "/Headers/" + self.jdkInclude,

Here is a [gist of a completed setup.py](https://gist.github.com/JDStraughan/5669988) for OS X Mountain Lion

Continuing on with the installation:

    sudo python setup.py install
    cd ..
    sudo rm -rf JPype-0.5.4.2
  
## Install Jansson

    cd /usr/local/src/
    
    wget http://www.digip.org/jansson/releases/jansson-2.4.tar.gz
    tar xvf jansson-2.4.tar.gz 
    
    cd /usr/local/src/jansson-2.4
    ./configure
    make
    sudo make install  
  
## Install uWSGI

    sudo pip install uwsgi

### Configure uWSGI

Open `$LRI_DIR` and update `wsgi_config.json` to look something like this:
IMPORTANT: Change `$LIRDIR` to your lri-b path.

    {
      "uwsgi": {
        "gid":"www-data",
        "uid":"www-data", 
        "enable-logging":true, 
        "socket":"/tmp/wsgi.sock", 
        "chmod-socket":666,
        "protocol":"wsgi",
        "buffer-size":25000, 
        "wsgi-file":"$LIRDIR/webapp.py", 
        "pyargv":"$LIRDIR/lri_config.json",
        "plugins":["python","http"],
          "processes":1,
          "master":true,
          "harakiri":60,
          "limit-as":1024,
          "memory-report":true,
          "no-orphans":true
      } 
    }

### Inbloom Index Setup

This is almost verbatim from the Administrator Guide.  You can pick up on step 4 of page 6 or just keep following along.

Move to your `$LRIDIR`

    cd $LRIDIR

Init neo4j

    python lri_admin.py init_neo4j
    
Start neo4j

    python lri_admin.py start_neo4j
    
Check that neo4j is running by opening a browser window to [http://localhost:7474/webadmin/](http://localhost:7474/webadmin/)

Initialize the LRI server by loading the bootstrap schemata:

    python lri_admin.py create_lri
  
This could take a while to run.  Don't be surprised if it runs for several minutes to an hour.

    python lri_admin.py start_lri
    
This should start the server.  If you get web.py errors, there is probably a fix.  If you find it - put it here.