""""""

from __future__ import absolute_import
import logging
from elasticsearch import Elasticsearch

class DAMNIndex(object):
    """Class to launch queries against the DAMN's Elasticsearch index"""
    def __init__(self):
        self.log = logging.getLogger('DAMNIndex')
        
    def _serialize_file_description(self, file_descr):
        return {
                    '_id': file_descr.file.hash,
                    "_type" : "FileDescription",
                    'file__hash': file_descr.file.hash,
                    'file__filename': file_descr.file.filename,
                }
        
    def _serialize_asset_description(self, file_descr, asset_descr):
        asset = asset_descr
        return {
                    '_id': str(asset.asset.file.hash)+str(asset.asset.subname)+str(asset.asset.mimetype),
                    "_type" : "AssetDescription",
                    '_parent': file_descr.file.hash,
                    'asset__subname': asset.asset.subname,
                    'asset__mimetype': asset.asset.mimetype,
                    'asset__file__filename': asset.asset.file.filename,
                    'asset__file__hash': asset.asset.file.hash,
                    'metadata': [{'key': key} for key, meta in asset.metadata.items()] if asset.metadata else [],
                    'dependencies': [{'subname': dep.subname, 'mimetype': dep.mimetype, 'file__filename':dep.file.filename, 'file__hash': dep.file.hash} for dep in asset.dependencies] if asset.dependencies else [],
                }
        
    def serialize_to_documents(self, file_descr):
        """
        """
        yield self._serialize_file_description(file_descr)
        if file_descr.assets:
            for asset_descr in file_descr.assets:
                yield self._serialize_asset_description(file_descr, asset_descr)
