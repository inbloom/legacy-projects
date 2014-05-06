@LDAPCleanup
Feature:
  As an unverified application provider
  In order to complete my registration on the gateway
  I need to be able to set the password for my new account

Background:
  Given I have a JSON representation of an app provider
  And I have already registered as an app provider
  And I click on the verification link from the e-mail

  Scenario: A user clicks on the link in their verification e-mail
   Then I should be on the create password page

 Scenario: A user enters a valid password on the validation page and confirms
    When I enter a valid password
     And I confirm that password
    Then the submit button is enabled
     And I see no validation errors

 Scenario: A user enters a valid password on the validation page but does not confirm
    When I enter a valid password
    Then the submit button is disabled

 Scenario: A user enters an invalid password on the validation page
    When I enter an invalid password
     And I confirm that password
    Then the submit button is disabled


 Scenario Outline: User sees validation errors on invalid password input
    When I enter a password of <password>
    Then I see a validation error of <message>
   Examples:
   | password | message |
   | AA!aaaa  | 1 digit |
   | AA1aaaa  | 1 special character |
   | !1aaaa   | 2 upper case     |
   | AA!1     | 2 lower case     |
   | AA!1aaa  | 8 character minimum length|

 Scenario: User sees validation errors on non-matching password confirmation
    When I enter a valid password
     And I enter a different password confirmation
    Then I see a validation error of passwords must match

 Scenario: User cancels the Create Password process
     When I click on cancel button
     Then I should be redirected to Sign in screen

 Scenario: User clicks validation link after account has already been created
    Given I have already created the account
     When I click on the verification link from the e-mail
     Then I should be redirected to Sign in screen