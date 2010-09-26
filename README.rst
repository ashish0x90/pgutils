
Utility scripts for PostgreSQL
______________________________

1. **Indexprofiling.py**

   It can be run against a db instance to quickly check 
   what all indexes are present but are *not getting used*,
   and where all creating indexes might be helpful.
   While, Managing indexes is more of an art, and one even might need 
   to know how to use explain analyze effectively and so on.
   This script may be helpful in giving you a head start.

   **Usage**
   Indexprofiling.py [options]: ::

      -h, --help            show this help message and exit
      -U USERNAME, --user=USERNAME
                        Username to connect to the database
      -D DBNAME, --database=DBNAME
                        Database name
      -H HOSTNAME, --hostname=HOSTNAME
                        Database hostname
      -P PORT, --port=PORT  Port number to connect to the database [Optional]


