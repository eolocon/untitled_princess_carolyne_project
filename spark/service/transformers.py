from pyspark.sql.functions import from_json, to_json, struct, col

"""Module containing various dataframe transformers

   Todo:
   		*each class in the module should be refactor to extend the spark 'Transformer' class

"""

class SentiPolc16Preprocessor:
	"""Preprocessor for the sentipolc16 dataset"""

	def transform(self, df):
		return df.withColumn('positive', col('positive').cast('integer'))

class SimpleKafkaDeserializer:
	"""Deserializer for messages from Kafka"""

	def __init__(self, schema):
		"""
			Args:
				schema (obj): schema to parse the messages

			Attributes:
				_schema (obj): schema to parse the messages

		"""

		self._schema = schema

	def transform(self, df):
		"""
			Args:
				df (pyspark.slq.DataFrame): spark DataFrame containing messages from Kafka

		"""

		return df.withColumn('value', df.value.cast('string')) \
		  		 .withColumn('value', from_json('value', schema=self._schema))

class SimpleKafkaSerializer:
	"""Serializer for messages to Kafka"""

	def transform(self, df):
		"""
			Args:
				df (pyspark.slq.DataFrame): spark DataFrame containing messages to Kafka

		"""

		return df.select(to_json(struct(df.columns)).alias('value'))

class SimplePreprocessor:
	def transform(self, df):
		return df.select('value.data.*') \
		         .withColumnRenamed('document_text', 'text')

class SimplePostprocessor:
	def transform(self, df):
		drop_list = ['tokens', 'filtered_words', 'features_vector', 'rawPrediction', 'probability']

		return df.withColumnRenamed('text', 'document_text') \
				 .withColumnRenamed('prediction', 'polarity') \
		         .drop(*[col for col in drop_list])
			