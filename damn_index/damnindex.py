""""""

import logging
from elasticsearch import Elasticsearch

class DAMNIndex(object):
    """Class to launch queries against the DAMN's Elasticsearch index"""
    def __init__(self):
        self.log = logging.getLogger('DAMNIndex')
        
    def _serialize_file_reference(self, a_file_reference):
        return {
                    '_id': a_file_reference.file.hash,
                    "_type" : "FileReference",
                    'file__hash': a_file_reference.file.hash,
                    'file__filename': a_file_reference.file.filename,
                }
        
    def _serialize_asset_reference(self, a_file_reference, an_asset_reference):
        asset = an_asset_reference
        return {
                    '_id': str(asset.asset.file.hash)+str(asset.asset.subname)+str(asset.asset.mimetype),
                    "_type" : "AssetReference",
                    '_parent': a_file_reference.file.hash,
                    'asset__subname': asset.asset.subname,
                    'asset__mimetype': asset.asset.mimetype,
                    'asset__file__filename': asset.asset.file.filename,
                    'asset__file__hash': asset.asset.file.hash,
                    'metadata': [{'key': key} for key, meta in asset.metadata.items()] if asset.metadata else [],
                    'dependencies': [{'subname': dep.subname, 'mimetype': dep.mimetype, 'file__filename':dep.file.filename, 'file__hash': dep.file.hash} for dep in asset.dependencies] if asset.dependencies else [],
                }
        
    def serialize_to_documents(self, a_file_reference):
        """
        """
        yield self._serialize_file_reference(a_file_reference)
        if a_file_reference.assets:
            for an_asset_reference in a_file_reference.assets:
                yield self._serialize_asset_reference(a_file_reference, an_asset_reference)
