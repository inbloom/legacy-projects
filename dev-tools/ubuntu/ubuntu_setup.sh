#!/bin/bash

MODE="screen"
WORKING_DIR=$(pwd)
INSTALL_ROOT="${HOME}/Projects/"


bashexec () 
{
	# Create a temporary file
	TMPFILE=$(mktemp)

	# Add stuff to the temporary file
	echo "source ~/.bashrc" > $TMPFILE
	echo "$1" >> $TMPFILE
	echo "rm -f $TMPFILE" >> $TMPFILE

	# Start the new bash shell 
	bash --rcfile $TMPFILE
}

start_inmemory_ldap ()
{
    echo "start start_inmemory_ldap"
    #start start_inmemory_ldap
    cd $IN_MEMORY_LDAP_ROOT
    if [ $MODE = "screen" ]
    then
        screen -S ldap-in-memory -d -m mvn jetty:run
    elif [ $MODE = "tabbed" -o $MODE = "command" ]
    then
		bashexec "mvn jetty:run"
    fi
}

start_ingestion ()
{
    echo "start ingestion"
    #start ingestion service
    cd $SLI_ROOT/ingestion/ingestion-service
    if [ $MODE = "screen" ]
    then
        screen -S ingestion-service -d -m mvn jetty:run
    elif [ $MODE = "tabbed" -o $MODE = "command" ]
    then
        bashexec "mvn jetty:run"
    fi
}

start_api ()
{
    #start api
    cp $SLI_ROOT/data-access/dal/keyStore/trustey.jks /tmp
    cd $SLI_ROOT/api
    if [ $MODE = "screen" ]
    then
        screen -S api -d -m mvn jetty:run
    elif [ $MODE = "tabbed" -o $MODE = "command" ]
    then
        bashexec "mvn jetty:run"
    fi
}

start_simple_idp ()
{
    #start simple-idp
    cd $SLI_ROOT/simple-idp
    if [ $MODE = "screen" ]
    then
        screen -S simple-idp -d -m mvn jetty:run
    elif [ $MODE = "tabbed" -o $MODE = "command" ]
    then
        bashexec "mvn jetty:run"
    fi
}

start_search_indexer ()
{
    #start search indexer
    cd $SLI_ROOT/search-indexer
    if [ $MODE = "screen" ]
    then
        screen -S search-indexer -d -m ./scripts/local_search_indexer.sh start
        screen -S search-indexer-tail -d -m tail -f logs/search-indexer.log
    elif [ $MODE = "tabbed" -o $MODE = "command" ]
    then    
        #./scripts/local_search_indexer.sh start
        bashexec "./scripts/local_search_indexer.sh start && tail -f logs/search-indexer.log"
    fi
}

start_dashboard ()
{
    #start dashboard
    cd $SLI_ROOT/dashboard
    if [ $MODE = "screen" ]
    then
        screen -S dashboard -d -m mvn jetty:run
    elif [ $MODE = "tabbed" -o $MODE = "command" ]
    then
        bashexec "mvn jetty:run"
    fi
}

start_admin_tools ()
{
    #start admin tools
    cd $SLI_ROOT/admin-tools/admin-rails
    #bundle install
    if [ $MODE = "screen" ]
    then
        screen -S admin-rails -d -m bundle exec rails server
    elif [ $MODE = "tabbed" -o $MODE = "command" ]
    then
		bashexec "bundle exec rails server"
    fi
}

start_data_browser ()
{
    #start data browser
    cd $SLI_ROOT/databrowser
    #bundle install
    if [ $MODE = "screen" ]
    then
        screen -S databrowser -d -m bundle exec rails server
    elif [ $MODE = "tabbed" -o $MODE = "command" ]
    then
        bashexec "bundle exec rails server"
    fi
}

list ()
{
    screen -list
}

startall ()
{
    echo "startall"
    if [ $MODE = "screen" ]
    then
        echo "Starting components in screen mode"
        start_inmemory_ldap
        start_ingestion
        start_api
        start_simple_idp
        #start_search_indexer
        start_dashboard
        start_admin_tools
        start_data_browser
		
		echo "Applications started in the following active screen sessions: "
		list
    elif [ $MODE = "tabbed" ]
    then
        echo "starting in tabbed mode"
        exec gnome-terminal --tab --title "ingestion" -e "bash -c \"$WORKING_DIR/ubuntu_setup.sh -c start_ingestion\"" --tab-with-profile=Default --title="api" -e "bash -c \"$WORKING_DIR/ubuntu_setup.sh -c start_api\"" --tab-with-profile=Default --title="simple idp" -e "bash -c \"$WORKING_DIR/ubuntu_setup.sh -c start_simple_idp\"" --tab-with-profile=Default --title="search indexer" -e "bash -c \"$WORKING_DIR/ubuntu_setup.sh -c start_search_indexer\"" --tab-with-profile=Default --title="dashboard" -e "bash -c \"$WORKING_DIR/ubuntu_setup.sh -c start_dashboard\"" --tab-with-profile=Default --title="admin tools" -e "bash -c \"$WORKING_DIR/ubuntu_setup.sh -c start_admin_tools\"" --tab-with-profile=Default --title="data_browser" -e "bash -c \"$WORKING_DIR/ubuntu_setup.sh -c start_data_browser\"" 
    fi
    
}

realmInit ()
{
    cd $SLI_ROOT/acceptance-tests
    bundle install
    bundle exec rake realmInit
}

importSandboxData ()
{
    cd $SLI_ROOT/acceptance-tests
    bundle install
    bundle exec rake importSandboxData
}

ingestSmallSampleDataset ()
{
	echo "Ingesting data to tenant $1"
    cd $SLI_ROOT/ingestion/ingestion-service/target/ingestion/lz/inbound/$1
    cp $SLI_ROOT/acceptance-tests/test/features/ingestion/test_data/SmallSampleDataSet.zip ./
    ruby $SLI_ROOT/opstools/ingestion_trigger/publish_file_uploaded.rb STOR $(pwd)/SmallSampleDataSet.zip
}

resetDatabase ()
{
    cd $SLI_ROOT/config/scripts
    sudo bundle install
    ./resetAllDbs.sh
}

build_sli () 
{
    cd "${INSTALL_ROOT}secure-data-service/build-tools"
    mvn clean install
	
    cd $SLI_ROOT
    mvn clean install -DskipTests -Dsli.env=local-ldap-server #build to use local in-memory ldap
	
    #build admin-rails app
    cd $SLI_ROOT/admin-tools/admin-rails
    bundle install
    
    
    #build databrowser rails app
    cd $SLI_ROOT/databrowser
    bundle install
    
	
}

setup ()
{
	echo -e "BEGIN INSTALL\n\n\n"
	
	if [[ $EUID = 0 ]]; then
	   echo -e "DANGER DANGER DANGER!!\nRunning this script as root is a bad idea. Run as a normal user and let sudo work its magic." 
	   exit 1
	fi
	
    #setup additional apt repositories
    echo "Configuring oracle-java apt repo"
    if [ ! `which add-apt-repository` ]
    then
    sudo apt-get update
    echo "installing python-software-properties"
    sudo apt-get -y install python-software-properties
    sudo apt-get update
    echo "Python software properties installed"
    else
    echo "add-apt-repository exists and is in path.  Skipping install"
    fi
    sudo add-apt-repository -y ppa:webupd8team/java
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
    
    #config mongodb sources for correct version
    echo "Configure mongodb apt repo"
    echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
    
    #refresh packages
    sudo apt-get update
    
    packagelist=( "openssh-server" "curl" "git" "screen" "build-essential" "zip" "libxml2-dev" "libxslt1-dev" "libssl-dev" "zlib1g-dev" "libgdbm-dev" "libncurses5-dev" "automake" "libtool bison" "libffi-dev" "python-software-properties" "oracle-java7-installer" "mongodb-10gen=2.2.6" "maven")
    
    for i in "${packagelist[@]}"
    do
        echo "Installing package $i"
        sudo apt-get -y install $i
        
        res=$? 
        if [ $res -ne 0 ] #test to make sure the package installed correctly before proceeding to the next
        then
            echo "apt-get returned a code of $res"
            echo "Failed to install package \"$res\", aborting installation!"
            exit 1
        fi
    done

    #prevent mongodb from updating to latest version in the future
    echo "mongodb-10gen hold" | sudo dpkg --set-selections
     
    # is the next step needed with sufficient disk?
    #uncomment nojournal in /etc/mongodb.conf
    
	#install ruby
	echo "Installing RVM and Ruby"
	curl -L https://get.rvm.io | bash -s stable
	source $HOME/.rvm/scripts/rvm
	echo "source ${HOME}/.rvm/scripts/rvm" >> $HOME/.bashrc
	rvm install 2.0.0
	rvm use 2.0.0 --default
	ruby -v
	
	echo "gem: --no-ri --no-rdoc" > $HOME/.gemrc
	
    sudo gem install bundler
    # install activemq
	echo "Install activemq"	
	mkdir $HOME/tmp
	cd $HOME/tmp
	curl -O http://archive.apache.org/dist/activemq/apache-activemq/5.8.0/apache-activemq-5.8.0-bin.tar.gz
	tar xvzf apache-activemq*.tar.gz -C /tmp/
	sudo su -c "mv /tmp/apache-activemq* /opt/"
	sudo ln -sf /opt/apache-activemq-5.8.0/ /opt/activemq
	sudo adduser -system activemq
	sudo chown -R activemq: /opt/apache-activemq-5.8.0
	sudo ln -sf /opt/activemq/bin/activemq /etc/init.d/
	sudo update-rc.d activemq defaults	
	rm -rf $HOME/tmp
	
    #sudo service activemq stop
    
    #check to see if we've already added stomp config to activemq
    if ! $(grep -q stomp /opt/activemq/conf/activemq.xml)
    then
        echo "Adding stomp config to activemq.xml"
        sudo perl -pi -e "s~</transportConnectors>~<transportConnector name=\"stomp\" uri=\"stomp://0\.0\.0\.0\:61613?maximumConnections=1000&amp;wireformat.maxFrameSize=104857600\"/>\n</transportConnectors>~g" /opt/activemq/conf/activemq.xml
        # Stomp must be activated by adding <transportConnector name="stomp" uri="stomp://0.0.0.0:61613"/>to the conf/activemq.xml file in the <transportConnectors> block
	else
        echo "Stomp config already added to activemq.xml. Skipping."
    fi
    sudo ln -s /opt/activemq/instances-available/main /opt/activemq/instances-enabled/main # still needed?
	sudo service activemq stop
    sudo service activemq start
    
    # OpenADK 
    mkdir "$INSTALL_ROOT"
    cd "$INSTALL_ROOT"
    git clone https://github.com/open-adk/OpenADK-java.git
    cd OpenADK-java/adk-generator
    ant clean US
    cd ../adk-library
    # Change the ADK-library pom.xml line #7 from 1.0.0-snapshot to: 1.0.0 - This is due to the fact that the project dependency does not have SNAPSHOT in the version.
    perl -pi -e 's/1.0.0-SNAPSHOT/1.0.0/g' ./pom.xml
    mvn -P US install
    
    cd $INSTALL_ROOT
    git clone https://github.com/inbloom/secure-data-service.git
    
    cd $INSTALL_ROOT
    git clone https://github.com/inbloom/ldap-in-memory.git

    #set env variables for future
    echo 'export MAVEN_OPTS="-Xmx2g -XX:+CMSClassUnloadingEnabled -XX:PermSize=128M -XX:MaxPermSize=512M"' >> ~/.bashrc
    echo "export SLI_ROOT=${INSTALL_ROOT}secure-data-service/sli" >> ~/.bashrc
    echo "export IN_MEMORY_LDAP_ROOT=${INSTALL_ROOT}ldap-in-memory" >> ~/.bashrc

    source $HOME/.bashrc

    #need to export env variables for now
    export MAVEN_OPTS="-Xmx2g -XX:+CMSClassUnloadingEnabled -XX:PermSize=128M -XX:MaxPermSize=512M"
    export SLI_ROOT="${INSTALL_ROOT}secure-data-service/sli"
    export IN_MEMORY_LDAP_ROOT="${INSTALL_ROOT}ldap-in-memory"
       

    #kick off maven builds and bundle ruby tools
    build_sli
    
    #start mongodb
    sudo service mongodb start
    
	resetDatabase
    
    cp $SLI_ROOT/data-access/dal/keyStore/trustey.jks /tmp
    
    start_inmemory_ldap
    start_ingestion
    start_api
    start_simple_idp
    #start_search_indexer
	start_admin_tools
	start_data_browser
	start_dashboard
    
    #ingest sample data set
	realmInit
	importSandboxData
      
    echo -e "\n\nInstallation complete!!!" 
}

stopall ()
{
    #stop ingestion service
    echo "Stopping ingestion-service"
    screen -S ingestion-service -p 0 -X stuff $'\003'
    
    #stop api
    echo "Stopping api"
    screen -S api -p 0 -X stuff $'\003'
    
    #stop simple-idp
    echo "Stopping simple-idp"
    screen -S simple-idp -p 0 -X stuff $'\003'
    
    #stop search indexer
    #echo "Stopping search indexer"
    #cd $SLI_ROOT/search-indexer
    #screen -S search-indexer -d -m ./scripts/local_search_indexer.sh stop
    #screen -S search-indexer-tail -p 0 -X kill

    echo "Stopping sample ingestion log"    
    screen -S sample-ingestion-tail -p 0 -X kill
    
    #stop dashboard
    echo "Stopping dashboard"
    screen -S dashboard -p 0 -X stuff $'\003'
    
    #stop admin tools
    echo "Stopping admin tools"
    screen -S admin-rails -p 0 -X stuff $'\003'
    
    #stop data browser
    echo "Stopping data browser"
    screen -S databrowser -p 0 -X stuff $'\003'

    #stop datastore_ldap_inmemory
    echo "Stopping ldap-in-memory"
    screen -S ldap-in-memory -p 0 -X stuff $'\003'
}


if [ -z "$SLI_ROOT" ]
then
   export SLI_ROOT=${INSTALL_ROOT}secure-data-service/sli 
fi
if [ -z "$MAVEN_OPTS" ]
then
   export MAVEN_OPTS="-Xmx2g -XX:+CMSClassUnloadingEnabled -XX:PermSize=128M -XX:MaxPermSize=512M"
fi

while getopts ":tc:" opt; do
    case $opt in
        t)
            MODE="tabbed"
            echo "tabbed mode!" >&2
            
            ;;
        c)
            #command mode: execute the passed in function and bypass normal argument processing 
            MODE="command"
            echo "command: $OPTARG" >&2
            ${OPTARG}
            
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            
            ;;
    esac
done
shift $((OPTIND-1))

if [ $MODE != "command" ]
then
    if [ "$1" = "install" ]
    then
		echo -e "\n\n==========================================================\nBeginning install, writing output to installation.log\n=========================================================="
        setup | tee installation.log
    elif [ "$1" = "start" ]
    then
        startall
    elif [ "$1" = "stop" ]
    then
        stopall
    elif [ "$1" = "list" ]
    then
        list
    elif [ "$1" = "resetdb" ]
    then
        resetDatabase
	elif [ "$1" = "realminit" ]
	then
		realmInit
	elif [ "$1" = "ingestdata" ]
	then
		if [ ! -z "$2" ]
		then
			ingestSmallSampleDataset $2
		else
			ingestSmallSampleDataset Midgar-DAYBREAK
		fi
		
	elif [ "$1" = "importdata" ]
	then
		importSandboxData
	elif [ "$1" = "loaddata" ]
	then
		loadData
	elif [ "$1" = "build" ]
	then
		build_sli
    else
        echo "Valid parameters for this script are:"
        echo "    install : Performs initial installation and configuration of software"
        echo "    start : Start all components of the application"
        echo "    stop : Stop all components of the application"
        echo "    resetdb : Reset the database"
		echo "    realminit : Initialize realms"
		echo "    ingestdata : Load the small sample dataset via ingestion"
		echo "    importdata : Load the small sample dataset sandbox data via import"
		echo "    build : Run maven build and bundle rails apps"
        echo "    list : List all active screen sessions"
    fi
fi
