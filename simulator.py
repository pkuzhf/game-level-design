import sqlite3
import requests
import json

MAX_SIMULATE=3
MAX_TURN=60

class cache(object):

    """
    valueFunc(function) : calculate the value of a given game result
    """
    def __init__(self, valueFunc):
        self.url="http://162.105.98.7:15233/api/53933a415dcbc5f837707b74/9148008697/admin_runmatch"
        self.gameName="Tank"
        self.DATABASE_URI="data/data.db"
        self.valueFunc=valueFunc
        conn=sqlite3.connect(self.DATABASE_URI)
        cursor=conn.cursor()
        try:
            conn.execute('''CREATE TABLE IF NOT EXISTS SITUTATION(PLAYER0 TEXT,
                PLAYER1 TEXT,INITDATA TEXT,COUNTER INT,TOTAL REAL)''')
        except:
            print("Create table failed...")
        conn.close()

    '''Send get requests'''
    def __get(self,player0,player1,initData):
        headers={
        'x-game':self.gameName,
        'x-player-0':player0,
        'x-player-1':player1,
        'x-initData':str({"field":initData,"maxTurn":MAX_TURN})
        }
        flag=True
        while flag:
            try:
                result=requests.get(self.url,headers=headers)
                result.raise_for_status()
            except Exception as e:
                print(e)
                print(str(headers)+" try again!")
                print("===============================================")
            else:
                flag=False
        
        return result

    """
    player=(player0,player1)
    player0(string) : ID of the first player
    player1(string) : ID of the second player
    initData(list)  : A list with three elements
    """
    def run(self,player,initData):
        conn=sqlite3.connect(self.DATABASE_URI)
        cursor=conn.cursor()
        player0,player1=player
        sql="SELECT COUNTER,TOTAL FROM SITUTATION WHERE PLAYER0='%s'\
            AND PLAYER1='%s' AND INITDATA='%s'"\
            %(player0,player1,str(initData))
        cursor.execute(sql)
        result=cursor.fetchone()
        if(result==None):
            sql="INSERT INTO SITUTATION(PLAYER0,PLAYER1,\
                INITDATA,COUNTER,TOTAL)\
                VALUES('%s','%s','%s',%d,%f)"\
                %(player0,player1,str(initData),0,0.0)
            cursor.execute(sql)
            conn.commit()
            counter,total=0,0
        else:
            counter,total=result[0],result[1]
        if counter<MAX_SIMULATE:
            result=self.__get(player0,player1,initData)
            cur=self.valueFunc(result)
            counter+=1
            total+=cur
            sql="UPDATE SITUTATION SET COUNTER=%d,TOTAL=%f WHERE PLAYER0='%s'\
                AND PLAYER1='%s' AND INITDATA='%s'"\
                %(counter,total,player0,player1,str(initData))
            cursor.execute(sql)
            conn.commit()
        conn.close()
        return total/counter,counter,total

















