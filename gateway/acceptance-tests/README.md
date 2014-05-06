# Gateway Acceptance Tests

##Assumptions

1. the mysql database has been created and the mysql server is running (`mysql.server start`)
2. the application is running on the localhost at port 9001 against the test database (`thor gateway:start`)

## Environment Variables

The tests make use of the following environment variables for parameterizing external services
(including the gateway application itself). For testing purposes, default values for the environment variables used by
the tests are specified in the `.env` file.

- **GATEWAY_API_URL** - the full URL to the gateway API (e.g. `http://localhost:9001/gateway`)
- **GATEWAY_PORTAL_URL** - the full URL to the gateway portal (e.g. `http://localhost:9000`)
- **DB_USERNAME** - the MySQL database username (e.g. `root`)
- **DB_NAME**     - the name of the development database (e.g. `gateway`); the test datbase name is derived by adding `_test`

##Running the tests

You can execute the following commands from the acceptance-tests directory:

- `thor test:features # Runs all features (except those tagged as *@wip*)`
- `thor test:feature app_providers # Runs all scenarios in the *app_providers* feature`
- `thor test:feature app_providers:17 # Runs the scenario on line 17 of the *app_providers* feature`

## Writing tests

One aspect of the acceptance tests that must be considered (and an appropriate strategy discussed) is how data is
managed. A tenet of any good test design is that the test itself should be responsible for creating any required data
and then cleaning data up (i.e. not leaving any side effects) after the test completes. One strategy for accomplishing
this is by using a separate test database that is setup after every scenario run.