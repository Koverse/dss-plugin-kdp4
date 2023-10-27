import kdp_api
import logging
from kdp_api.api import audit_log_api
from kdp_api.model.audit_log_paginator import AuditLogPaginator
from kdp_api.configuration import Configuration


class AuditLogApi(object):
    def __init__(self, configuration: Configuration=None):
        self.configuration = configuration


    def post_audit_log_query(self, config, dataset_id: str, expression: str, limit: int = 5, offset: int = 0) -> AuditLogPaginator:
        """This method will be used to query data in KDP datasets using the lucene syntax

            :param Configuration config: Connection configuration
            :param str dataset_id: audit log dataset id
            :param str expression: Lucene style query expression ex. name: John
            :param int limit: max number of results in the response.
            :param int offset: how many records to skip before returning first record.
            :returns: AuditLogPaginator object which contains audit log records matching query expression

            :rtype: AuditLogPaginator
        """
        logging.info(f'function parameters - dataset_id: %s, expression: %s, limit: %s, offset: %s' % (dataset_id, expression, limit, offset))
        with kdp_api.ApiClient(config) as api_client:
            api_instance = audit_log_api.AuditLogApi(api_client)
            query = {}
            query['datasetId'] = dataset_id
            query['expression'] = expression
            query['limit'] = limit
            query['offset'] = offset

            return api_instance.post_audit_log_query(lucene_query_request=query)

