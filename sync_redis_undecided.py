import os
import redis
import tqdm
import argparse


REDIS_DB_UNDECIDED = 0
INDEXES = ["bbchallenge-undecided-index/bb5_undecided_index"]

r = redis.Redis()


def load_uint32_index_into_redis(src, db):
    r.select(db)
    r.flushdb()
    file_size = os.path.getsize(src)
    print("Index size", file_size // 4)
    with open(src, "rb") as f:
        for _ in tqdm.tqdm(range(0, file_size // 4)):
            b = f.read(4)
            machine_i = int.from_bytes(b, byteorder="big")
            r.set(machine_i, 1)


for db in [REDIS_DB_UNDECIDED]:
    print(f"Loading `{INDEXES[db]}` into REDIS...")
    load_uint32_index_into_redis("indexes/" + INDEXES[db], db)
