Given(/^I have already registered as an app provider$/) do
  @response = RestClient.post(path_for('applicationProviders'), @request_json, :content_type => :json)
end

Then /^the response contains a representation of the app provider$/ do
  app_provider = JSON.parse(@response)
  app_provider['applicationProviderId'].should_not be_nil
  %w(applicationProviderName organizationName).each do |attr|
    app_provider[attr].should == app_provider_resource[attr]
  end
  app_provider['user']['userId'].should_not be_nil
  %w(email firstName lastName).each do |attr|
    app_provider['user'][attr].should_not == app_provider_resource[attr]
  end
end

Then /^the response contains a location header for the app provider$/ do
  app_provider = JSON.parse(@response)
  @response.headers[:location].should == path_for('applicationProviders',app_provider['applicationProviderId'])
end

Then(/^the app provider receives an email with a verification link that is good for (\d+) days$/) do |days|
  user_id = JSON.parse(@response)['user']['userId']
  user_id.should_not be_nil

  email_to = app_provider_resource['user']['email']
  mail_file = email_file_for(email_to)
  # dir = File.expand_path File.dirname(__FILE__)
  # mail_file = File.join(dir,'..','..','..','gateway','gateway-boot','temp', "#{email_to}.eml")
  File.exists?(mail_file).should be_true

  verify_email_verification_link(mail_file, user_id, days.to_i)
end

def verify_email_verification_link(email_file, user_id, expires_in_days)
  results = db_client.query("SELECT * FROM verifications WHERE user_id=#{user_id}")
  verification = results.first
  verification.should_not be_nil, "Verification not found for user #{user_id}"
  verification['is_verified'].should be(0), "Verification 'is_verified' flag was not false(0)"
  verification['valid_from'].to_i.should be_within(60).of(Time.new.to_i), "'valid_from' date is not within 1 minute of now"
  (verification['valid_until'] - verification['valid_from']).should == 60*60*24*expires_in_days #, "Expiration period is not #{expires_in_days}"

  token = verification['token']

  # Verify that the file contains a link with the correct token
  link_regex = /<a id="validate-link" href=".+\/email_validation\?token=#{Regexp.escape(token)}/
  File.open(email_file).read.should match(link_regex)
end

def verification_email_link(email)
  link_regex = /<a id="validate-link" href="([^"]+)/
  File.open(email_file_for(email)).read.match(link_regex).captures.first
end

def email_file_for(email)
  dir = File.expand_path File.dirname(__FILE__)
  File.join(dir,'..','..','..','gateway','gateway-boot','temp', "#{email}.eml")
end

When(/^I POST to the applicationProviders resource without (.*)$/) do |field|
  resource = app_provider_resource
  case field
    when 'organizationName'
      resource['organizationName'] = nil
    when 'firstName'
      resource['user']['firstName'] = nil
    when 'lastName'
      resource['user']['lastName'] = nil
    when 'email'
      resource['user']['email'] = nil
    else
      fail("Unexpected field #{field}")
  end
  @request_json = resource.to_json
  RestClient.post(path_for('applicationProviders'), @request_json, :content_type => :json) do |response, request, result|
    @response = response
  end
end

When /^I POST to the verifications resource with a valid token$/ do
  user_id = JSON.parse(@response)['user']['userId']
  @app_provider_email = JSON.parse(@response)['user']['email']
  token = db_client.query("SELECT token FROM verifications WHERE user_id=#{user_id}").first['token']
  RestClient.post(path_for('verifications', token), @request_json, :content_type => :json) do |response, request, result|
    @response = response
  end
end

Then /^the response contains a representation of a validated verification$/ do
  verification = JSON.parse(@response)
  verification['verified'].should == true
end

Given /^my verification has expired$/ do
  db_client.query("update verifications set valid_from = '2014-04-08 00:00:00', valid_until = '2014-04-08 00:00:00'")
end

When /^I GET that applicationProviders resource$/ do
  @response = RestClient.get(@response.headers[:location], :accept => :json)
end

When /^I modify my app provider information$/ do
  @app_provider = JSON.parse(@response)
  @app_provider['organizationName'] = 'Learning Forever Inc'
  @app_provider['user']['firstName'] = 'Jane'
  @app_provider['user']['lastName'] = 'Doe'
  @app_provider['user']['email'] = 'jane.doe@inbloom.org'
end

When /^I POST the update to applicationProviders resource$/ do
  @url = path_for('applicationProviders', @app_provider['applicationProviderId'])
  RestClient.post(@url, @app_provider.to_json, :content_type => :json) do |response, request, result|
    @response = response
  end
end

Then /^my account information should be modified$/ do
  @response = RestClient.get(@url)
  modified = JSON.parse(@response)
  modified.should eq(@app_provider)
end

Given /^my verification has previously been redeemed/ do
  db_client.query("UPDATE verifications SET is_verified=1")
end

When(/^I fill in registration fields with valid information$/) do
  fill_in 'First Name', :with => 'Mary'
  fill_in 'Last Name', :with => 'Jane'
  fill_in 'Company', :with => "Learning 'R' Us"
  fill_in 'Email', :with => 'mary.jane@learningrus.com'
end

Then(/^I should be presented with the EULA$/) do
  pending
  # page.should have_title('inBloom EULA')
end

Then(/^I should see some fields are required$/) do
  page.should have_css('#firstname[required]')
  page.should have_css('#lastname[required]')
  page.should have_css('#email[required]')
end
