APP_ROOT = File.expand_path(File.dirname(__FILE__) + "/../")
require "#{APP_ROOT}/features/support/database_cleaner"

class Test < Thor

  desc 'features', 'Run all non-wip cucumber features'
  def features
    run_command cucumber_command
  end

  desc 'feature [NAME]', 'Run the cucumber feature NAME'
  long_desc <<-DESC
    `test:feature NAME` runs features/NAME.feature
    \x5`test:feature NAME/` runs all features in the features/NAME directory
    \x5`test:feature NAME:123` runs the scenario at the given line number
  DESC
  def feature(name='')
    run_command feature_command(name)
  end

  desc 'db_reset', 'Reset the test database'
  def db_reset
    DatabaseCleaner.new(ENV['DB_NAME']).reset_database
  end

  private

  def feature_command(feature)
    to_run = feature.dup
    unless to_run.empty?
      unless to_run.end_with? '/'
        file, line = to_run.split(':')
        file << '.feature' unless file.end_with? '.feature' # add missing extension
        file << ":#{line}" if line
        to_run = file
      end
      to_run = "features/#{to_run}"
    end
    "cd #{APP_ROOT} && cucumber --color #{to_run}"
  end

  def cucumber_command
    "cd #{APP_ROOT} && cucumber --color --tags ~@wip"
  end

  def run_command(command)
    puts `#{command}`
  end
end