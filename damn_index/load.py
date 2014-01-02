#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
delete everything

curl -XDELETE 'http://localhost:9200/damn/'
'''

from __future__ import print_function

import os
from os.path import dirname, basename, abspath
from itertools import chain
from datetime import datetime
import logging

from damn_at import MetaDataStore

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, streaming_bulk

def create_store_index(client, index):
    # create empty index
    client.indices.create(
        index=index,
        body={
          'settings': {
            # just one shard, no replicas for testing
            'number_of_shards': 1,
            'number_of_replicas': 0,

            # custom analyzer for analyzing file paths
            'analysis': {
              'analyzer': {
                'file_path': {
                  'type': 'custom',
                  'tokenizer': 'path_hierarchy',
                  'filter': ['lowercase']
                }
              }
            }
          }
        },
        # ignore already existing index
        ignore=400
    )

    AssetId = {
        'subname': {"type" : "multi_field",
                    "fields" : {
                        "subname" : {"type" : "string", "index" : "analyzed"},
                        "subname_raw" : {"type" : "string", "index" : "not_analyzed", 'store': True}
                    }},
        'mimetype': {'type': 'string', 'index' : 'not_analyzed', 'store': True},
        'file__hash': {'type': 'string', 'index' : 'not_analyzed', 'store': True},
        'file__filename': {'type': 'string', 'analyzer': 'file_path'}
    }
    
    client.indices.put_mapping(
        index=index,
        doc_type='FileReference',
        body={
          'FileReference': {
            "_id" : {
                "path" : "file__hash"
            },
            'properties': {
              'file__hash': {'type': 'string', 'index' : 'not_analyzed', 'store': True},
              'file__filename': {'type': 'string', 'analyzer': 'file_path', 'store': True}
            }
          }
        }
    )
    
    client.indices.put_mapping(
        index=index,
        doc_type='AssetReference',
        body={
          'AssetReference': {
            '_parent': {
              'type': 'FileReference'
            },
            'properties': {
              'asset__subname': {"type" : "multi_field",
                "fields" : {
                    "asset__subname" : {"type" : "string", "index" : "analyzed", 'store': True},
                    "asset__subname_raw" : {"type" : "string", "index" : "not_analyzed", 'store': True}
                    }},
              'asset__mimetype': {'type': 'string', 'index' : 'not_analyzed', 'store': True},
              'asset__file__filename': {'type': 'string', 'analyzer': 'file_path', 'store': True},
              'asset__file__hash': {'type': 'string', 'index' : 'not_analyzed', 'store': True},
              "metadata" : {
                "type" : "nested", "store" : "yes", "index" : "analyzed", "omit_norms" : "true", "include_in_parent":True,
                "properties" : {
                        "key" : {"type" : "string"},
                        "value" : {"type" : "string"}, #TODO: make multi_field
                        "type" : {"type" : "string"}
                    }
                },
                "dependencies" : {
                    "type" : "nested", "store" : "yes", "index" : "analyzed", "omit_norms" : "true", "include_in_parent":True,
                    'properties': AssetId,
                },
            }
          }
        }
    )


def parse_file_references(path):
    """
    """
    store = MetaDataStore()
    for filename in os.listdir(path):
        print('=' * 80)
        print(filename) 
        metadata = store.get_metadata(path, filename)
        print(metadata)
        yield {
            '_id': metadata.file.hash,
            "_type" : "FileReference",
            'file__hash': metadata.file.hash,
            'file__filename': metadata.file.filename,
        }
        if metadata.assets:
            for asset in metadata.assets:
                print(asset.asset.subname, asset.asset.mimetype, asset.asset.file.filename)
                yield {
                    '_id': str(asset.asset.file.hash)+str(asset.asset.subname)+str(asset.asset.mimetype),
                    "_type" : "AssetReference",
                    '_parent': metadata.file.hash,
                    'asset__subname': asset.asset.subname,
                    'asset__mimetype': asset.asset.mimetype,
                    'asset__file__filename': asset.asset.file.filename,
                    'asset__file__hash': asset.asset.file.hash,
                    'metadata': [{'key': key} for key, meta in asset.metadata.items()] if asset.metadata else [],
                    'dependencies': [{'subname': dep.subname, 'mimetype': dep.mimetype, 'file__filename':dep.file.filename, 'file__hash': dep.file.hash} for dep in asset.dependencies] if asset.dependencies else [],
                }


def parse_store(client, path='/tmp/damn', index='damn'):
    """
    """
    path = dirname(dirname(abspath(__file__))) if path is None else path
    repo_name = basename(path)

    create_store_index(client, index)

    for ok, result in streaming_bulk(
            client,
            parse_file_references(path),
            index=index,
            chunk_size=50 # keep the batch sizes small for appearances only
        ):
        action, result = result.popitem()
        doc_id = '/%s/%s/%s' % (index, result['_type'], result['_id'])
        # process the information from ES whether the document has been
        # successfully indexed
        if not ok:
            print('Failed to %s document %s: %r' % (action, doc_id, result))
        else:
            print(doc_id)


if __name__ == '__main__':
    # get trace logger and set level
    tracer = logging.getLogger('elasticsearch.trace')
    tracer.setLevel(logging.INFO)
    tracer.addHandler(logging.FileHandler('/tmp/es_trace.log'))

    # instantiate es client, connects to localhost:9200 by default
    es = Elasticsearch()

    # we load the repo and all commits
    parse_store(es)

    # refresh to make the documents available for search
    es.indices.refresh(index='damn')

    # and now we can count the documents
    print(es.count(index='damn')['count'], 'documents in index')

