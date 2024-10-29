# qlogger
simple logger library based on logging original library of python (for my purposes, but you can use it as well, hope I will continue to maintain it so it would be really helpful and convenient)

# Logger class
Takes next arguments:
  "directory_name" - used to specify the path for script to save logs, default is "logs" dir in the script's folder (yeah, for now it does not have support for rooting, I'll add it later).
  "level" - used to specify the MINIMUM level the script will output info at. So e.g. "debug" will output absolutely everything. "info" will ignore "debug" and output everything above. However, logging to a file will always be from "debug" to the highest, so it's an argument for a stream logging. default: "info"
  "file_stream" - whether write or not logs to a file, default: false
  "file_cap" - used to specify the file cap for the logs directory. e.g. cap is 10, so on the 11th log the script will remove the oldest out of log files. default: 10
  "color" - whether use colored output or not. Takes changes only on stream (output to terminal) the file will still be plain, without coloring.

"get_logger" function takes one argument: 
  "name" - a string with a name for the logger. Could be name of module. default: "untitled"
  
At the end script returns to you a configured sample of the logging.Logger("stuff").get_logger() class. To see how to work with that consider reading about it in pip.
