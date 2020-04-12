import pymysql

class Database:
    def connect(self):
        return pymysql.connect("mysqldb","cryptouser","123456","cryptodb" )
    
    def read(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        
        try:
            if id == None:
                cursor.execute("SELECT * FROM users order by id desc")
            else:
                cursor.execute("SELECT * FROM users where id = %s order by username asc", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self,data):
        con = Database.connect(self)
        cursor = con.cursor()
        
        try:
            cursor.execute("INSERT INTO users(username,password) VALUES (%s,%s)", (data['username'],data['password'],))
            con.commit()
            
            return True
        except:
            con.rollback()
            
            return False
        finally:
            con.close()
            
    def update(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()
        
        try:
            cursor.execute("UPDATE users set username = %s, password = %s where id = %s", (data['username'],data['password'],id,))
            con.commit()
            
            return True
        except:
            con.rollback()
            
            return False
        finally:
            con.close()
        
    def delete(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        
        try:
            cursor.execute("DELETE FROM users where id = %s", (id,))
            con.commit()
            
            return True
        except:
            con.rollback()
            
            return False
        finally:
            con.close()

    def update_settings(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE parameters set buy_size = %s, buy_timeout = %s, sell_timeout =%s, profit =%s, force_stop =%s, maxorders =%s, max_markets =%s, min_percent_chg =%s, max_percent_chg =%s, debug=%s, stop_bot =%s, api_key =%s, api_secret=%s  where id = %s",
                           (data['buy_size'], data['buy_timeout'], data['sell_timeout'], data['profit'], data['force_stop'], data['maxorders'], data['max_markets'], data['min_percent_chg'], data['max_percent_chg'], data['debug_mode'], data['stop_bot'], data['api_key'], data['api_secret'], id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def read_settings(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM parameters")
            else:
                cursor.execute("SELECT * FROM parameters where id = %s ", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()



    def read_orders(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM orders where active = 1")
            else:
                cursor.execute("SELECT * FROM orders where active = 1 and where id = %s ", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def read_corders(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM orders where active = 0")
            else:
                cursor.execute("SELECT * FROM orders where active = 0 and where id = %s ", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()


    def read_logs(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM logs order by log_id desc")
            else:
                cursor.execute("SELECT * FROM logs order by log_id desc where id = %s ", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def update_market(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute(
                "UPDATE markets set market = %s, enabled = %s, slow_market = %s, ai_active =%s, active =%s  where id = %s",
                (data['market'], data['enabled'], data['slow_market'], data['ai_active'], data['active'], id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()


    def read_markets(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM markets")
            else:
                cursor.execute("SELECT * FROM markets where id = %s ", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
          con.close()

    def delete_markets(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM markets where id = %s", (id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def insert_market(self, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO markets(market,enabled, slow_market, ai_active, active) VALUES (%s,%s,%s,%s,%s)", (data['market'], data['enabled'], data['slow_market'], data['ai_active'], data['active'],))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

