module Paths
  def path_for(resource, id=nil)
    path = case resource
      when /^realms$/
        'realms'
      else
        resource
     end
     url = "#{ENV['GATEWAY_API_URL']}/#{path}/#{id}"
  end
  def portal_path_for(resource, id=nil)
    path = case resource
             when /^registration$/
               'registration'
             else
               resource
           end
    url = "#{ENV['GATEWAY_PORTAL_URL']}/#{path}/#{id}"
  end
end