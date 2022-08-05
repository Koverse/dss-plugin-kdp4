# This file is the actual code for the custom Python dataset Koverse KDP Import Dataset
import operator

import pandas as pd
from dataiku.connector import Connector
from kdp_connector import KdpConn
from auth_utils import get_jwt

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='kdp-dataiku-connector plugin %(levelname)s - %(message)s')


class MyConnector(Connector):

    def __init__(self, config):
        Connector.__init__(self, config)
        self.dataset_id = config.get("dataset_id")
        self.dataset_name = config.get("dataset_name")
        self.batch_size = config.get("batch_size")
        self.starting_record_id = ''  # Not needed for writing a dataset, but required to read a dataset (for preview)
        self.use_existing_dataset = config.get("use_existing_dataset")
        self.api_configuration_preset = config.get("api_configuration_preset")

        if self.api_configuration_preset is None or self.api_configuration_preset == {}:
            raise ValueError("Please specify an API configuration preset")

        api_url = self.api_configuration_preset.get("kdp_url")
        path_to_ca_file = self.api_configuration_preset.get("path_to_ca_file")

        logger.info('kdp-dataset api_url: %s' % str(api_url))
        logger.info('kdp-dataset path_to_ca_file: %s' % str(path_to_ca_file))

        self.kdp_conn = KdpConn(path_to_ca_file=path_to_ca_file,
                                host=api_url)

    def get_writer(self, dataset_schema=None, dataset_partitioning=None, partition_id=None):
        """
        Returns a writer object to write in the dataset (or in a partition).
        The dataset_schema given here will match the the rows given to the writer below.
        Note: the writer is responsible for clearing the partition, if relevant.
        """
        logger.info('Kdp-Dataset:get_writer')

        writer_config = {
            "kdp_connector_instance": self.kdp_conn,
            "workspace_id": self.api_configuration_preset.get("workspace_id"),
            "dataset_id": self.dataset_id,
            "dataset_name": self.dataset_name,  # for create only
            "use_existing_dataset": self.use_existing_dataset,
            "batch_size": self.batch_size,
            "api_configuration_preset": self.api_configuration_preset
        }
        return KdpWriter(writer_config, dataset_schema, dataset_partitioning, partition_id)

    def get_read_schema(self):
        return None

    def generate_rows(self, dataset_schema=None, dataset_partitioning=None,
                      partition_id=None, records_limit = -1):

        jwt = get_jwt(self.config.get('api_configuration_preset'), self.kdp_conn, logger)

        if self.dataset_id is None or operator.not_(self.use_existing_dataset):
            raise ValueError("Cannot read from KDP using kdp-dataset connector, "
                             "when creating a new dataset; or if an existing dataset_id is not provided. "
                             "Check 'use_existing_dataset' and update dataset_id field in settings for this dataset.")

        dictionary_list = self.kdp_conn.read_dataset_to_dictionary_list(self.dataset_id,
                                                                        jwt,
                                                                        self.starting_record_id,
                                                                        self.batch_size)

        data_generator = (item for item in dictionary_list)

        return data_generator


class KdpWriter(object):
    def __init__(self, config, dataset_schema, dataset_partitioning, partition_id):
        self.dataset_schema = dataset_schema
        self.dataset_partitioning = dataset_partitioning
        self.partition_id = partition_id
        self.kdp_conn = config.get('kdp_connector_instance')
        self.config = config
        self.row_buffer = []

        logger.info("KdpWriter: writer_config workspace_id=%s, dataset_id=%s, batch_size=%s",
                    self.config.get('workspace_id'), self.config.get('dataset_id'), self.config.get('batch_size'))

    def write_row(self, row):
        obj = {}

        # We generate the "regular" row with the content of the row
        for (col, val) in zip(self.dataset_schema["columns"], row):
            obj[col["name"]] = val

        self.row_buffer.append(obj)

    def close(self):
        if len(self.row_buffer) > 0:
            df = pd.DataFrame.from_records(self.row_buffer)

            jwt = get_jwt(self.config.get('api_configuration_preset'), self.kdp_conn, logger)

            logger.info("use_existing_dataset: %s", self.config.get('use_existing_dataset'))

            dataset_id = self.config.get('dataset_id')
            #  if use_existing_dataset is false: create new dataset
            if operator.not_(self.config.get('use_existing_dataset')):

                if self.config.get('dataset_name') is None or self.config.get('dataset_name') == '':
                    raise ValueError("Dataset name is required to create new KDP dataset")

                new_dataset = self.kdp_conn.create_dataset(name=self.config.get('dataset_name'),
                                                           workspace_id=self.config.get('workspace_id'),
                                                           jwt=jwt)

                logger.info("Created new KDP dataset with name: %s, and dataset_id: %s", new_dataset.name,
                            new_dataset.id)

                dataset_id = new_dataset.id

            logger.info("Writing to KDP dataset with dataset_id: %s ", dataset_id)

            partitions_set = self.kdp_conn.batch_write(dataframe=df,
                                                  dataset_id=dataset_id,
                                                  jwt=jwt,
                                                  batch_size=self.config.get('batch_size'))
            logger.info("Export to Kdp dataset completed with partitions %s", partitions_set)
        logger.info("Write to Kdp completed")
