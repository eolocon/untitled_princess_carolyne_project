"""Module with various input/output classes.

The module name is misleading, since not all the classes use spark streaming capabilities.

	Todo:
		*refactor so tha the class in the module are coherent withe the module;
		 this could lead to the creation of new modules

"""

class SimpleCsvReader:
	"""Simple implementation of a csv reader."""
	
	def __init__(self, session, options):
		"""
		
		Args:
			session (obj): spark session
			options (obj): reader options

		Attributes:
			_options (obj): reader options
			_reader (obj): csv reader
		
		"""

		self._options = options
		self._reader = session.read

	def read(self):
		"""Read from csv input.
		
			Returns:
				pyspark.sql.Dataframe

		"""

		return self._reader.csv(**self._options)

class SimpleReader:
	"""Simple implementation of a reader.
	
	Can read from the various spark sources.
	The specified options must be coherent with the source.

	"""
	def __init__(self, session, format, options):
		"""

			Args:
				session (obj): spark session
				format (str): string specifying a valid spark source
				options (obj): reader options

			Attributes:
				_reader (obj): source reader
		
		"""

		self._reader = session.readStream.format(format)
		for key, value in options.items():
			self._reader.option(key, value)

	def load(self):
		""" Load data from the specified source

			Returns:
				pyspark.ml.DataFrame

		"""

		return self._reader.load()

class SimpleStreamWriter:
	"""Simple implementation of a writer.

	Can write on the various spark sinks.
	The specified options must be coherent with the sink.

	"""

	def __init__(self, format, options):
		"""

			Args:
				format (str): string specifying a valid spark sink
				options (obj): writer options

			Attributes:
				_format (str): string specifying a valid spark sink
				_options (obj): writer options
				_writer (obj): sink writer

		"""

		self._format = format
		self._options = options
		self._writer = None
	
	def write(self, df):
		"""Write to the specified sink.

			Args:
				df (pyspark.ml.DataFrame): spark DataFrame to write
		
		"""

		self._config_writer(df)
		self._writer.start().awaitTermination()

	def _config_writer(self, df):
		"""Configure the writer."""
		
		self._writer = df.writeStream.format(self._format).outputMode('append')
		for key, value in self._options.items():
			self._writer.option(key, value)