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
        client.pymongo_test.jobqueue.drop()
        cls.db = client.pymongo_test

    def tearDown(self):
        self.db['jobqueue'].drop()

    def test_init(self):
        jq = JobQueue(self.db)
        self.assertTrue(jq.valid())
        self.assertRaises(Exception, jq._create)
        jq.clear_queue()

    def test_valid(self):
        jq = JobQueue(self.db)
        jq.db['jobqueue'].drop()
        jq._create(capped=False)
        self.assertFalse(jq.valid())
        self.assertRaises(Exception, jq._create)
        jq.clear_queue()

    def test_publish(self):
        jq = JobQueue(self.db)
        job = {'message': 'hello world!'}
        jq.pub(job)
        self.assertEquals(jq.queue_count(), 1)
        jq.clear_queue()
        jq.q = None  # erase the queue
        self.assertRaises(Exception, jq.pub, job)

    def test_next(self):
        jq = JobQueue(self.db)
        self.assertRaises(Exception, jq.next)
        job = {'message': 'hello world!'}
        jq.pub(job)
        row = jq.next()
        self.assertEquals(row['data']['message'], 'hello world!')
        jq.clear_queue()

    # def test_iter(self):
    #     jq = JobQueue(self.db)
    #     job = {'message': 'hello world!'}
    #     jq.pub(job)
    #     for job in jq:
    #         if job:
    #             self.assertTrue(True, "Found job")
    #             jq.clear_queue()
    #             return
    #     self.assertEquals(False, "No jobs found!")
    #     jq.clear_queue()


if __name__ == '__main__':
    unittest.main()
