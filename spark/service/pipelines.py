from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, Word2Vec
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline

"""Module containing user defined pipelines"""

class SentiPolc16:
	"""Simple training pipeline, composed of:
	
		- a tokenizer
		- a stopwords remover
		- a features extracor (word2vec)
		- a binary classificator (logistic_regressor)

	"""

	def __init__(self):
		self._tokenizer = RegexTokenizer(inputCol='text', outputCol='tokens', pattern=r'\W')
		self._stopwords_remover = StopWordsRemover(
										   inputCol=self._tokenizer.getOutputCol(), outputCol='filtered_words',
		                                   stopWords=StopWordsRemover.loadDefaultStopWords('italian')
		                                )
		self._word2vec = Word2Vec(inputCol=self._stopwords_remover.getOutputCol(), outputCol='features_vector', vectorSize=100)
		self._logistic_regressor = LogisticRegression(featuresCol=self._word2vec.getOutputCol(), labelCol='positive', maxIter=100)


		self.pipeline = Pipeline(stages=[
											self._tokenizer,
											self._stopwords_remover,
											self._word2vec,
											self._logistic_regressor
										]
							)