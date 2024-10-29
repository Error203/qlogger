import logging
from os import mkdir, listdir, path, remove
from time import strftime


class ColoredFormat(logging.Formatter):

	yellow = "\x1b[33;20m"
	red = "\x1b[31;20m"
	bold_red = "\x1b[31;1m"
	reset = "\x1b[0m"
	format = "[%(name)s] %(levelname)s: %(message)s"

	FORMATS = {

		logging.NOTSET: format,
		logging.DEBUG: format,
		logging.INFO: format,
		logging.WARNING: yellow + format + reset,
		logging.ERROR: red + format + reset,
		logging.CRITICAL: bold_red + format + reset,

	}

	def format(self, record):
		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(log_fmt)
		return formatter.format(record)


class DefaultFormat(logging.Formatter):

	format = "[%(name)s] %(levelname)s: %(message)s"

	FORMATS = {

		logging.NOTSET: format,
		logging.DEBUG: format,
		logging.INFO: format,
		logging.WARNING: format,
		logging.ERROR: format,
		logging.CRITICAL: format,

	}

	def format(self, record):
		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(log_fmt)
		return formatter.format(record)


class Logger:


	def __init__(self, directory_name=None, level=None, file_stream=False, file_cap=None, color=None):

		self.file_stream = file_stream
		self.color = color

		if self.file_stream:

			if not directory_name:
				directory_name = "logs"

			if directory_name not in listdir("."):
				mkdir(directory_name)

			self.directory_name = directory_name

		if not file_cap:

			self.file_cap = 10

		if level:

			level = level.lower()

		self.level = self.level_resolver(level)


	def level_resolver(self, level=None):

		if not level or level == "info":

			return logging.INFO

		if level == "debug":

			return logging.DEBUG

		if level == "warning":

			return logging.WARNING

		if level == "error":

			return logging.ERROR

		if level == "critical":

			return logging.CRITICAL

		else:

			return logging.NOTSET


	def prevent_overwriting(self, file_name):
		'''
		Function to prevent overwriting
		other log files, e.g.
		script was launched at the same time (which is not
		really intended, but can be) then it'll check
		if there is a log named exactly like that, and
		will add (2), I WILL HOPE THAT
		NOONE COULD RUN THE SCRIPT IN LESS THEN A SECOND
		AND I DOUBT THAT THOSE LOGS FOR A LITERALLY SECOND
		WOULD MAKE SOME USE FOR THE USER, OKAY?
		'''
		base_name, ext = path.splitext(file_name)

		if file_name in listdir(self.directory_name):

			return base_name + " (2)" + ext

		return file_name


	def process_cap(self):

		'''
		Function to process file cap in directory,
		e.g. if the cap is 10, then on the 11th
		log file created, it will delete the
		oldest log in directory, therefore
		not taking a lot of space
		'''

		log_directory_files = listdir(self.directory_name)
		logs_count = len(log_directory_files)
		log_directory_files.sort()
		'''
		let's hope that there is no garbage
		in the log directory, so we can
		sort those logs out to understand
		what log file is the oldest to then
		delete it
		'''

		if logs_count > self.file_cap:

			for i in range(logs_count - self.file_cap):

				log_file = path.join(self.directory_name, log_directory_files[0])

				if log_file.endswith(".log"):
					remove(log_file)
					log_directory_files.pop(0)


	def get_logger(self, name: str="untitled") -> logging.Logger:

		if name == "root":
			print("WARNING: it's better not use name 'root' for logger name as it'll double the output")

		file_name = strftime("[%d-%m-%y] %H-%M-%S.log")
		file_name = self.prevent_overwriting(file_name)

		logger = logging.getLogger(name)
		logger.setLevel(logging.DEBUG)
		stream_handler = logging.StreamHandler()

		stream_handler.setFormatter(DefaultFormat())
		
		if self.color:

			stream_handler.setFormatter(ColoredFormat())

		stream_handler.setLevel(self.level)

		if self.file_stream:

			self.process_cap()

			file_handler = logging.FileHandler(path.join(self.directory_name, file_name))
			file_formatter = logging.Formatter(fmt="[%(asctime)s] %(name)s, %(levelname)s: %(message)s")
			file_handler.setFormatter(file_formatter)
			file_handler.setLevel(logging.DEBUG)
			file_logger = logging.getLogger(name)
			file_logger.addHandler(file_handler)
			print(file_logger.handlers)
			logger.addHandler(file_handler)

		logger.addHandler(stream_handler)

		return (logger, file_logger)


def main():

	log = Logger(file_stream=True)
	logger = log.get_logger("testing")[1]
	logger.info("hello world")
	logger.warning("warning msg")
	logger.critical("critical msg")



if __name__ == '__main__':
	main()
