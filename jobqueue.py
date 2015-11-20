from pymongo.cursor import _QUERY_OPTIONS
import pymongo
from datetime import datetime
import bson
import time

class JobQueue:

    def __init__(self, db):
        """ Return an instance of a JobQueue.
        Initialization requires one argument, the database,
        since we use one jobqueue collection to cover all
        sites in an installation/database. """
        self.db = db
        if not self.exists():
            print ('Creating jobqueue collection.')
            self.create()
        self.q = self.db['jobqueue']

    def create(self):
        """ Creates a Capped Collection. """
        # TODO - does the size parameter mean number of docs or bytesize?
        try:
            self.db.create_collection('jobqueue', 
                                      capped=True, max=100000, 
                                      size=100000, autoIndexId=True)
        except:
            print ('Collection "jobqueue" already created')

    def exists(self):
        """ Ensures that the jobqueue exists in the DB. """
        return 'jobqueue' in self.db.collection_names()

    def valid(self):
        """ Checks to see if the jobqueue is a capped collection. """
        opts = self.db['jobqueue'].options()
        if opts.get('capped', False):
            return True
        return False

    def next(self):
        """ Runs the next job in the queue. """
        cursor = self.q.find({'status':'waiting'},
                              tailable=True)
        if cursor:
            row = cursor.next()
            row['status'] = 'working'
            row['ts']['started'] = datetime.now()
            self.q.save(row)
            job = Job(row)

            try:
                job.execute()
            except:
                raise Exception('There are no jobs in the queue')

            row['status'] = 'done'
            row['ts']['done'] =  datetime.now()
            self.q.save(row)


    def pub(self, channel, data=None):
        """ Publishes a doc to the work queue.
        All jobs should conform to this spec:
            {
                'created': datetime,
                'started': datetime,
                'done': datetime,
                'status': 'string',
                'data': {
                    '_id': ObjectId,    # ObjectId of the document to fetch
                    'op': 'string',     # method to call on the document
                    'parms': 'string'   # parameters to pass to the op
                }
            }
        """
        doc = dict(
            ts = {'created': datetime.now(), 'started': datetime.now(), 'done':datetime.now()},
            status = 'waiting',
            channel = channel,
            data=data)
        print doc
        try:
            self.q.insert(doc, manipulate=False)
        except:
            raise Exception('could not add to queue')
        return True

    def __iter__(self):
        cursor = self.q.find({'status':'waiting'},
                              tailable=True)

        while 1:
            try:
                row = cursor.next()
                try:
                    result = self.q.update({'_id': row['_id'] ,'status':'waiting'},
                                                    {'$set':{'status':'working',
                                                    'ts.started':datetime.now()}} )
                    print result
                except OperationFailure:
                    print 'Failed!!!!'
                    continue


                print '---'
                print 'I got work'
                print row

                job = Job(row)
                yield job

                row['status'] = 'done'
                row['ts']['done'] =  datetime.now()
                self.q.save(row)

            except:
                time.sleep(5)
                print 'waiting!'


class Job(object):

    def __init__ (self, job_data):
        self.job_data = job_data

    def execute(self):
        """ Returns the job's message. """
        print self.job_data
        print '!!!!!!!!'
        return self.job_data['data']['message']