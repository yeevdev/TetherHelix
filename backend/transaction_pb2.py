# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: backend/transaction.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'backend/transaction.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19\x62\x61\x63kend/transaction.proto\x12\x10tetherhelix_grpc\"\x1f\n\rMarketRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\"R\n\x0eMarketResponse\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\r\n\x05price\x18\x02 \x01(\x01\x12\x0e\n\x06volume\x18\x03 \x01(\x01\x12\x11\n\ttimestamp\x18\x04 \x01(\t2h\n\x0bTransaction\x12Y\n\x10StreamMarketData\x12\x1f.tetherhelix_grpc.MarketRequest\x1a .tetherhelix_grpc.MarketResponse\"\x00\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'backend.transaction_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_MARKETREQUEST']._serialized_start=47
  _globals['_MARKETREQUEST']._serialized_end=78
  _globals['_MARKETRESPONSE']._serialized_start=80
  _globals['_MARKETRESPONSE']._serialized_end=162
  _globals['_TRANSACTION']._serialized_start=164
  _globals['_TRANSACTION']._serialized_end=268
# @@protoc_insertion_point(module_scope)
