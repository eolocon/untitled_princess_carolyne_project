from pyspark.sql.types import StructType, StructField, StringType, IntegerType

"""Module containing using defined dataframe schemas

	Todo:
		* maybe design a class for each different schema

"""

# prediction service input schema
type_field = StructField('document_type', StringType())
id_field = StructField('document_id', StringType())
parent_id = StructField('parent_document_id', StringType())
user_id_field = StructField('user_id', StringType())
user_name_field = StructField('username', StringType())
text_field = StructField('document_text', StringType())
time_field = StructField('document_time', StringType())
data_field = StructField('data', StructType([
												type_field, 
												id_field, 
												parent_id, 
												user_id_field, 
												user_name_field, 
												text_field, 
												time_field
											]
										))

prediction_input_schema = StructType([data_field])