Feature:
  As an Application Provider
  I want to submit my information for an account with inBloom on the Registration page and Accept the EULA
  So that I establish an account and develop my inBloom application

  Scenario: App Provider registers for an account with minimal information
    Given I am on the registration page
     When I fill in registration fields with valid information
      And I submit the form
     Then I should be presented with the EULA

  Scenario: App Provider registers for an account with missing information
     When I am on the registration page
     Then I should see some fields are required
