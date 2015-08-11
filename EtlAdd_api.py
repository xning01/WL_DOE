__author__ = 'ken201507'
# -*- coding: utf-8 -*-

import MySQLdb
from pub_util import *
import os


class etl_add_api(object):
    def __init__(self, conf_path):
        self.hostip = read_ini_value(conf_path, 'dbconfig', 'hostip')
        self.user = read_ini_value(conf_path, 'dbconfig', 'dbuser')
        self.passwd = read_ini_value(conf_path, 'dbconfig', 'passwd')
        self.dbname = read_ini_value(conf_path, 'dbconfig', 'dbname')
        self.port = read_ini_value(conf_path, 'dbconfig', 'port')
        self.charset = read_ini_value(conf_path, 'dbconfig', 'charset')

    def conn(self):
        '''
        :return:初始化连接，从INI中获取连接参数返回连接对象
        '''
        try:
            conn = MySQLdb.connect(host=self.hostip, user=self.user,
                                   passwd=self.passwd, db=self.dbname,
                                   port=int(self.port), charset=self.charset)
            conn.ping(True)
            return conn
        except MySQLdb.Error, e:
            error_msg = 'Error %d: %s' % (e.args[0], e.args[1])
            print error_msg

    def get_host_version(self):
        '''
        从远程数据库中返回系统当前的操作系统和
        :return:
        '''
        conn = self.conn()
        try:
            cus = conn.cursor()
            cus.execute("SELECT VERSION()")
            row = cus.fetchone()
            if row is not None:
                return row[0]
            else:
                return 'fail to connect '
                # Log.Info_Log('abc')
        except MySQLdb.Error, e:
            cus.rollback()
            error_msg = 'Error %d: %s' % (e.args[0], e.args[1])
            # Log.Error_Log(error_msg)

    def reconnectDB(self, *args, **kwargs):
        '''
        重连接数据库，
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            pass
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cur = self.connect_mysql().cursor()
            # print 'reconnect fail'

    def disconnect(self):
        '''
        :return:断开数据库
        '''
        conn = self.conn()
        conn.close()

    def insert_sql_cmd(self, sql_cmd):
        '''
        插数据
        :param sql_cmd:
        :return:
        '''
        try:
            conn = self.conn()
            cur = conn.cursor()
            cur.execute(sql_cmd)
            conn.commit()
            cur.close()
            return True
        except Exception, e:
            print "[MYSQL ERROR] : %s" % sql_cmd
            print "%s" % (str(e))
            cur.close()
            return False

    def update_sql_cmd(self, sql_cmd):
        '''
        更新数据
        :param sql_cmd:
        :return:
        '''
        try:
            conn = self.conn()
            cur = conn.cursor()
            cur.execute(sql_cmd)
            conn.commit()
            cur.close()
            return True
        except Exception, e:
            print "[MYSQL ERROR] : %s" % sql_cmd
            print "%s" % (str(e))
            cur.close()
            return False

    def query_sql_cmd(self, sql_cmd):
        '''
        查询数据
        :param sql_cmd:
        :return:
        '''
        try:
            conn = self.conn()
            cur = conn.cursor()
            cur.execute(sql_cmd)
            res = cur.fetchall()
            cur.close()
            return res
        except Exception, e:
            print "[MYSQL ERROR] : %s" % sql_cmd
            print "%s" % (str(e))
            return False

    def usr_spend_time_on_each_ques(self, usr_id):
        '''becasue requirement ,static some return below 20150723'''
        target_dir = "./result/"
        if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
        save_file_name = target_dir+str(datetime.now().strftime('%Y%m%d%H%M%S'))\
            + ' ' + self.usr_spend_time_on_each_ques.__name__+'.kol'
        try:
            conn = self.conn()
            cur = conn.cursor()
            cur.execute("select userID,questionID,spend_on_question \
                        from ETL_etl_question where userID=%d" % (usr_id))
            res = cur.fetchall()
            cur.close()
            f = open(save_file_name, 'w')
            f.write("user_id  questionid  spend_on_question" + '\n')
            for i in res:
                listtmp = []
                for k in i:
                    if isinstance(k, datetime):
                        k = str(k)
                    elif isinstance(k, long):
                        k = str(k)
                    elif isinstance(k, float):
                        k = str(k)
                    else:
                        pass
                    listtmp.append(k)
                    strtmp = str(listtmp)
                f.write(strtmp.strip(strtmp[0]).strip(strtmp[-1])+'\n')
                # f.write(i)
            f.close()
            write_log('etl', 'usr_spend_time_on_each_ques OK', 'message')
        except Exception, e:
            write_log('etl', 'usr_spend_time_on_each_ques fail' + str(e),
                      'error')

    def usr_timestamp_on_each_ques(self, usr_id):
        target_dir = "./result/"
        if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
        save_file_name = target_dir + \
            str(datetime.now().strftime('%Y%m%d%H%M%S')) \
            + ' ' + self.usr_timestamp_on_each_ques.__name__ + '.kol'
        try:
            conn = self.conn()
            cur = conn.cursor()
            cur.execute("select userID,questionID,start_datetime \
                        from ETL_etl_question where userID=%d" % (usr_id))
            res = cur.fetchall()
            cur.close()
            f = open(save_file_name, 'w')

            f.write("userid  questionid  timestamp " + '\n')
            for i in res:
                listtmp = []
                for k in i:
                    if isinstance(k, datetime):
                        k = str(k)
                    elif isinstance(k, long):
                        k = str(k)
                    elif isinstance(k, float):
                        k = str(k)
                    else:
                        pass
                    listtmp.append(k)
                    strtmp = str(listtmp)
                f.write(strtmp.strip(strtmp[0]).strip(strtmp[-1]) + '\n')
                # f.write(i)
            f.close()
            write_log('etl', 'usr_timestamp_on_each_ques OK', 'message')
        except Exception, e:
            write_log('etl', 'usr_timestamp_on_each_ques fail' + str(e),
                      'error')

    def usr_timestamp_on_pass_subject(self, usr_id):
        '''
        how ?
        '''
        pass

    def usr_correct_or_wrong_count(self, usr_id, isright=1):
        target_dir = "./result/"
        if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
        save_file_name = target_dir + \
            str(datetime.now().strftime('%Y%m%d%H%M%S')) + \
            ' ' + self.usr_correct_or_wrong_count.__name__ + '.kol'
        try:
            conn = self.conn()
            cur = conn.cursor()
            if isright == 1:
                cur.execute("select userID,questionID,start_datetime,\
                            is_true from ETL_etl_question where userID=%d \
                            and is_true=1" % (usr_id))
            elif isright == 0:
                cur.execute("select userID,questionID,start_datetime,\
                            is_true from ETL_etl_question where userID=%d \
                            and is_true=0" % (usr_id))
            res = cur.fetchall()
            cur.close()
            f = open(save_file_name, 'w')

            f.write("userid  questionid  timestamp is_true" + '\n')
            for i in res:
                listtmp = []
                for k in i:
                    if isinstance(k, datetime):
                        k = str(k)
                    elif isinstance(k, long):
                        k = str(k)
                    elif isinstance(k, float):
                        k = str(k)
                    else:
                        pass
                    listtmp.append(k)
                    strtmp = str(listtmp)
                f.write(strtmp.strip(strtmp[0]).strip(strtmp[-1])+'\n')
                # f.write(i)
            f.close()
            if isright == 1:
                write_log('etl', 'usr_correct_or_wrong_count (par:is_true=1)',
                          'message')
            elif isright == 0:
                write_log('etl', 'usr_correct_or_wrong_count (par:is_true=0)',
                          'message')
        except Exception, e:
            write_log('etl', 'usr_correct_or_wrong_count fail' + str(e),
                      'error')

    def usr_level_try(self, usr_id):
        target_dir = "./result/"
        if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
        save_file_name = target_dir + \
            str(datetime.now().strftime('%Y%m%d%H%M%S')) + ' ' \
            + self.usr_level_try.__name__+'.kol'
        try:
            conn = self.conn()
            cur = conn.cursor()
            cur.execute("select userID,engry_point,count(engry_point) \
                        from ETL_etl_question where userID=%d \
                        group by engry_point" % (usr_id))
            res = cur.fetchall()
            cur.close()
            f = open(save_file_name, 'w')

            f.write("userID  engry_point  try_times " + '\n')
            for i in res:
                listtmp = []
                for k in i:
                    if isinstance(k, datetime):
                        k = str(k)
                    elif isinstance(k, long):
                        k = str(k)
                    elif isinstance(k, float):
                        k = str(k)
                    else:
                        pass
                    listtmp.append(k)
                    strtmp = str(listtmp)
                f.write(strtmp.strip(strtmp[0]).strip(strtmp[-1]) + '\n')
                # f.write(i)
            f.close()
            write_log('etl', 'usr_level_try OK', 'message')
        except Exception, e:
            write_log('etl', 'usr_level_try fail' + str(e), 'error')

    def usr_test_subject_include(self, usr_id):
        target_dir = "./result/"
        if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
        save_file_name=target_dir+str(datetime.now().strftime('%Y%m%d%H%M%S'))+' '+self.usr_test_subject_include.__name__+'.kol'
        try:
            conn=self.conn()
            cur=conn.cursor()
            cur.execute("select userID,subjectID from ETL_etl_user where userID=%d" %(usr_id))
            res=cur.fetchall()
            cur.close()
            f = open(save_file_name, 'w')

            f.write("userID  subjectID  "+'\n' )
            for i in res:
                listtmp=[]
                for k in i:
                    # print type(k)
                    if isinstance(k,datetime):
                        k=str(k)
                    elif isinstance(k,long):
                        k=str(k)
                    elif isinstance(k,float):
                        k=str(k)
                    elif isinstance(k,unicode):
                        k=str(k)
                    else:
                        pass
                    listtmp.append(k)
                    strtmp=str(listtmp)
                f.write(strtmp.strip(strtmp[0]).strip(strtmp[-1])+'\n')
                # f.write(i)
            f.close()
            write_log('etl','usr_test_subject_include OK','message')
        except Exception, e:
            write_log('etl','usr_test_subject_include fail' + str(e),'error')


#use recommendation system

    def usr_accuracy_of_test_subject(self,usr_id):
        target_dir = "./result/"
        if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
        save_file_name=target_dir+str(datetime.now().strftime('%Y%m%d%H%M%S'))+' '+self.usr_accuracy_of_test_subject.__name__+'.kol'
        try:
            conn=self.conn()
            cur=conn.cursor()
            cur.execute("select count(*) from ETL_etl_question where userID=%d and is_true=1" %(usr_id))
            res_right=cur.fetchall()
            cur.execute("select count(*) from ETL_etl_question where userID=%d and is_true=0" %(usr_id))
            res_wrong=cur.fetchall()
            cur.close()
            f = open(save_file_name, 'w')
            f.write("userID  ques_answer_total right wrong percentage  "+'\n' )

            for i in res_right:
                for k in i:
                    # print type(k)
                    right_count=k
            for ii in res_wrong:
                for kk in ii:
                    wrong_count=kk
            ques_answer_total=right_count+wrong_count
            # print float(right_count)/float(ques_answer_total)
            f.write(str(usr_id)+'  '+str(ques_answer_total)+'  '+str(right_count)+'  '+str(wrong_count)+'  '+str(float(right_count)/float(ques_answer_total))+'\n')
            f.close()
            write_log('etl','usr_accuracy_of_test_subject OK','message')
        except Exception, e:
            write_log('etl','usr_accuracy_of_test_subject fail' + str(e),'error')

    def usr_complete_seq_ques(self,usr_id):
        target_dir = "./result/"
        if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
        save_file_name=target_dir+str(datetime.now().strftime('%Y%m%d%H%M%S'))+' '+self.usr_complete_seq_ques.__name__+'.kol'
        try:
            conn=self.conn()
            cur=conn.cursor()
            cur.execute("select userID,questionID,start_datetime from ETL_etl_question where userID=%d" %(usr_id))
            res=cur.fetchall()
            cur.close()
            f = open(save_file_name, 'w')

            f.write("userid  questionid  timestamp "+'\n' )
            for i in res:
                listtmp=[]
                for k in i:
                    if isinstance(k,datetime):
                        k=str(k)
                    elif isinstance(k,long):
                        k=str(k)
                    elif isinstance(k,float):
                        k=str(k)
                    else:
                        pass
                    listtmp.append(k)
                    strtmp=str(listtmp)
                f.write(strtmp.strip(strtmp[0]).strip(strtmp[-1])+'\n')
                # f.write(i)
            f.close()
            write_log('etl','usr_complete_seq_ques OK','message')
        except Exception, e:
            write_log('etl','usr_complete_seq_ques fail' + str(e),'error')

    def ques_be_answer(self,ques_id):
        target_dir = "./result/"
        if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
        save_file_name=target_dir+str(datetime.now().strftime('%Y%m%d%H%M%S'))+' '+self.ques_be_answer.__name__+'.kol'
        try:
            conn=self.conn()
            cur=conn.cursor()
            cur.execute("select questionID,count(*) from ETL_etl_question where questionID=%d" %(ques_id))
            res=cur.fetchall()
            cur.close()
            f = open(save_file_name, 'w')

            f.write("question_id  question_be_answer_times "+'\n' )
            for i in res:
                for k in i:
                    pass
            f.write(str(ques_id)+'  '+str(k)+'\n')
            f.close()
            write_log('etl','ques_be_answer OK','message')
        except Exception, e:
            write_log('etl','ques_be_answer fail' + str(e),'error')

    def ques_be_answer_correct(self,ques_id):
        target_dir = "./result/"
        if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
        save_file_name=target_dir+str(datetime.now().strftime('%Y%m%d%H%M%S'))+' '+self.ques_be_answer_correct.__name__+'.kol'
        try:
            conn=self.conn()
            cur=conn.cursor()
            cur.execute("select questionID,engry_point,count(*) from ETL_etl_question where questionID=%d and is_true=1" %(ques_id))
            res=cur.fetchall()
            cur.close()

            f = open(save_file_name, 'w')
            f.write("question_id  level answer_correct_times "+'\n' )

            for i in res:
                tmplist=[]
                for k in i:
                    if isinstance(k,long):
                        k=str(k)
                    elif isinstance(k,float):
                        k=str(k)
                    tmplist.append(k)
                    strtmp=str(tmplist)
                f.write(strtmp.strip(strtmp[0]).strip(strtmp[-1])+'\n')
            write_log('etl','ques_be_answer_correct OK','message')
        except Exception, e:
            write_log('etl','ques_be_answer_correct fail' + str(e),'error')

    def ques_be_answer_lasting(self,ques_id):
        target_dir = "./result/"
        if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
        save_file_name=target_dir+str(datetime.now().strftime('%Y%m%d%H%M%S'))+' '+self.ques_be_answer_lasting.__name__+'.kol'
        try:
            conn=self.conn()
            cur=conn.cursor()
            cur.execute("select questionID,spend_on_question from ETL_etl_question where questionID=%d" %(ques_id))
            res=cur.fetchall()
            cur.close()

            f = open(save_file_name, 'w')
            f.write("question_id  spend_on_question "+'\n' )

            for i in res:
                listtmp=[]
                for k in i:
                    if isinstance(k,datetime):
                        k=str(k)
                    elif isinstance(k,long):
                        k=str(k)
                    elif isinstance(k,float):
                        k=str(k)
                    else:
                        pass
                    listtmp.append(k)
                    strtmp=str(listtmp)
                f.write(strtmp.strip(strtmp[0]).strip(strtmp[-1])+'\n')
            write_log('etl','ques_be_answer_lasting OK','message')
        except Exception, e:
            write_log('etl','ques_be_answer_lasting fail' + str(e),'error')

    def get_ques_by_level(self, ques_level):
        '''
        :param ques_id: level 1、2、3、4  4:hardest
        :return: list(ques_id)
        '''
        target_dir = "./result/"
        if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
        save_file_name = target_dir + \
            str(datetime.now().strftime('%Y%m%d%H%M%S')) + ' ' + \
            self.get_ques_by_level.__name__+'.kol'
        try:
            conn = self.conn()
            cur = conn.cursor()
            cur.execute("select questionID from ETL_question \
                        where engry_point=%d" % (ques_level))
            res = cur.fetchall()
            cur.close()

            f = open(save_file_name, 'w')
            f.write("get level %d list:" % (ques_level) + '\n')

            llresult = []

            for i in res:
                for k in i:
                    if isinstance(k, long):
                        k = int(k)
                        llresult.append(k)
                    else:
                        pass

            return llresult
            # debug
            # f.write(str(llresult)+'\n')
            # write_log('etl', 'get_ques_by_level OK', 'message')
        except Exception, e:
            write_log('etl', 'get_ques_by_level fail' + str(e), 'error')

    def get_usr_last_ques_restult(self, usr_id):
        '''
        :param usr_id: usr_ID
        :return: 1=true,0=false
        '''
        target_dir = "./result/"
        if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
        save_file_name=target_dir+str(datetime.now().strftime('%Y%m%d%H%M%S'))+' '+self.get_usr_last_ques_restult.__name__+'.kol'
        try:
            conn=self.conn()
            cur=conn.cursor()
            cur.execute("select questionID,is_true from ETL_etl_question where userID=%d" %(usr_id))
            res=cur.fetchall()
            cur.close()

            f = open(save_file_name, 'w')
            f.write("user: %d latest result:"%(usr_id)+'\n' )

            res=res[-1]
            print res[0],res[1]

            f.write(str(res[0])+' '+str(res[1])+'\n')
            f.close()
            write_log('etl','get_usr_last_ques_restult OK','message')
        except Exception, e:
            write_log('etl','get_usr_last_ques_restult fail' + str(e),'error')

    def get_subject_by_ques(self, ques_id):
        '''
        :param ques_id: ques_id
        :return:
        '''
        # target_dir = "./result/"
        # if not os.path.isdir(target_dir):
        #        os.makedirs(target_dir)
        # save_file_name = target_dir + \
        #    str(datetime.now().strftime('%Y%m%d%H%M%S')) + ' ' + \
        #    self.get_subject_by_ques.__name__+'.kol'
        try:
            conn = self.conn()
            cur = conn.cursor()
            cur.execute("select testing_centre from ETL_question \
                        where questionID=%d" % (ques_id))
            res = cur.fetchall()
            cur.close()

            res = res[0][0]
            res = res.split(';')
            for i in range(len(res)):
                res[i] = int(res[i])

            return res
            # print "Q " + str(ques_id) + " : " + str(res)

            # f = open(save_file_name, 'w')
            # f.write("ques: %d test_sbujectID:" % (ques_id) + '\n')
            # f.write(str(res[0]) + '\n')
            # f.close()
            # write_log('etl', 'get_subject_by_ques OK', 'message')
        except Exception, e:
            write_log('etl', 'get_subject_by_ques fail' + str(e), 'error')
            return None


if __name__ == "__main__":
    cc = etl_add_api('./config.ini')
    print cc.get_host_version()

    ll = cc.get_ques_by_level(1)
    ll = ll + cc.get_ques_by_level(2)
    ll = ll + cc.get_ques_by_level(3)
    ll = ll + cc.get_ques_by_level(4)

    ll.sort()
    # for i in range(165):
    #     cc.get_subject_by_ques(i)
    cc.get_subject_by_ques(3)
    # cc.get_usr_last_ques_restult(1000)
    # cc.get_subject_by_ques(150)
