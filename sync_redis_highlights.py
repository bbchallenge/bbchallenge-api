import os
import redis
import tqdm
import argparse


REDIS_DB_HIGHLITS = 2


r = redis.Redis()

r.select(REDIS_DB_HIGHLITS)
r.flushdb()

highlighted_machines = [
    "BB(5) champion: 47,176,870-halter;mAQACAQEDAQADAQACAQAEAAEFAQEBAQEEAQAGAAEB&s=10000&w=250&ox=0.8&status=halt",
    "40,899-halter;mAQACAAEDAAADAAAAAQAEAAAFAQEFAAABAAEBAAEF&s=40899&w=500&ox=0.93&status=halt",
    "20,739-halter;mAQACAAEBAAADAQAEAQEDAQEBAQABAQAFAAAAAAAC&s=20739&w=250&ox=0.93&status=halt",
    "7410754&s=10000&w=300&ox=0.5",
    "55897188&s=10000&w=300&ox=0.5",
    "43374927&s=10000&w=300&ox=0.65",
    "27879939&s=10000&w=300&ox=0.5",
    "62537065&s=10000&w=300&ox=0.2",
    "2713328&s=10000&w=300&ox=0.5",
    '"chaotic" in [Marxen and Buntrock, 1990];76708232&s=10000&w=300&ox=0.3',
    '"complex counter" in [Marxen and Buntrock, 1990];10936909&s=5000&w=150&ox=0.5',

]

for h in highlighted_machines:
    r.rpush("highlighted", h)
