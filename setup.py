from distutils.core import setup
setup(
  name = 'pymjq',
  packages = ['pymjq'], # this must be the same as the name above
  version = '1.0.1',
  description = 'Simple MongoDB based job queue',
  author = 'Andy Craze',
  author_email = 'acraze@discogsinc.com',
  url = 'https://github.com/discogs/pymongo-job-queue', # use the URL to the github repo
  download_url = 'https://github.com/discogs/pymongo-job-queue/tarball/1.0.0',
  keywords = ['queue', 'pymongo', 'mongodb', 'job', 'async', 'worker', 'tail'], # arbitrary keywords
  classifiers = [],
)
