require 'simplecov'
require 'coveralls'

SimpleCov.formatter = Coveralls::SimpleCov::Formatter
SimpleCov.start do
   add_filter '/crawler/package/database_manager'
   add_filter '/crawler/package/database_swiftea'
   add_filter '/crawler/package/FTP'
   add_filter '/crawler/package/ftp_manager'
   add_filter '/crawler/package/__init__'
   add_filter '/crawler/package/data'
   add_filter '/crawler/package/file_manager'
end
