require 'dotenv'
Dotenv.load

module Gateway

  APP_ROOT = File.expand_path(File.dirname(__FILE__) + "/../")

  class Api < Thor
    desc 'start', 'Start the Gateway API using the test database'
    def start
      exec start_command
    end

    private

    def start_command
      path = File.join(APP_ROOT,'..','gateway','gateway-boot')
      mvn_command = "mvn -DsaveEmailToFile=true -Dspring.datasource.url=jdbc:mysql://localhost:3306/#{ENV['DB_NAME']}_test spring-boot:run"
      "cd #{path} && #{mvn_command}"
    end
  end

  class Portal < Thor
    desc 'start', 'Start the Gateway Portal UI'
    def start
      exec start_command
    end

    private

    def start_command
      path = File.join(APP_ROOT,'..','gateway','gateway-portal')
      mvn_command = 'mvn spring-boot:run'
      "cd #{path} && #{mvn_command}"
    end
  end

end