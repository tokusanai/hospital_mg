import os, psycopg2, string, random, hashlib
# DBへのコネクションを生成

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    cherset = string.ascii_letters + string.digits
    
    salt = ''.join(random.choices(cherset, k=30))
    return salt

def get_hash(pw,salt):
    b_pw = bytes(pw, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_pw = hashlib.pbkdf2_hmac('sha256',b_pw, b_salt, 1200).hex()
    return hashed_pw

def insert_user(name,gender,birthday,mail,pw):
    sql = 'INSERT INTO hp_users VALUES(default,%s, %s, %s, %s, %s, %s )'
    
    salt = get_salt()
    hashed_pw = get_hash(pw, salt)
    try:
        connection = get_connection()
        cursor = connection.cursor()
        Strbirthday = str(birthday)
        print(hashed_pw)
        print(salt)
        cursor.execute(sql, (name, gender,Strbirthday,mail,hashed_pw,salt))
        count = cursor.rowcount #更新件数を表示
        connection.commit()
        
    except psycopg2.DatabaseError :
        count = 0
        
    finally :
        cursor.close()
        connection.close()
        
    return count
    
def login(mail, pw):
    sql = 'SELECT hashpw, salt FROM hp_users WHERE email = %s'
    flg = False
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(mail,))
        user = cursor.fetchone()
        
        if user != None:
            salt = user[1]
            
            hashpw = get_hash(pw,salt)
            
            if hashpw == user[0]:
                flg = True
    except psycopg2.DatabaseError:
        flg = False
    finally :
        cursor.close()
        connection.close()
        
    return flg    

def select_user(mail):
    sql = 'SELECT user_id, name FROM hp_users WHERE email = %s'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (mail,))
        user = cursor.fetchone()

        if user is not None:
            user_id = user[0]
            name = user[1]
            return user_id, name
        else:
            return None, None

    except psycopg2.DatabaseError:
        return None, None

    finally:
        cursor.close()
        connection.close()

def register_reserve(user_id,name,year,manth,day,time,symptoms, remarks):
    sql = 'INSERT INTO  hp_reserve  VALUES(default, %s, %s, %s, %s, %s, %s, %s, %s)'
    try : # 例外処理
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_id,name,year,manth,day,time,symptoms,remarks))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()
        
    except psycopg2.DatabaseError: # Java でいうcatch 失敗した時の処理をここに書く
        count = 0 # 例外が発生したら0 をreturn する。
        
    finally: # 成功しようが、失敗しようが、close する。
        cursor.close()
        connection.close()
        
    return count

