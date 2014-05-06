Then /^the operator has an identifier$/ do
  @operator['operatorId'].should_not be_nil
end

# operator retrieval
When /^I GET that operator resource$/ do
  @response = RestClient.get(@response.headers[:location], :accept => :json)
end

# operator modification
Given /^I modify that operator resource$/ do
  @operator['operatorName'] = 'Illinois Cloud'
  @operator['enabled'] = false
end

When /^I PUT that operator resource$/ do
  url = path_for('operators', @operator['operatorId'])
  RestClient.put(url, @operator.to_json, :content_type => :json) { |response, request, result| @response = response }
end

Then /^the operator should be modified$/ do
  url = path_for('operators', @operator['operatorId'])
  @response = RestClient.get(url)
  modified = JSON.parse(@response)
  modified['enabled'].should be false
  modified['operatorName'].should == @operator['operatorName']
end

Given /^I have an invalid JSON representation of an operator$/ do
  bad_operator = operator_resource
  bad_operator['operatorName'] = ''
  @request_json = bad_operator.to_json
end

When /^I PUT that operator resource with the wrong id on the URL$/ do
  url = path_for('operators', 12345)
  RestClient.put(url, @operator.to_json, :content_type => :json) { |response, request, result| @response = response }
end

Given /^I modify that resource with an unknown id$/ do
  @operator['operatorId'] = 0
end

And /^the response contains an operator$/ do
  @operator = JSON.parse(@response)
end
