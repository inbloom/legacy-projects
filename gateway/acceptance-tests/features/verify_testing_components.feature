@wip
Feature:
  As a developer
  In order to verify my setup
  I want to execute a simple cucumber feature

# This scenario is simply used to verify that the testing components are set up correctly
#
Scenario: Verify testing components
  Given I am using Cucumber with RSpec
   When I exercise Capybara
    And I exercise Rest-Client
    And I exercise WebMock
   Then all is green