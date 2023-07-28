import logging
from os import mkdir, listdir, path
from time import strftime


class Logger:


	def __init__(self, directory_name=None, level=None, file_stream=False):

		self.file_stream = file_stream

		if self.file_stream:

			if not directory_name:
				directory_name = "logs"

			if directory_name not in listdir("."):
				mkdir(directory_name)

			self.directory_name = directory_name

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


	def get_logger(self, name: str="untitled") -> logging.Logger:

		if name == "root":
			print("WARNING: better not use name 'root' for logger name")

		file_name = strftime("[%d-%m-%y] %H-%M-%S.log")

		logger = logging.getLogger(name)
		logger.setLevel(logging.DEBUG)
		stream_handler = logging.StreamHandler()
		formatter = logging.Formatter(fmt="[%(name)s] %(levelname)s: %(message)s")
		stream_handler.setFormatter(formatter)
		stream_handler.setLevel(self.level)

		if self.file_stream:

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
