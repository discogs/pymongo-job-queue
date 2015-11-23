from pymongo import MongoClient
from jobqueue import JobQueue
import unittest

host = 'localhost'
port = 27017
pair = '%s:%d' % (host, port)

class Job(object):

    def __init__ (self, job_data):
        self.job_data = job_data

    def execute(self):
        """ Returns the job's message.  """
        return (self.job_data['data']['message'])


class TestJobQueue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        client = MongoClient(host, port)
        cls.db = client.pymongo_test
      

    def test_init(self):
        jq = JobQueue(self.db)
        self.assertTrue(jq.valid())

    def test_publish(self):
        jq = JobQueue(self.db)
        job = {'message': 'hello world!'}
        jq.pub('test', job)
        self.assertTrue(jq.pub('test', job))

    def test_next(self):
        jq = JobQueue(self.db)
        job = {'message': 'hello world!'}
        row = jq.next()
        for data in row:
            job = Job(data)
            result = job.execute()
            self.assertEquals(result, 'hello world!')

    def test_iter(self):
        jq = JobQueue(self.db)
        for job in jq:
            if job:
                self.assertTrue(True, "Found job")
                return
        self.assertEquals(False, "No jobs found!")


if __name__ == '__main__':
    unittest.main()