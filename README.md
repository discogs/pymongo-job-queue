# pymongo-jobqueue
work in progress

Simple MongoDB based job queue using pymongo.

#### Dependencies
* pymongo 2.7.2


#### Jobs
All jobs should conform to this spec:
```
{
    'created': datetime,
    'started': datetime,
    'done': datetime,
    'status': 'string',
    'site': 'string',
    'data': {
        '_id': ObjectId,    # ObjectId of the document to fetch
        'op': 'string',     # method to call on the document
        'parms': 'string'   # parameters to pass to the op
    }
}
```


### Useage

```
>>> from pymongo import MongoClient
>>> from jobqueue import JobQueue
>>> client = MongoClient('localhost', 27017)
>>> db = client.job_queue
>>> jq = JobQueue(db)
Creating jobqueue collection.

>>> jq.valid()
True
```