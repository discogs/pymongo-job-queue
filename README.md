# pymongo-jobqueue
work in progress

Simple MongoDB based job queue using pymongo.

#### Dependencies
* pymongo 2.7.2


#### Jobs
Jobs are added to the queue in the following structure:
```
{
    'created': datetime,
    'started': datetime,
    'done': datetime,
    'status': 'string',
    'site': 'string',
    'data': {
    # define your own data structure
    }
}
```
In the `data` dict you will add whatever info your job needs. When running this job queue with a worker, you will supply a custom Job class that will know what to do with this data.


### Useage
```python
from pymongo import MongoClient
from jobqueue import JobQueue

class Job(object):

    def __init__ (self, job_data):
        self.job_data = job_data

    def execute(self):
        """ Returns the job's message.  """
        print self.job_data
        print (self.job_data['data']['message'])

client = MongoClient('localhost', 27017)
db = client.job_queue
jobqueue = JobQueue(db)
if not jobqueue.valid():
    print ('jobqueue is not configured correctly!')
    sys.exit(1)

jobqueue.pub('test', {'message': 'hello world!'} ) # add a job
for j in jobqueue:
    job = Job(j)
    job.execute()
```