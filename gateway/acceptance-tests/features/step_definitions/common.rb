require 'net/ldap'

Given /^I have a JSON representation of a(?:n?) (.*)$/ do |resource_type|
  resource_type.gsub!(' ','_')
  @request_json = send("#{resource_type}_resource").to_json
end

Given(/^I am on the (.*) page$/) do |page|
  visit portal_path_for(page)
end

When /^I GET the (.*) resource$/ do |resource_type|
  @response = RestClient.get(path_for(resource_type)) { |response, request, results| response }
end

Then /^I get a list of (.*)$/ do |resource_type|
  body = JSON.parse(@response)
  body.should be_a_kind_of Array
  instance_variable_set("@#{resource_type}", body)
end

Then /^the response status should be (\d+)/ do |code|
  @response.code.should == code.to_i
end

Then /^the response body status code should be (.*)$/ do |code|
  body = JSON.parse(@response)
  body['status'].should == code
end

When /^I POST to the (.*?) resource$/ do |resource|
  RestClient.post(path_for(resource), @request_json, :content_type => :json) do |response, request, result|
    @response = response
  end
end

When(/^I submit the form$/) do
  click_button 'Submit'
end

def db_client
  @db_client ||= Mysql2::Client.new(:host => 'localhost', :username => ENV['DB_USERNAME'], :database => "#{ENV['DB_NAME']}_test")
end

def app_provider_resource
  {
    'applicationProviderName' => 'Math Cats LLC',
    'organizationName' => 'Learning Kitties Holdings Inc',
    'user' => {
      'email' => 'john.smith@inbloom.org',
      'firstName' => 'John',
      'lastName' => 'Smith'
    }
  }
end

def operator_resource
  {
      'operatorName' => 'Illini Cloud',
      'primaryContactName' => 'Chief Illiniwek',
      'primaryContactEmail' => 'chief@illinicloud.edu',
      'primaryContactPhone' => '5185551212',
      'apiUri' => 'http://localhost:8080',
      'connectorUri' => 'http://localhost:8080/connector',
      'enabled' => true
  }
end

def account_validation_resource
  {
      'password' => 'P@5Sw0rd'
  }
end

def account_validation_with_an_invalid_password_resource
  {
      'password' => 'password'
  }
end

