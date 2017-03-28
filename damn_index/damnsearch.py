"""
sudo /usr/share/elasticsearch/bin/plugin -install mobz/elasticsearch-head
http://localhost:9200/_plugin/head/
"""

from __future__ import absolute_import
import logging
from elasticsearch import Elasticsearch

class DAMNSearch(object):
    """Class to launch queries against the DAMN's Elasticsearch index"""
    def __init__(self):
        self.es = Elasticsearch()
        self.log = logging.getLogger('DAMNSearch')
        tracer = logging.getLogger('elasticsearch.trace')
        tracer.setLevel(logging.INFO)
        tracer.addHandler(logging.FileHandler('/tmp/es_trace.log'))
        
    def _search(self, doc_type, body):
        self.log.debug('Launching query with body %s '%str(body))
        results = self.es.search(
            index='damn',
            doc_type=doc_type,
            body=body
        )
        return results
    
    def _search_facets(self, doc_type, facets):    
        return self._search(doc_type,
            {
                "query" : {
                    "match_all" : {  }
                },
                "facets" : facets
            }
        )
    
    def get_mimetypes_with_count(self):
        results = self._search_facets('AssetDescription',
                        {
                            "mimetype" : {
                                "terms" : {
                                    "field" : "asset__mimetype"
                                }
                            }
                        })
        if results:
            ret = results.get('facets', {}).get('mimetype', {}).get('terms', {})
            return ret
        else:
            raise Exception('Failed to get_mimetypes_with_count')
        
