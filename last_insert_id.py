"""
Purpose:

  Demonstrate manual method to obtain LAST_INSERT_ID() from MySQL server
  on a database e.g. when provided API (AVEVA/Indusoft) does not work
       with MySQL correctly and LAST_INSERT_ID() cannot be used

  Cf. https://www.plctalk.net/qanda/showthread.php?t=130178

Usage:

  python last_insert_id.py [row_value]

"""
import os
import sys
import pprint
import MySQLdb
from random import gauss

########################################################################
class FORTY2:
  """
Class to create, and add data to, the MySQL table, test_forty2.forty2,

  +------------+-------------+------+-----+---------+----------------+
  | Field      | Type        | Null | Key | Default | Extra          |
  +------------+-------------+------+-----+---------+----------------+
  | row_id     | int(11)     | NO   | PRI | NULL    | auto_increment |
  | forty2_col | varchar(64) | YES  |     | NULL    |                |
  +------------+-------------+------+-----+---------+----------------+

"""
  ######################################################################
  def last_insert_id(self,new_row_val):
    """Insert value, retrieve equivalent of LAST_INSERT_ID() manually"""

    ### Get the current date/time from MySQL, e.g.'2021-08-11 14:04:06'
    ### N.B. this has nothing to do with table test_forty2.forty2;
    ###      it only accesses the NOW() function of MySQL
    self.cu.execute("SELECT NOW()")
    guard = str(self.cu.fetchone()[0])

    ### ***TEMPORARILY*** insert that guard date/time string, as the
    ### value for column [forty2_col], of a new row
    self.cu.execute("INSERT INTO forty2 (forty2_col) VALUES (%s)"
                   ,(guard,)
                   )
    self.cu.execute("COMMIT")

    ### Get the LAST_INSERT_ID() from the current connection, to show
    ### the MySQL internal function does work for the current connection
    self.cu.execute("SELECT LAST_INSERT_ID()")
    last_insert_id = str(self.cu.fetchone()[0])

    ### Close the current connection, open a new connection
    self.close()
    self.connect()

    ### Get the LAST_INSERT_ID() again, to show that LAST_INSERT_ID()
    ### does ***NOT*** for the new connection
    self.cu.execute("SELECT LAST_INSERT_ID()")
    bad_last_insert_id = self.cu.fetchone()[0]

    ### SELECT the row inserted using the previous connection by looking
    ### for the guard date/time string, and extract the insert ID
    ### manually
    self.cu.execute("""
SELECT row_id
FROM forty2
WHERE forty2_col=%s
""",(guard,))

    manual_last_insert_id = self.cu.fetchone()[0]

    ### UPDATE the guard date/time string to the desired value, using
    ### the manually-obtained insert ID
    self.cu.execute("UPDATE forty2 SET forty2_col=%s WHERE row_id=%s"
                   ,(new_row_val,manual_last_insert_id,)
                   )
    self.cu.execute("COMMIT")

    ### Return the results
    return dict(bad_last_insert_id=bad_last_insert_id
               ,last_insert_id=last_insert_id
               ,manual_last_insert_id=manual_last_insert_id
               ,value_added=new_row_val
               )

  ######################################################################
  def __init__(self):
    """Class instantiation and initialization; do nothing"""
    pass

  ######################################################################
  def connect(self,secondpass=True):
    """
    1) Connect to MySQL database test_forty2;
    2) Ensure table test_forty2.forty2 exists

    N.B. The [unix_socket] argument is specific to the author's
         MariaDB/MySQL server configuration, and may not be required for
         others' setups

"""
    try:
      ### Make the connection; cf. the note about [unix_socket] above
      try:
        self.cn = MySQLdb.connect(db="test_forty2")
      except:
        self.cn = MySQLdb.connect(db="test_forty2",unix_socket="/var/run/mysqld/mysqld.sock")

      ### Instantiate a cursor to the database to make queries
      self.cu = self.cn.cursor()

      ### Create the table if it does not yet exist
      self.cu.execute("""
CREATE TABLE IF NOT EXISTS forty2
( row_id      INTEGER      PRIMARY KEY AUTO_INCREMENT
, forty2_col  VARCHAR(64)  DEFAULT NULL
)
;
""")

      if not secondpass: self.msg = None

    except:

      ### If code gets to here, the a possible reason is that the
      ### database [test_forty2] does not yet exist, so try to create it

      ### Avoid recursive loop
      if secondpass: raise

      ### Connect to MySQL server but with no database
      try:
        cn = MySQLdb.connect(db="")
      except:
        cn = MySQLdb.connect(db="",unix_socket="/var/run/mysqld/mysqld.sock")

      ### Instantiate a cursor, CREATE database, store creation meassge,
      ### delete cursor, close connection, make recursive call to make
      ### the intended connection for this method
      cu = cn.cursor()
      cu.execute("CREATE DATABASE test_forty2")
      self.msg = "Created database test_forty2"
      del cu
      cn.close()
      self.connect()

    return

  ######################################################################
  def close(self):
    """Delete the cursor and close the connection"""

    try   : del self.cu
    except: pass
    try   : self.cn.close()
    except: pass

    return

########################################################################
if "__main__" == __name__:

  print()

  ### Instantiate the class, then connect to the database
  forty2 = FORTY2()
  forty2.connect(secondpass=False)

  ### Output any non-null message from the above
  if not (None is forty2.msg): print(forty2.msg)

  ### Build an argument if one was not supplied on the command line
  new_row_val = sys.argv[1:] and sys.argv[1] or str(gauss(0,1))[:5]

  ### Call the .last_insert_id method of the FORTY2 class instance,
  ### then close the connection
  result = forty2.last_insert_id(new_row_val)
  forty2.close()

  ### Output the results
  pprint.pprint(result)
  print()

########################################################################
