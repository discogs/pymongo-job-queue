import pymongo
from datetime import datetime
import time


class JobQueue:

    def __init__(self, db, silent=False):
        """ Return an instance of a JobQueue.
        Initialization requires one argument, the database,
        since we use one jobqueue collection to cover all
        sites in an installation/database. The second 
        argument specifies if to print status while waiting
        for new job, the default value is False"""
        self.db = db
        self.silent=silent
        if not self._exists():
            print ('Creating jobqueue collection.')
            self._create()
        self.q = self.db['jobqueue']

    def _create(self, capped=True):
        """ Creates a Capped Collection. """
        # TODO - does the size parameter mean number of docs or bytesize?
        try:
            self.db.create_collection('jobqueue',
                                      capped=capped, max=100000,
                                      size=100000, autoIndexId=True)
        except:
            raise Exception('Collection "jobqueue" already created')

    def _exists(self):
        """ Ensures that the jobqueue collection exists in the DB. """
        return 'jobqueue' in self.db.collection_names()

    def valid(self):
        """ Checks to see if the jobqueue is a capped collection. """
        opts = self.db['jobqueue'].options()
        if opts.get('capped', False):
            return True
        return False

    def next(self):
        """ Runs the next job in the queue. """
        cursor = self.q.find({'status': 'waiting'},
                             tailable=True)
        if cursor:
            row = cursor.next()
            row['status'] = 'done'
            row['ts']['started'] = datetime.now()
            row['ts']['done'] = datetime.now()
            self.q.save(row)
            try:
                return row
            except:
                raise Exception('There are no jobs in the queue')

    def pub(self, data=None):
        """ Publishes a doc to the work queue. """
        doc = dict(
            ts={'created': datetime.now(),
                'started': datetime.now(),
                'done': datetime.now()},
            status='waiting',
            data=data)
        try:
            self.q.insert(doc, manipulate=False)
        except:
            raise Exception('could not add to queue')
        return True

    def __iter__(self):
        """ Iterates through all docs in the queue
            andw aits for new jobs when queue is empty. """
        cursor = self.q.find({'status': 'waiting'}, tailable=True)
        while 1:
            try:
                row = cursor.next()
                try:
                    result = self.q.update({'_id': row['_id'],
                                            'status': 'waiting'},
                                           {'$set': {
                                                'status': 'working',
                                                'ts.started': datetime.now()
                                                }
                                            })
                except OperationFailure:
                    print ('Job Failed!!')
                    continue
                print ('---')
                print ('Working on job:')
                yield row
                row['status'] = 'done'
                row['ts']['done'] = datetime.now()
                self.q.save(row)
            except:
                time.sleep(5)
                if not self.silent:
                    print ('waiting!')

    def queue_count(self):
        """ Returns the number of jobs waiting in the queue. """
        cursor = self.q.find({'status': 'waiting'})
        if cursor:
            return cursor.count()

    def clear_queue(self):
        """ Drops the queue collection. """
        self.q.drop()
