# pymongo-job-queue

A simple MongoDB based job queue for pymongo. Using [capped collections](http://docs.mongodb.org/manual/core/capped-collections/) and [tailable cursors](http://docs.mongodb.org/manual/tutorial/create-tailable-cursor/), you can queue up data to be consumed by a service worker.

#### Dependencies
* pymongo 2.7.2

### How It Works
Capped collections ensure that documents are accessed in the natural order they are inserted into the collection and tailable cursors give us a cursor that will stay open and wait for new documents to process if the job queue is empty, similar to using to the **tail** Unix command with the -f option.
The **JobQueue** class has a generator
#### Jobs
Jobs are added to the queue in the following structure:
```python
{
    'created': datetime,
    'started': datetime,
    'done': datetime,
    'status': 'string',
    'site': 'string',
    'data': {
        """ Add your job data here! Define whatever structure you want. """
    }
}
```
In the `data` dict the `JobQueue.pub` method will add whatever info your job needs. When running the job queue with a worker, the job queue will return a similar looking job that holds your specified data.


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

jobqueue.pub({'message': 'hello world!'}) # add a job to queue
for j in jobqueue:
    job = Job(j)
    job.execute()
```