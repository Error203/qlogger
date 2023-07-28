# qlogger
simple logger library based on logging original library of python (for my purposes, but you can use it as well)

# Logger class
Takes "directory_name", "level" and "file_stream" arguments.
The first one is the directory where .log files will be written (by default logs dir in ./).
The second one is a string, level of debugging (can be info, debug, warning, error, critical)
The third one is bool, set True and qlogger will write files into "directory_name", set False and it will not.

"get_logger" function takes one argument: "name", a string.
Makes some needed stuff and returns you tuple of logger and file_logger objects based on Logger class to work with. (for more information check out logging library on official site)
