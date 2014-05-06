Then /^each realm has an "identifier" and a "name"$/ do
  @realms.each do |realm|
    realm['identifier'].should_not be_nil
    realm['name'].should_not be_nil
  end
end

