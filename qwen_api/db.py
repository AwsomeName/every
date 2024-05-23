import pymysql
import sys
import os
import logging
import json

format = "%Y-%m-%d"
run_env = os.getenv("EVERY_ENV")
logging.basicConfig(filename="sql.log", level=logging.DEBUG)

class EVR_DB():
    def __init__(
        self,
    ) -> None:
        if run_env == "dev":
            self.conn = pymysql.connect(
                host="127.0.0.1",
                port=3306,
                user="lc",
                password="abc12345",
                database="every",
                charset="utf8"
            )
        elif run_env == "online":
            self.conn = pymysql.connect(
                host="127.0.0.1",
                port=3306,
                user="lc",
                password="abc12345",
                database="every",
                charset="utf8"
            )
            
    def create_user(self, user_phone_num, user_name_uni, user_img_url=""):
        sql = "insert into users_base_infos \
    (is_del, u_id_uni, u_phone_num, u_name_uni, u_img_url, if_login) \
    values(%r, %s, %s, %s, %s, %r);"
        data = []
        data.append(0)
        u_id_uni = ""
        try:
            # check_sql = "SELECT count(*) FROM users_base_infos;"
            check_sql = "SELECT count(*) FROM users_base_infos;"
            with self.conn.cursor() as cursor:
                row = cursor.execute(check_sql)
                print("row:", row)
                res = cursor.fetchone()[0]
                print("midres:", res)
                u_id_uni = str(100100101 + int(res))
                print('u_id_uni:', u_id_uni)
            # res = self.conn.commit()
            # print("res:", res)
        except:
            return {"msg": "failed", "err": "retry later..."} 
        data.append(u_id_uni)
        # 电话号码需要额外的检查，用来确保一个电话号码一个
        data.append(user_phone_num)
        data.append(user_name_uni)
        data.append(user_img_url)
        data.append(1)
        
        try:
            with self.conn.cursor() as cursor:
                row = cursor.execute(sql, data)
            self.conn.commit()

        except pymysql.MySQLError as err:
            self.conn.rollback()
            # print(type(err), err)
            log_str = "insert failed " + ",".join([str(d) for d in data])
            logging.info(log_str)
            # logging.debug(log_str)
            return {"msg": "failed", "err": "same_name"}

        return {"msg": "suc", "err": ""}
    
    def delete_user(self, user_id):
        sql = "UPDATE users_base_infos SET is_del=0 WHERE u_id_uni=" + user_id
        try:
            with self.conn.cursor() as cursor:
                row = cursor.execute(sql)
                print("row:", row)
        except:
            return {"msg": "failed", "err": "retry later..."} 
        
        return {"msg": "suc", "err": "see u later"}
    
    def user_login(self, user_id):
        sql = "UPDATE users_base_infos SET if_login=1 WHERE u_id_uni=" + user_id
        try:
            with self.conn.cursor() as cursor:
                row = cursor.execute(sql)
                print("row:", row)
        except:
            return {"msg": "failed", "err": "retry later..."} 
        
        return {"msg": "suc", "err": ""}
    
    def user_logout(self, user_id):
        sql = "UPDATE users_base_infos SET if_login=0 WHERE u_id_uni=" + user_id
        try:
            with self.conn.cursor() as cursor:
                row = cursor.execute(sql)
                print("row:", row)
        except:
            return {"msg": "failed", "err": "retry later..."} 
        
        return {"msg": "suc", "err": "see u later"} 
    
    
    def check_last_chat(self, user_id):
        check_sql = "SELECT * FROM user_aichat_history_v01 WHERE u_id_uni=" + user_id + " ORDER by create_time desc LIMIT 5"
        try:
            with self.conn.cursor() as cursor:
                rows = cursor.execute(check_sql)
                print("row:", rows)
                res = cursor.fetchall()
                return {"msg": "suc", "err": "", "infos": res}
        except:
            return {"msg": "failed", "err": "retry later..."} 
    
    def add_chat_histroy(self, user_id, img_path, chat_content):
        sql = "insert into user_aichat_history_v01 \
            (u_id_uni, u_img_path, u_chat_history) \
            values(%s, %s, %s);"
        data = []
        data.append(user_id)
        data.append(img_path)
        data.append(chat_content)
        try:
            with self.conn.cursor() as cursor:
                rows = cursor.execute(sql, data)
            self.conn.commit()

        except pymysql.MySQLError as err:
            self.conn.rollback()
            # print(type(err), err)
            log_str = "insert failed " + ",".join([str(d) for d in data])
            logging.info(log_str)
            # logging.debug(log_str)
            return {"msg": "failed", "err": "add err"}

        return {"msg": "suc", "err": ""}

    
    def delete_chat_history(self):
        # 定时删除历史对话
        pass
    
    def check_user(self):
        check_sql = "SELECT * FROM users_base_infos"
        # try:
        if True:
            with self.conn.cursor() as cursor:
                rows = cursor.execute(check_sql)
                print("row:", rows)
                res = cursor.fetchall()
                print("res:", res)
                for r in res:
                    print(r)
                return {"msg": "suc", "err": "", "infos": json.dumps(rows)}

    def check_history(self):
        check_sql = "SELECT * FROM user_aichat_history_v01"
        # try:
        if True:
            with self.conn.cursor() as cursor:
                rows = cursor.execute(check_sql)
                print("row:", rows)
                res = cursor.fetchall()
                print("res:", res)
                for r in res:
                    print(r)
                return {"msg": "suc", "err": "", "infos": json.dumps(rows)}
            

if __name__ == "__main__":
    db = EVR_DB()
    print(db.check_user())
    print("------")
    print(db.create_user("17611180092", "test11"))
    print(db.create_user("17611180092", "test2"))
    print(db.create_user("17611180092", "test3"))
    print(db.create_user("17611180092", "test4"))
    print("------")
    print(db.delete_user('100100105'))
    print(db.user_login('100100101'))
    print(db.user_logout('100100101'))
    print("------")
    print(db.check_history())
    chat = {"role": "user", "content": "你好"}
    print(db.add_chat_histroy("100100101", img_path = "", chat_content = json.dumps(chat)))
    print(db.check_last_chat("100100101"))
    