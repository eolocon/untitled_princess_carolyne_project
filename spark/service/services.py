from pyspark.sql import SparkSession
from os import getenv
from pyspark.ml import PipelineModel

import schemas
import transformers
import streaming
import pipelines

def get_runner(service_type):
	"""Factory method for service runner"""

	if 'training' == service_type:
		return TrainingServiceRunner

	if 'prediction' == service_type:
		return PredictionServiceRunner

class ServiceRunner:
	"""Class to run a service.

	Has only a static method that istantiates the specified service runner

	"""

	@staticmethod
	def run():
		service_type = getenv('SERVICE', default='prediction')

		session = SparkSession.builder.appName(service_type + 'Service').getOrCreate()
		session.sparkContext.setLogLevel('OFF')
		get_runner(service_type).run(session=session)

class TrainingServiceRunner:
	"""A runner implementation for training service.

	Configures the service and runs it

	Todo:
		* the configuration is partially hard coded; refactor to modify this

	"""

	@staticmethod
	def run(session):
		"""Configure and run the service

			Args:
				session (obj): spark session

		"""

		trainingset_path = '/service/datasets/training_set_sentipolc16.csv'
		model_path = '/service/models/pipeline'
		

		reader_options = {
							'path': trainingset_path,
							'sep': ',',
							'header': True
						 }

		reader = streaming.SimpleCsvReader(session, reader_options)
		preprocessor = transformers.SentiPolc16Preprocessor()
		pipeline = pipelines.SentiPolc16().pipeline

		service = TrainingService(
									reader=reader,
									preprocessor=preprocessor,
									pipeline=pipeline,
									model_path=model_path
								)
		service.run()

class PredictionServiceRunner:
	"""A runner implementation for prediction service.

	Configures the service and runs it

	Todo:
		* the configuration is partially hard coded; refactor to modify this

	"""

	@staticmethod
	def run(session):
		"""Configure and run the service

			Args:
				session (obj): spark session

		"""

		kafka_broker = getenv('KAFKA_BROKER', default='kafka:9092')
		input_topics = getenv('IN_TOPICS', default='spark_input')
		output_topic = getenv('OUT_TOPICS', default='spark_output')

		model_path = '/service/models/pipeline'
		checkpoint_path = '/service/checkpoint'

		input_format = 'kafka'
		input_options = {
							'kafka.bootstrap.servers': kafka_broker,
			                'subscribe': input_topics,
			                'startingOffsets': 'earliest',
			                'failOnDataLoss': 'false'
			            }

		output_format = 'kafka'
		output_options = {
							'kafka.bootstrap.servers': kafka_broker,
							'topic': output_topic,
							'checkpointLocation': checkpoint_path
						 }	

		stream_reader = streaming.SimpleReader(session=session, format=input_format, options=input_options)
		stream_writer = streaming.SimpleStreamWriter(format=output_format, options=output_options)
		deserializer = transformers.SimpleKafkaDeserializer(schemas.prediction_input_schema)
		serializer = transformers.SimpleKafkaSerializer()
		preprocessor = transformers.SimplePreprocessor()
		postprocessor = transformers.SimplePostprocessor()
		pipeline = PipelineModel.load(model_path)
		
		service = PredictionService(
					stream_reader=stream_reader,
					stream_writer=stream_writer,
					deserializer=deserializer,
					serializer = serializer,
					preprocessor=preprocessor, 
					postprocessor = postprocessor,
					pipeline=pipeline
				)

		service.run()

class TrainingService:
	"""An implementation of a training service.

	The workflow of the service is the following:
		-preprocess input data
		-train the model with the input data
		-save the model

	"""

	def __init__(self, reader, preprocessor, pipeline, model_path):
		"""
			Args:
				reader (obj): input data reader
				preprocessor (obj): object to preprocess input data
				pipeline (pyspark.ml.Pipeline): pipeline containing the model to train
				model_path (str): path where to save the trained model

			Attributes:
				_dataframe (pyspark.sql.DataFrame): spark Dataframe containing the input data
				_preprocessor (obj): object to preprocess input data
				_pipeline (pyspark.ml.Pipeline): pipeline containing the model to train
				_trained_model (pyspark.ml.PipelineModel): trained model
				_model_path (str): path where to save the trained model

		"""

		self._dataframe = reader.read()
		self._preprocessor = preprocessor
		self._pipeline = pipeline
		self._model_path = model_path
		self._trained_model = None

	def run(self):
		# LOG
		print('\n\n\ntraining service is running\n\n')
		
		self._preprocess()
		self._train()
		self._save_model()

		# LOG
		print('\n\n\ntraining complete\n\n\n')
		print('accuracy:', self._trained_model.stages[-1].summary.accuracy)
		print('trained model saved in', self._model_path)

	def _preprocess(self):
		self._dataframe = self._preprocessor.transform(self._dataframe)

	def _train(self):
		self._trained_model = self._pipeline.fit(self._dataframe)

	def _save_model(self):
		self._trained_model.save(self._model_path)


class PredictionService:
	"""An implementation of the prediction service.

	The workflow of the service is the following:
	-deserialize input data
	-preprocess deserialized data
	-predict preprocessed data
	-postprocess predicted data
	-serialize postprocessed data
	-output serialized data

	"""

	def __init__(
				 self,
				 stream_reader,
				 stream_writer,
				 deserializer,
				 serializer,
				 preprocessor,
				 postprocessor,
				 pipeline
				):
		"""

			Args:
				stream_reader (obj): reader for input data
				stream_writer (obj): writer for output data
				deserializer (obj): object to deserialize input data
				serializer (obj): object to serialize output data
				preprocessor (obj): object to preprocess deserialized data
				postprocessor (obj): object to postprocess predicted data
				pipeline (pyspark.ml.PipelineModel): pipeline model to perform prediction on preprocessed data

		"""
		
		self._stream = stream_reader.load()
		self._stream_writer = stream_writer
		self._deserializer = deserializer
		self._preprocessor = preprocessor
		self._postprocessor = postprocessor
		self._serializer = serializer
		self._pipeline = pipeline

	def run(self):
		# LOG
		print('\n\n\nprediction service is running\n\n')
		
		self._deserialize_stream()
		self._preprocessing()
		self._predict()
		self._postprocessing()
		self._serialize_stream()
		self._write_stream()

	def _write_stream(self):
		self._stream_writer.write(self._stream)

	def _deserialize_stream(self):
		self._stream = self._deserializer.transform(self._stream)

	def _preprocessing(self):
	   	self._stream = self._preprocessor.transform(self._stream)

	def _predict(self):
		self._stream = self._pipeline.transform(self._stream)

	def _postprocessing(self):
		self._stream = self._postprocessor.transform(self._stream)

	def _serialize_stream(self):
		self._stream = self._serializer.transform(self._stream)

