When(/^I click on the verification link from the e\-mail$/) do
 email = app_provider_resource['user']['email']
 email_link = verification_email_link(email)
 visit email_link
end

Then(/^I should be on the create password page$/) do
 page.should have_title('Create your Password')
end

Given(/^I am on the validation page$/) do
  pending # express the regexp above with the code you wish you had
end

When(/^I enter a valid password$/) do
  @password = 'AA!1aaaa'
  fill_in_password(@password)
end

When(/^I enter an invalid password$/) do
  @password = 'abcde'
  fill_in_password(@password)
end

When(/^I confirm that password$/) do
  fill_in_confirm_password(@password)
end

Then(/^the submit button is enabled$/) do
  page.should have_button('submit')
end

Then(/^the submit button is disabled$/) do
  page.should have_css('#submit[disabled]')
end

When(/^I enter a password of (.*)$/) do |password|
  fill_in_password(password)
end

When(/^I enter a different password confirmation$/) do
  fill_in_confirm_password('wxyz')
end

Then(/^I see a validation error of (.*)$/) do |validation_message|
  expect(page).to have_content(validation_message)
end

Then(/^I see no validation errors$/) do
  page.should have_no_css('.help-block li')
end

When (/^I click on (.*) button$/) do |button_name|
  page.should have_css('#' + button_name)
  click_button(button_name)
end

Then (/^I should be redirected to Sign in screen$/) do
  current_path.should == '/'
end

Given (/^I have already created the account$/) do
  pending
end

#methods

def fill_in_password(password)
  fill_in('Choose a Password', :with => password)
end

def fill_in_confirm_password(password)
  fill_in('Confirm Password', :with => password)
end
