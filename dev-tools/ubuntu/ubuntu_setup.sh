#!/bin/bash

MODE="screen"
WORKING_DIR=$(pwd)

start_inmemory_ldap ()
{
    echo "start start_inmemory_ldap"
    #start start_inmemory_ldap
    cd $IN_MEMORY_LDAP_ROOT
    if [ $MODE = "screen" ]
    then
        screen -S datastore_ldap_inmemory -d -m mvn jetty:run
    elif [ $MODE = "tabbed" -o $MODE = "command" ]
    then
        bash --rcfile <(echo "mvn jetty:run")
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
        bash --rcfile <(echo "mvn jetty:run")
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
        bash --rcfile <(echo "mvn jetty:run")
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
        bash --rcfile <(echo "mvn jetty:run")
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
        bash --rcfile <(echo "./scripts/local_search_indexer.sh start && tail -f logs/search-indexer.log")
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
        bash --rcfile <(echo "mvn jetty:run")
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
        bash --rcfile <(echo "bundle exec rails server")
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
        bash --rcfile <(echo "bundle exec rails server")
    fi
}

startall ()
{
    echo "startall"
    if [ $MODE = "screen" ]
    then
        echo "starting normally"
        start_inmemory_ldap
        start_ingestion
        start_api
        start_simple_idp
        start_search_indexer
        start_dashboard
        start_admin_tools
        start_data_browser
    elif [ $MODE = "tabbed" ]
    then
        echo "starting in tabbed mode"
        exec gnome-terminal --tab --title "ingestion" -e "bash -c \"$WORKING_DIR/ubuntu_setup.sh -c start_ingestion\"" --tab-with-profile=Default --title="api" -e "bash -c \"$WORKING_DIR/ubuntu_setup.sh -c start_api\"" --tab-with-profile=Default --title="simple idp" -e "bash -c \"$WORKING_DIR/ubuntu_setup.sh -c start_simple_idp\"" --tab-with-profile=Default --title="search indexer" -e "bash -c \"$WORKING_DIR/ubuntu_setup.sh -c start_search_indexer\"" --tab-with-profile=Default --title="dashboard" -e "bash -c \"$WORKING_DIR/ubuntu_setup.sh -c start_dashboard\"" --tab-with-profile=Default --title="admin tools" -e "bash -c \"$WORKING_DIR/ubuntu_setup.sh -c start_admin_tools\"" --tab-with-profile=Default --title="data_browser" -e "bash -c \"$WORKING_DIR/ubuntu_setup.sh -c start_data_browser\"" 
    fi
    
}

resetDatabase ()
{
    cd $SLI_ROOT/config/scripts
    sudo bundle install
    ./resetAllDbs.sh
    
    cd $SLI_ROOT/acceptance-tests
    bundle install
    bundle exec rake realmInit
    bundle exec rake importSandboxData
    cd $SLI_ROOT/ingestion/ingestion-service/target/ingestion/lz/inbound/Midgar-DAYBREAK
    cp $SLI_ROOT/acceptance-tests/test/features/ingestion/test_data/SmallSampleDataSet.zip ./
    ruby $SLI_ROOT/opstools/ingestion_trigger/publish_file_uploaded.rb STOR $(pwd)/SmallSampleDataSet.zip
}

setup ()
{
    #setup additional apt repositories
    echo "Configuring oracle-java apt repo"
    sudo add-apt-repository -y ppa:webupd8team/java
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
    
    #config mongodb sources for correct version
    echo "Configure mongodb apt repo"
    echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
    
    #refresh packages
    sudo apt-get update
    
    packagelist=( "openssh-server" "git" "screen" "build-essential" "zip" "libxml2-dev" "libxslt1-dev" "libssl-dev" "zlib1g-dev" "ruby2.0" "ruby2.0-dev" "ruby-switch" "python-software-properties" "oracle-java7-installer" "mongodb-10gen=2.2.6" "maven" "activemq" )
    
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
    
    sudo gem install bundler
    # configure activemq
    sudo service activemq stop
    
    #check to see if we've already added stomp config to activemq
    if ! $(grep -q stomp /etc/activemq/instances-available/main/activemq.xml)
    then
        echo "Adding stomp config to activemq.xml"
        sudo perl -pi -e "s~<transportConnector name=\"openwire\" uri=\"tcp\://127\.0\.0\.1:61616\"/>~<transportConnector name=\"openwire\" uri=\"tcp://127\.0\.0\.1:61616\"/>\n\t\t<transportConnector name=\"stomp\" uri=\"stomp://0\.0\.0\.0\:61613\"/>~g" /etc/activemq/instances-available/main/activemq.xml
        # Stomp must be activated by adding <transportConnector name="stomp" uri="stomp://0.0.0.0:61613"/>to the conf/activemq.xml file in the <transportConnectors> block
    else
        echo "Stomp config already added to activemq.xml. Skipping."
    fi
    sudo ln -s /etc/activemq/instances-available/main /etc/activemq/instances-enabled/main
    sudo service activemq start
    
    # OpenADK 
    mkdir ~/Projects
    cd ~/Projects
    git clone https://github.com/open-adk/OpenADK-java.git
    cd OpenADK-java/adk-generator
    ant clean US
    cd ../adk-library
    # Change the ADK-library pom.xml line #7 from 1.0.0-snapshot to: 1.0.0 - This is due to the fact that the project dependency does not have SNAPSHOT in the version.
    perl -pi -e 's/1.0.0-SNAPSHOT/1.0.0/g' ./pom.xml
    mvn -P US install
    
    cd ~/Projects
    git clone https://github.com/inbloomdev/datastore.git
    
    cd ~/Projects
    git clone https://github.com/inbloomdev/datastore_ldap_inmemory.git

    #set env variables for future
    echo 'export MAVEN_OPTS="-Xmx2g -XX:+CMSClassUnloadingEnabled -XX:PermSize=128M -XX:MaxPermSize=512M"' >> ~/.bashrc
    echo 'export SLI_ROOT=~/Projects/datastore/sli' >> ~/.bashrc
    echo 'export IN_MEMORY_LDAP_ROOT=~/Projects/datastore_ldap_inmemory' >> ~/.bashrc

    source ~/.bashrc

    #need to export env variables for now
    export MAVEN_OPTS="-Xmx2g -XX:+CMSClassUnloadingEnabled -XX:PermSize=128M -XX:MaxPermSize=512M"
    export SLI_ROOT=~/Projects/datastore/sli
    export IN_MEMORY_LDAP_ROOT=~/Projects/datastore_ldap_inmemory
       

    cd ~/Projects/datastore/build-tools
    mvn clean install
    cd $SLI_ROOT
    mvn clean install -DskipTests
    
    #start mongodb
    sudo service mongodb start
    
    cd $SLI_ROOT/config/scripts
    sudo bundle install
    ./resetAllDbs.sh
    
    cp $SLI_ROOT/data-access/dal/keyStore/trustey.jks /tmp
    
    start_inmemory_ldap
    start_ingestion
    start_api
    start_simple_idp
    start_search_indexer
    
    #ingest sample data set
    cd $SLI_ROOT/acceptance-tests
    bundle install
    bundle exec rake realmInit
    bundle exec rake importSandboxData
    cd $SLI_ROOT/ingestion/ingestion-service/target/ingestion/lz/inbound/Midgar-DAYBREAK
    cp $SLI_ROOT/acceptance-tests/test/features/ingestion/test_data/SmallSampleDataSet.zip ./
    screen -S sample-ingestion -d -m ruby $SLI_ROOT/opstools/ingestion_trigger/publish_file_uploaded.rb STOR $(pwd)/SmallSampleDataSet.zip
    screen -S sample-ingestion-tail -d -m tail -F $SLI_ROOT/ingestion/ingestion-service/target/ingestion/logs/ingestion.log    
    
    start_dashboard
    
    #build admin-rails app
    cd $SLI_ROOT/admin-tools/admin-rails
    bundle install
    start_admin_tools
    
    #build databrowser rails app
    cd $SLI_ROOT/databrowser
    bundle install
    start_data_browser

    echo "Installation complete!" 
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
    echo "Stopping search indexer"
    cd $SLI_ROOT/search-indexer
    screen -S search-indexer -d -m ./scripts/local_search_indexer.sh stop
    screen -S search-indexer-tail -p 0 -X kill

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
    echo "Stopping datastore_ldap_inmemory"
    screen -S datastore_ldap_inmemory -p 0 -X stuff $'\003'
}

list ()
{
    screen -list
}

if [ -z "$SLI_ROOT" ]
then
   export SLI_ROOT=~/Projects/datastore/sli 
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
        #read -ep "Please enter your github username: " gitusername
        #read -esp "Please enter you github password: " gitpassword
        setup #gitusername gitpassword
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
    else
        echo "Valid parameters for this script are:"
        echo "    install : Performs initial installation and configuration of software"
        echo "    start : Start all components of the application"
        echo "    stop : Stop all components of the application"
        echo "    resetdb : Reset the database and rerun injestion of the sample dataset"
        echo "    list : List all active screen sessions"
    fi
fi
