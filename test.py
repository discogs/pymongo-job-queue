from pymongo import MongoClient
from jobqueue import JobQueue
import unittest

host = 'localhost'
port = 27017
pair = '%s:%d' % (host, port)


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
        self.assertRaises(Exception, jq.next)
        job = {'message': 'hello world!'}
        jq.pub('test', job)
        self.assertTrue(jq.pub('test', job))
