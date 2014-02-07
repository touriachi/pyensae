"""
@file
@brief Contains functions to import a text file into a database (SQLite).
"""

import os
from .database_main import Database

def import_flatfile_into_database (
                    filedb, 
                    filetext, 
                    table   = None, 
                    header  = True, 
                    columns = None,
                    engine  = 'SQLite', 
                    host    = 'localhost',
                    fLOG    = print) :
    """
    
    function which imports a file into a database.
    
    @param  filedb      something.db3
    @param  filetext    something.txt or .tsv
    @param  table       table name (in the database), if None, the database name will be the filename without extension
    @param  columns     if header is False, this must be specified. It should be a list of column names.
    @param  header      boolean (does it have a header or not)
    @param  engine      engine to use when using a SQL server (SQLite or ODBCMSSQL)
    @param  host        host (server)
    @param  fLOG        logging function (will display information through the command line)
    
    example:
    @code
    from pyensae import import_flatfile_into_database
    dbf = "database.db3"
    file = "textfile.txt"
    import_flatfile_into_database(dbf, file)
    @endcode
        
    """
    # connection
    db = Database (filedb, engine = engine, host = host, LOG = fLOG)
    db.connect ()
    
    if table == None :
        table = os.path.splitext(os.path.split(filetext)[-1])[0].replace(".","").replace(",","")
    
    if db.has_table (table) :
        fLOG ("remove ", table)
        db.remove_table (table)
        
    if header :
        db.import_table_from_flat_file (filetext, table, columns = None, header = header)
    else :
        db.import_table_from_flat_file (filetext, table, columns = columns, header = header)
    
    db.close ()        
