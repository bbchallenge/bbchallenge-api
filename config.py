SESSION_COOKIE_NAME = "bbchallenge_backend"
SESSION_COOKIE_SAMESITE = "LAX"
SESSION_COOKIE_HTTPONLY = True

# bbchallenge db files
DB_PATH = "all_5_states_undecided_machines_with_global_header"  # seed DB
DB_SIZE = 88664064  # nb machines in seed DB
DB_PATH_DECIDED = "indexes/bb5_decided_indexes"  # decided index files
DB_PATH_UNDECIDED = "indexes/bbchallenge-undecided-index/bb5_undecided_index"  # undecided index file
