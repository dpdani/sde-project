# coding: utf-8

"""
    kappa-fn-code

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.0.0
    Generated by: https://openapi-generator.tech
"""

from kappa_fn_code_client.paths.code_code_id_.post import CreateCode
from kappa_fn_code_client.paths.code_code_id_.delete import DeleteCode
from kappa_fn_code_client.paths.code_code_id_.get import GetCode
from kappa_fn_code_client.paths.code_.get import GetCodeIds


class DefaultApi(
    CreateCode,
    DeleteCode,
    GetCode,
    GetCodeIds,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
