# Recreate a new empty test database
class DatabaseCleaner

  attr_reader :database, :test_database

  def initialize(database, test_database=nil)
    @database = database
    @test_database = test_database || "#{database}_test"
  end

  def reset_database
    drop_database
    create_database
    load_database
  end

  def create_database
    exec_mysql "create database #{test_database}"
  end

  def drop_database
    exec_mysql "drop database if exists #{test_database}"
  end

  def load_database
    cmd = "mysqldump -u #{ENV['DB_USERNAME']} "
    cmd << "-p #{ENV['DB_PASSWORD']}" if ENV['DB_PASSWORD']
    cmd << "-d #{database} | "
    cmd << "mysql -u #{ENV['DB_USERNAME']} "
    cmd << "-D#{test_database}"
    system cmd
  end

  private

  def exec_mysql(command)
    cmd = "mysql -u #{ENV['DB_USERNAME']} "
    cmd << "-p #{ENV['DB_PASSWORD']} " if ENV['DB_PASSWORD']
    cmd << "-e '#{command}'"
    system cmd
  end
end