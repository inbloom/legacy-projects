require 'dotenv'
Dotenv.load

require 'capybara'
Capybara.default_driver = :selenium

require 'capybara-screenshot'
require 'capybara-screenshot/cucumber'

require 'webmock/cucumber'
WebMock.allow_net_connect!

require 'rest-client'
require 'mysql2'

require_relative 'paths'

class TestWorld
  include Capybara::DSL
  include Paths
end

World do
  TestWorld.new
end