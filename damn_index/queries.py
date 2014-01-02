#!/usr/bin/env python
from __future__ import print_function

import logging
from dateutil.parser import parse as parse_date

from elasticsearch import Elasticsearch

def print_hits(results, facet_masks={}):
    " Simple utility function to print results of a search query. "
    print('=' * 80)
    print('Total %d found in %dms' % (results['hits']['total'], results['took']))
    if results['hits']['hits']:
        print('-' * 80)
    for hit in results['hits']['hits']:
        print('/%s/%s/%s' % (hit['_index'], hit['_type'], hit['_id']))

    for facet, mask in facet_masks.items():
        print('-' * 80)
        for d in results['facets'][facet]['terms']:
            #print(mask % d)
            print(d)
    print('=' * 80)
    print()

# get trace logger and set level
tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
tracer.addHandler(logging.FileHandler('/tmp/es_trace.log'))
# instantiate es client, connects to localhost:9200 by default
es = Elasticsearch()


print_hits(es.search(index='damn'))

result = es.search(
    index='damn',
    doc_type='AssetReference',
    body={
        "query" : {
            "match_all" : {  }
        },
        "facets" : {
            "mimetype" : {
                "terms" : {
                    "field" : "asset__mimetype",
                    "size" : 10
                }
            }
        }
    }
)
print_hits(result, {'mimetype': ''})


result = es.search(
    index='damn',
    doc_type='AssetReference',
    body={
        "query" : {
            "match_all" : {  }
        },
        "facets" : {
            "metadata" : {
                "terms" : {
                    "field" : "metadata.key",
                    "size" : 10
                }
            }
        }
    }
)
print_hits(result, {'metadata': ''})





result = es.search(
    index='damn',
    doc_type='AssetReference',
    body={
        'query': {
        'filtered': {
          'filter': {
            'has_parent': {
                'type': 'FileReference',
                "query" : {
                "filtered": {
                  "query": { "match_all": {}},
                  "filter" : {"term": {  "file__hash": "90ca0b2230d6f9b486cd932e1ae1c28b780a2b0c"}}            
                  }
                }
              }
            }
          }
        }
    }
)
'''
result = es.search(
    index='damn',
    doc_type='AssetReference',
    body={
            "query" : {
            "filtered": {
              "query": { "match_all": {}},
              "filter" : {"term": {  "file__hash": "90ca0b2230d6f9b486cd932e1ae1c28b780a2b0c"}}            
              }
            }
          }
)
'''
print_hits(result)
