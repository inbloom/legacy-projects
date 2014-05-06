# Add your Before, After and Around hooks here
Before do
  db_cleaner = DatabaseCleaner.new(ENV['DB_NAME'])
  db_cleaner.reset_database
end

After '@LDAPCleanup' do
  ldap_cleanup if @app_provider_email
end

def ldap_cleanup
  puts "Removing #{@app_provider_email} from LDAP"
  base = 'ou=LocalNew,ou=DevTest,dc=slidev,dc=org'
  group_base  = "ou=groups,#{base}"

  ldap_config = {
      :host => '127.0.0.1',
      :port => 10389,
      :base => group_base, # sets the treebase for search
      :auth => {
          :method => :simple,
          :username => 'cn=Admin,dc=slidev,dc=org',
          :password => 'test1234'
      }
  }

  Net::LDAP.open(ldap_config) do |ldap|
    # Remove user from the groups
    ['application_developer', 'Sandbox Administrator'].each do |group_id|
      group_dn = "cn=#{group_id},#{group_base}"
      group = ldap.search(:filter => Net::LDAP::Filter.eq('cn', group_id)).first
      if group
        removed = group[:memberuid].delete(@app_provider_email)
        ldap.replace_attribute(group_dn, :memberuid, group[:memberuid]) if removed
      end
    end

    # Delete the user
    ldap.delete(:dn => "cn=#{@app_provider_email},ou=people,#{base}")
  end
end