import importlib
# Have to use import_module, due to dashes in directory names, required for dataiku connector to work
connector = importlib.import_module("python-connectors.kdp-import-dataset.connector")

########################################################################################################
#  You can run the connector code outside of DSS using this script.
#  It does require some modification to connector.py to work, as the Dataiku.Connector is only available
#  internally for the DSS app.
#  Comment out references to the Dataiku Connector in connector.py like this...
#
#   # from dataiku.connector import Connector
#     from kdp_connector import KdpConn
#
#
#   # class MyConnector(Connector):
#     class MyConnector:
#
#      def __init__(self, config):
#   #      Connector.__init__(self, config)
#
#  With these modifications the script will work to test the connector, outside of DSS.
#
########################################################################################################

# Provide the required parameters below for testing
PATH_TO_CA_FILE = '${PATH_TO_CA_FILE}'
EMAIL = '${EMAIL}'
PASSWORD = '${PASSWORD}'
WORKSPACE_ID = '${WORKSPACE_ID}'
DATASET_ID = '${DATASET_ID}'
STARTING_RECORD_ID = ''
BATCH_SIZE = 100000

config = {
    'path_to_ca_file': PATH_TO_CA_FILE,
    'email': EMAIL,
    'password': PASSWORD,
    'workspace_id': WORKSPACE_ID,
    'dataset_id': DATASET_ID,
    'starting_record_id': STARTING_RECORD_ID,
    'batch_size': BATCH_SIZE
}

my_connector = connector.MyConnector(config=config)

generator = my_connector.generate_rows()

print(next(generator))




