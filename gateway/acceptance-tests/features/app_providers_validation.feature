@LDAPCleanup
Feature:
  As an Application Provider
  I want to validate my account
  So that I can get credentials and use the development environment within inBloom

  Background:
    Given I have a JSON representation of an app provider
    And I have already registered as an app provider
    And I have a JSON representation of an account validation

  Scenario: An application provider validates his account
    When I POST to the verifications resource with a valid token
    Then the response status should be 200 OK
    And the response contains a representation of a validated verification

  Scenario: An application provider validates his account with expired verification
    Given my verification has expired
    When I POST to the verifications resource with a valid token
    Then the response status should be 403 Forbidden
    And the response body status code should be EXPIRED

  Scenario: An application provider validates his account with a bad password
    Given I have a JSON representation of an account validation with an invalid password
    When I POST to the verifications resource with a valid token
    Then the response status should be 400 Bad Request

  Scenario: An application provider has previously validated his account
    Given my verification has previously been redeemed
    When I POST to the verifications resource with a valid token
    Then the response status should be 403 Forbidden
    And the response body status code should be REDEEMED

  Scenario: An application provider validates his account with an non-existent token
    When I POST to the verifications resource with a valid token