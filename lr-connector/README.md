LR Connector
===========

The LR Connector pulls data from the Learning Registry node and extracts and inserts relevant data into the LRI.


External Dependencies
------------

* GnuPG: http://www.gnupg.org/


Deployment
------------

1. Verify that GnuPG is installed
2. Clone the inBloom LR Connector git repository to the deployment directory
3. Install the required libraries:

        pip install -r requirements.txt
4. Configure by editing config.json (see **Configuration** below)
5. Launch the connector:

        python connector.py


Configuration
------------

Breakdown of the configuration options provided in config.json:

**Learning Registry configuration**

    {
        "lr": {
            "url": "http://lrnode.inbloom.org",
            "first_run_start_date": "2013-04-05",
            "public_key_fingerprint": "5FCAF0FB45631978389313FA6350F8DF35B1647B",
            "tagger_submitter": "inBloom Tagger Application <tagger@inbloom.org>"
        },

* "url" - URL of the Learning Registry node
* "first_run_start_date" - Beginning harvest time to use for the first run of the connector

The following two settings are used to determine if an envelope was published by Tagger:

* "public_key_fingerprint" - Fingerprint of the key used by the inBloom Learning Registry node
* "tagger_submitter" - Submitter value set by the node when publishing from Tagger

**LRIB configuration**

        "lrib": {
            "url": "http://lriserver.inbloom.org",
            "username": "lri",
            "password": "7u2GR94z",
            "access_token": "DELEGATE_0",
            "local_cache_expiration": 86400
        },

* "url" - URL of the LRI API

Include the following two settings if the LRI API is protected by Basic Authentication

* "username" - Username for basic authentication
* "password" - Password for basic authentication

* "access_token" - Delegate access token for assertions by proxy.  This value should match a value in the "delegate_tokens" list in the lri_config.json file of the LRI instance
* "local_cache_expiration" - Connector caches the results of some LRI calls for improved performance.  This setting determines the expiration time (in seconds) of that local cache

**LRIS configuration**

        "lris": {
            "host": "localhost",
            "port": "9200",
            "index": "lris",
            "index_type": "schema-org"
        },

* "host" - Host of the ElasticSearch instance
* "port" - Port of the ElasticSearch instance
* "index" - Name of the index to use for the LRIS
* "index_type" - Name of the type to use for indexing data from the Learning Registry.  This value must match the type name from the mappings section within lrissetings.json

**GnuPG configuration**

        "gpg": {
            "binary": "/usr/bin/gpg"
        },

* "binary" - Path to the GnuPG binary

**Connector-specific configuration**

        "logging_level": "DEBUG",
        "interval": 60
    }

* "logging_level" - Sets the level of the python logging module used within Connector
* "interval" - Harvest interval (in seconds)


Licensing
=========
LR Connector is licensed under the Apache License, Version 2.0. See LICENSE-2.0.txt for full license text.
