#! /usr/bin/env python

import psycopg2
from csv import writer
from optparse import OptionParser
import getpass,sys

def getDBstats(username,dbname,hostname,port):
   
    password = getpass.getpass() #get password in a secure way from the user

    #Connect to the database, get db cursor
    conn = psycopg2.connect(database=dbname,host=hostname,user=username,password=password,port=port)
    cur =  conn.cursor()
    
    #Get all the user created schemas - and set search_path accordingly
    search_path_q = "select array_to_string(array(select schema_name::text from information_schema.schemata "\
        "where schema_owner != 'postgres'),',');"
    cur.execute(search_path_q)
    search_path = cur.fetchone()[0]

    cur.execute("set search_path to %s"%search_path) #set the search_path appropriately

    #Run queries to generate Index stats, not including unique indexes
    getIndexstats = '''SELECT idxstat.relname,
                       indexrelname,idxstat.idx_scan,
                       pg_size_pretty(pg_relation_size(idxstat.relname)), 
                       pg_size_pretty(pg_relation_size(indexrelname)),
                       n_tup_ins + n_tup_del + n_tup_upd as table_writes,
                       indexdef
                       FROM pg_stat_user_indexes AS idxstat JOIN pg_indexes ON indexrelname = indexname
                       JOIN pg_stat_user_tables ON idxstat.relname = pg_stat_user_tables.relname
                       WHERE indexdef !~* 'unique'
                       ORDER BY pg_relation_size(indexrelname) desc, table_writes desc;'''

    ##Write Index stats to a csv file
    cur.execute(getIndexstats)
    indexstats = cur.fetchall()
    cols = ['Table name','Index name','Times Used','Table size','Index size','Num writes','Index definition']
    indexstats.insert(0,cols) 
    f = open('index_stats.csv','w')
    w = writer(f)
    w.writerows(indexstats)
    f.close()


    #Run queries to generate Table stats
    getTablestats = '''select schemaname,relname,pg_size_pretty(pg_relation_size(relname)), 
                       seq_scan as number_of_seq_scans, seq_tup_read as number_of_rows_fetched_from_seq_scan, 
                       idx_scan as number_of_index_scan, idx_tup_fetch as number_of_tuples_fetched_by_idx, 
                       last_analyze, last_autoanalyze from pg_stat_user_tables order by 
                       number_of_rows_fetched_from_seq_scan desc,number_of_index_scan desc,
                       number_of_tuples_fetched_by_idx desc;'''

    cols = ['Schema name','Table name','Table size', 'Number of Seq scan', 'Number of rows fetched from seq scan',
            'Number of index scan','Number of Tuples Fetched by idx scan','last Analyzed','last Autoanalyzed']
    ##Write Table stats to a csv file
    cur.execute(getTablestats)
    tablestats = cur.fetchall()
    tablestats.insert(0,cols)
    f = open('table_stats.csv','w')
    w = writer(f)
    w.writerows(tablestats)
    f.close()




def parseCmdLine():
    '''
    Parses command line arguements and returns the parser
    '''
    parser = OptionParser()
    parser.add_option("-U", "--user", dest="username",
                  help="Username to connect to the database")
    parser.add_option("-D", "--database", dest="dbname",
                  help="Database name")
    parser.add_option("-H", "--hostname", dest="hostname",
                  help="Database hostname")
    parser.add_option("-P", "--port", dest="port", type="int", default=5432,
                  help="Port number to connect to the database [Optional]")
    return parser


if __name__=='__main__':
    parser = parseCmdLine()
    (options,args) = parser.parse_args()
    if not all([options.username,options.dbname,options.hostname,options.port]): #if any arg in empty,show usage and exit
        parser.print_help()
        sys.exit(1)

    getDBstats(options.username,options.dbname,options.hostname,options.port)
