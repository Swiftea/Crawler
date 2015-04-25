require 'simplecov'
require 'coveralls'

SimpleCov.formatter = Coveralls::SimpleCov::Formatter
SimpleCov.start do
   add_filter 'crawler/package/database_manager.py'
   add_filter 'crawler/package/database_swiftea.py'
   add_filter 'crawler/package/FTP.py'
   add_filter 'crawler/package/ftp_manager/py'
   add_filter 'crawler/package/file_manager.py'
end
