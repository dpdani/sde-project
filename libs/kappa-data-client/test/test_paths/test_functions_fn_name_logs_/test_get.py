# coding: utf-8

"""


    Generated by: https://openapi-generator.tech
"""

import unittest
from unittest.mock import patch

import urllib3

import kappa_data_client
from kappa_data_client.paths.functions_fn_name_logs_ import get  # noqa: E501
from kappa_data_client import configuration, schemas, api_client

from .. import ApiTestMixin


class TestFunctionsFnNameLogs(ApiTestMixin, unittest.TestCase):
    """
    FunctionsFnNameLogs unit test stubs
        Get Function Logs  # noqa: E501
    """
    _configuration = configuration.Configuration()

    def setUp(self):
        used_api_client = api_client.ApiClient(configuration=self._configuration)
        self.api = get.ApiForget(api_client=used_api_client)  # noqa: E501

    def tearDown(self):
        pass

    response_status = 200




if __name__ == '__main__':
    unittest.main()
