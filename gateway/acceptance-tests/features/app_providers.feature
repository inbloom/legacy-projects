Feature:
  As an application provider
  I need to register for an account at inBloom
  and validate my email address
  so that I can start creating apps.

  Background:
    Given I have a JSON representation of an app provider

  Scenario: An Application Provider registers for an account
    When I POST to the applicationProviders resource
    Then the response status should be 201 Created
    And the response contains a representation of the app provider
    And the response contains a location header for the app provider
    And the app provider receives an email with a verification link that is good for 3 days

  Scenario: An App Provider cannot register twice
    Given I have already registered as an app provider
    When I POST to the applicationProviders resource
    Then the response status should be 400 Bad Request

  Scenario Outline: An App Provider leaves off required attributes
    When I POST to the applicationProviders resource without <field>
    Then the response status should be 400 Bad Request

  Examples:
    | field     |
    | firstName |
    | lastName  |
    | email     |

  Scenario Outline: An App Provider leaves off optional attributes
    When I POST to the applicationProviders resource without <field>
    Then the response status should be 201 Created

  Examples:
    | field            |
    | organizationName |

Scenario: An Application Provider modifies account information
 Given I have already registered as an app provider
  When I modify my app provider information
   And I POST the update to applicationProviders resource
  Then the response status should be 204 No Content
   And my account information should be modified
