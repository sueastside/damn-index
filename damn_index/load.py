#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
delete everything

curl -XDELETE 'http://localhost:9200/damn/'
"""



from __future__ import absolute_import
import os
from os.path import dirname, basename, abspath
from itertools import chain
from datetime import datetime
import logging

from damn_at import MetaDataStore

from damn_index import DAMNIndex

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
        'subname': {"type": "multi_field",
                    "fields": {
                        "subname": {"type": "string", "index": "analyzed"},
                        "subname_raw": {"type": "string", "index": "not_analyzed", 'store': True}
                    }},
        'mimetype': {'type': 'string', 'index': 'not_analyzed', 'store': True},
        'file__hash': {'type': 'string', 'index': 'not_analyzed', 'store': True},
        'file__filename': {'type': 'string', 'analyzer': 'file_path'}
    }

    client.indices.put_mapping(
        index=index,
        doc_type='FileDescription',
        body={
            'FileDescription': {
                "_id": {
                    "path": "file__hash"
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
        doc_type='AssetDescription',
        body={
            'AssetDescription': {
                '_parent': {
                    'type': 'FileDescription'
                },
                'properties': {
                    'asset__subname': {
                        "type": "multi_field",
                        "fields": {
                            "asset__subname": {"type": "string",
                                               "index": "analyzed",
                                               'store': True},
                            "asset__subname_raw": {"type": "string",
                                                   "index": "not_analyzed",
                                                   'store': True}
                            }
                    },
                    'asset__mimetype': {'type': 'string',
                                        'index': 'not_analyzed',
                                        'store': True},
                    'asset__file__filename': {'type': 'string',
                                              'analyzer': 'file_path',
                                              'store': True},
                    'asset__file__hash': {'type': 'string',
                                          'index': 'not_analyzed',
                                          'store': True},
                    "metadata": {
                        "type": "nested", "store": "yes",
                        "index": "analyzed", "omit_norms": "true",
                        "include_in_parent": True,
                        "properties": {
                            "key": {"type": "string"},
                            "value": {"type": "string"},  # TODO: make multi_field
                            "type": {"type": "string"}
                            }
                    },
                    "dependencies": {
                        "type": "nested", "store": "yes",
                        "index": "analyzed", "omit_norms": "true",
                        "include_in_parent": True,
                        'properties': AssetId,
                    },
                }
            }
        }
    )


def parse_file_descriptions(path):
    """
    """
    import yaml
    import json
    store = MetaDataStore()
    indexer = DAMNIndex()
    dump = open('/tmp/play.txt', 'wb')
    for filename in os.listdir(path):
        print('=' * 80)
        print(filename)
        file_descr = store.get_metadata(path, filename)
        print(json.dumps(file_descr, indent=4))
        # print(file_descr)
        for document in indexer.serialize_to_documents(file_descr):
            print(document)
            dump.write(yaml.dump(document))
            dump.write('\n---\n')
            yield document


def parse_store(client, path='/tmp/damn', index='damn'):
    """
    """
    path = dirname(dirname(abspath(__file__))) if path is None else path
    repo_name = basename(path)

    create_store_index(client, index)

    for ok, result in streaming_bulk(
            client,
            parse_file_descriptions(path),
            index=index,
            chunk_size=50  # keep the batch sizes small for appearances only
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
