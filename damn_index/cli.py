import sys
import argparse
import json
import copy

from damn_at.utilities import unique_asset_id_reference_from_fields

def transform_meta(metadata):
    ret = []
    for key, val in metadata.items():
        val['name'] = key
        ret.append(val)
    return ret
#pt a ../damn-test-files/mesh/blender/untitled.blend -f json-pretty | pt m | curl -XPOST --data-binary @- http://localhost:9200/damn/asset/_bulk
def transform(parser, subparsers):
    subparse = subparsers.add_parser(
            "m", #aliases=("transform",),
            help="Transform a given filedescription to a format usable for indexing",
            )
    parser.add_argument(
            'infile', nargs='?',
            type=argparse.FileType('r'),
            default=sys.stdin)
    def transform(args):
        data = args.infile.read()
        data = json.loads(data)
        file_hash = data["file"]["hash"]
        assets = []
        file_copy = copy.deepcopy(data)
        file_copy['metadata'] = transform_meta(file_copy.get('metadata', {}))
        del file_copy['assets']
        for asset in data['assets']:
            subname = asset['asset']['subname']
            mimetype = asset['asset']['mimetype']
            id = unique_asset_id_reference_from_fields(file_hash, subname, mimetype)
            a = {'id': id, 'file': file_copy}
            asset['metadata'] = transform_meta(asset.get('metadata', {}))
            a.update(asset)
            assets.append(a)
        for asset in assets:
            print json.dumps({'index': {'_id': asset['id']}})
            print json.dumps(asset)


    subparse.set_defaults(
            func=lambda args:
                transform(args),
            )
