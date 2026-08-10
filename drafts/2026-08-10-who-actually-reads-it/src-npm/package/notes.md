# TODO
* parse date range
* allow the following to be configurable via cli
  * jsonTransform
  * tripleTransform
* better error handling
  * use pumpify
  * how to handle errors when pushing to an already existing transform stream [e.g. entry.on('error', err => outStream.destroy(err))]
* test w/ [ndjson-cli](https://github.com/mbostock/ndjson-cli)
  * in particular, does the default output (2 space indentation) work w/ newline-delimited json file parsing?
  * should indentation format be configurable
