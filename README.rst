
Utility scripts for PostgreSQL
______________________________

1. **Indexprofiling.py**

  It can be run against a db instance to quickly check what all indexes are present but are *not getting used*,
  and where all creating indexes might be helpful.
  While, Managing indexes is more of an art, and one even need to know how to use explain analyze effectively and so on.
  This script may be helpful in giving you a head start.

  Run as : python Indexprofiling.py -U <username> -D <database_name> -H <hostname> -P <port(optional)>
           enter password for the database user when prompted
           run python Indexprofiling.py -h for complete description of the options.


