# coding: utf-8

"""
    kappa-logs

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.0.0
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from kappa_logs_client import schemas  # noqa: F401


class Logs(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "logs",
        }
        
        class properties:
            
            
            class logs(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['Log']:
                        return Log
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['Log'], typing.List['Log']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'logs':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'Log':
                    return super().__getitem__(i)
            __annotations__ = {
                "logs": logs,
            }
    
    logs: MetaOapg.properties.logs
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["logs"]) -> MetaOapg.properties.logs: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["logs", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["logs"]) -> MetaOapg.properties.logs: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["logs", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        logs: typing.Union[MetaOapg.properties.logs, list, tuple, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Logs':
        return super().__new__(
            cls,
            *_args,
            logs=logs,
            _configuration=_configuration,
            **kwargs,
        )

from kappa_logs_client.model.log import Log
