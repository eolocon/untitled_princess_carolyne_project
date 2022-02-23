from runners import SimpleRunner
import os

""" Configures the service and istantiates it using a runner """


targets = os.getenv('TARGETS', default='')
cookies = os.getenv('COOKIES')
host = os.getenv('INGESTOR_HOST')
port = os.getenv('TCP_PORT')

runner = SimpleRunner(host, port)
runner.run(targets,cookies)


