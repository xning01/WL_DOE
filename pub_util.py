__author__ = 'ken201507'
# #-*- encoding:utf8 -*-
import os
from datetime import datetime
import urllib
import httplib
import json
import ConfigParser
import os
import time
import re

'''
the globals:
BASE_DIR：pub_util路径
log_fun_dir：各函数日志文件夹
log_etl_dir：etl运行结果日志文件
'''
now = datetime.now()
BASE_DIR=os.path.dirname(__file__)
log_fun_dir=BASE_DIR+'/log_fun/'
log_etl_dir=BASE_DIR+'/log_etl/'

def makebracket_with_par(fn):
    '''
    内容装饰器
    :param fn:内容装信息
    :return:
    '''
    def wrapped(message_type):
        return "["+fn(message_type)+"]"
    return wrapped

def makebracket_no_par(fn):
    '''
    内容装饰器
    :param fn:内容
    :return:
    '''
    def wrapped():
        return "["+fn()+"]"
    return wrapped

@makebracket_no_par
def timenow():
    '''
    :return:返回格式为[2015-07-20 14:52:18]一类的字符串日期格式
    '''
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@makebracket_with_par
def message_status(message_type):
    '''
    :param message_type:信息内容
    :return:返回[abort],[message],一类的字符串格式
    '''
    return message_type

def log_message_format(*args):
    '''
    :param messagestatus:消息类型，可以自定义，如warning,log,等
    :param logmessage:日志信息
    :return:返回”[2015-07-20 14:52:18] [message]“一类的字符串格式
    '''
    if args[0]=='':
        temp_arg='log'
        return timenow()+' '+message_status(temp_arg)+' '+args[1] + "\n"
    else:
        return timenow()+' '+message_status(args[0])+' '+args[1] + "\n"


def post_con(parmas,headers,con_domain,port,timeout,url):
    '''
    :param parmas:参数，字典形式，如{'username':'kentest','password':'kentest'}
    :param headers:字典，如：{"Content-type": "application/x-www-form-urlencoded" , "Accept": "text/plain"}
    :param con_domain:字符串，如“192.168.1.29”
    :param port:端口integer,如8000
    :param timeout:超时integer 如30
    :param url:访问的URL，字符串，如"/zh-cn/phone_message/phone_register/"
    :return:返回字符串
    # json_data=post_con({'username':'kentest','password':'kentest'},
    #                {"Content-type": "application/x-www-form-urlencoded" , "Accept": "text/plain"},
    #                "192.168.1.29",
    #                8000,30,
    #                "/zh-cn/phone_message/phone_login/")
    # print type(json_data['data'])
    # data_dict=json_data['data'][0]
    #
    # for k,v in data_dict.iteritems():
    #     print "[%s]=" %k,v
    '''
    #test kaoala server
    # json_data=post_con({'username':'kentest','password':'kentest'},
    #                    {"Content-type": "application/x-www-form-urlencoded" , "Accept": "text/plain"},
    #                    "192.168.1.29",
    #                    8000,30,
    #                    "/zh-cn/phone_message/phone_login/")
    # print json_data

    # print type(json_data['data'])
    # data_dict=json_data['data'][0]
    # for k,v in data_dict.iteritems():
    #      print "[%s]=" %k,v

    httpClient=None
    params=urllib.urlencode(parmas)
    headers = headers                                               #{"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    httpClient = httplib.HTTPConnection(con_domain,port,timeout)    # '192.168.1.29:8000'
    #httpClient = httplib.HTTPConnection("192.168.1.29",port=8000,timeout=30)  # '192.168.1.29:8000'

    httpClient.request("POST",url,params,headers)
    response = httpClient.getresponse()
    #return response.status, response.reason
    #res=response.read()
    httpClient.close()
    jdata = json.load(response)
    try:
        if jdata['status']==1000:
            print 'wrong'
        else:
            print 'yes'
    except:
        print 'except found'
    return jdata

def write_ini_value(path_with_filename,title,attribute,value):
    '''
    写INI文件
    path_with_filename：路径包含文件名
    title：标题
    attribute：属性
    value:值得
    eg:write_ini('./settings.ini','testtitle','testattri','abc')
    :param value:
    :return:
    '''
    config = ConfigParser.ConfigParser()
    ini_have=True  #赋值ini文件存在的，为True
    # title='local'
    title=title
    attribute=attribute
    try:
        ini_file=open(path_with_filename,'r')
        config.readfp(ini_file)
        ini_file.close()
        title_list= config.sections()
    except:
        ini_have=False    #ini文件不存，为False
    if ini_have==True: #判断ini文件是否存在
        if title in title_list:  #判断title是否已经存在了，ini中【】的内容
            config.set(title, attribute, value)
        else:
            config.add_section(title)
            config.set(title, attribute, value)
    else:
        config.add_section(title)
        config.set(title, attribute, value)
    ini_file=open(path_with_filename,'w')
    config.write(ini_file)
    ini_file.close()

def read_ini_value(path_with_filename,title,attri):
    '''
    读INI
    path_with_filename：路径包含文件名
    title：标题
    attri：属性
    eg:read_ini('./settings.ini','testtitle','testattri')
    :return:
    '''
    if not os.path.exists(path_with_filename):
        return None
    else:
        config = ConfigParser.ConfigParser()
        ini_file=open(path_with_filename,'r')
        config.readfp(ini_file)
        # title= config.sections()   #获取ini中[](中括号中的内容)
        # value=config.get('local','language')
        value=config.get(title,attri)
        ini_file.close()
        return value

def read_ini(path_with_filename,**kwargs):
    '''
    弹性读INI，可以通过**kwargs获取option下，item下，section下的所有键
    pars "./config.ini",option="dbconfig" or items="dbconfig" or sections=""
    path_with_filename：路径包含文件名
    sections:返回文件里面所有title
    option:返回title下的所有key
    item:返回title下的列表
    例子：
    # print read_ini("./config.ini",option="dbconfig",items="dbconfig",sections="")
    # print read_ini("./config.ini")
    # print read_ini("./config.ini",item="dbconfig")
    '''
    if not os.path.exists(path_with_filename):
        return None
    else:
        cf = ConfigParser.ConfigParser()
        cf.read(path_with_filename)
        if kwargs:
            if kwargs.has_key("section"):
                s=cf.sections()
                return s
            if kwargs.has_key("option"):
                o = cf.options(kwargs['option'])
                return o
            if kwargs.has_key("item"):
                v = cf.items(kwargs['item'])
                return v
        else:
            return 'no par'

def check_file_exists(path):
    '''
    :param path: 返回文件路径
    :return:
    '''
    return os.path.exists(path)

def get_file_size(path):
    '''获取文件字节大小
    :param path:文件路径
    :return:
    '''
    if os.path.isfile(path=path)==True:
        return os.path.getsize(path)

def use_etl_or_log_path(par):
    '''
    :param par: 使用etl 日志路径还是 使用 function 路径，入参为'fun'则使用log_fun路径，否则，为log_etl路径
    :return:
    '''
    try:
        if par=='fun':
            return log_fun_dir
        elif par=='etl':
            return log_etl_dir
        else:
            print "logdir_miss，'fun' or'etl'"
            return None
    except Exception:
        return None

def get_log_dir_sort(target_dir):
    '''
    :param target_dir:排序指定文件夹中的所有文件，并排序，返回一个文件夹名称列表
    :return:
    '''
    export = []
    for root, dirs, fileNames in os.walk(target_dir):
        if fileNames:
            for filename in fileNames:
                # export.append(os.path.join(root, filename))
                export.append(filename)
    es=sorted(export)
    return es


def get_lastest_log_file_name(par):
    '''
    获取日志文件夹中的最后一个文件
    :par:选取
    '''
    # BASE_DIR=os.path.dirname(__file__)
    terget_dir=use_etl_or_log_path(par)
    f= lambda x : [x-1]
    templist=get_log_dir_sort(terget_dir)
    print templist
    if templist==[]:
        return str(datetime.now().strftime('%Y%m%d%H%M%S'))+'.txt'
    else:
        file_count= f(len(get_log_dir_sort(terget_dir)))[0]
    return templist[file_count]

def create_log_file(file_dir):
    '''
    在pfile_dir下产生一个日志文件，返回该文件对象
    :param pfile_dir:
    :return:
    '''
    filename=str(datetime.now().strftime('%Y%m%d%H%M%S'))
    f=open(file_dir+filename+'.txt','w')
    return f

def write_log(par,log_message,message_type):
    '''
    :param par: 如果par='fun'使用log_fun ,否则par='etl'  使用log_etl 文件夹
    :param log_message:日志内容
    :param message_type:信息类型
    :return:
    '''
    currentfile= use_etl_or_log_path(par)+get_lastest_log_file_name(par)
    try:
        if check_file_exists(currentfile):
            if get_file_size(currentfile)<=200:
                log_file=open(currentfile, 'a+')
                log_file.writelines(log_message_format(message_type,log_message))
                log_file.close()
            else:
                newfile=create_log_file(use_etl_or_log_path(par))
                newfile.writelines(log_message_format(message_type,log_message))
                newfile.close()
        else:
            f=create_log_file(use_etl_or_log_path(par))
            f.writelines(log_message_format(message_type,log_message))
            f.close()
    except Exception ,e:
        log_file=open(use_etl_or_log_path(par), 'a')
        log_file.writelines(log_message_format('error',str(e)))
        log_file.close()

def file_spite_fish(source_file,target_dir):
    '''
    分解大文件,每个文件50000行记录
    :param source_file:被分解的日志文件
    :param target_dir: 分解之后的文件夹路径
    :return:none
    usage_eg:file_spite_fish('D:/datasources/access_log.log',"D:/datasources/spite")
    '''
    sfile=open(source_file,'r')
    number=50000
    dataline=sfile.readline()
    tempdata=[]
    filenum=1

    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)
    try:
        while dataline:
            for row in range(number):
                # print dataline
                tempdata.append(dataline)
                dataline=sfile.readline()
                if not dataline:
                    break
            tfilename=os.path.join(target_dir,os.path.split(source_file)[1]+str(filenum)+'.txt')
            # print tfilename
            tfile=open(tfilename,'a+')
            tfile.writelines(tempdata)
            tfile.close()
            tempdata=[]
            print(tfilename+"创建于："+str(time.ctime()))
            filenum+=1
        sfile.close()
    except Exception ,e:
        write_log('fun','spite_finish','error')


def map_file_fish(sourcefile,target_dir):
    '''
    :param sourcefile:文件分解后
    :param target_dir:文件转换后文件夹
    :return:
    usage_eg:map_file_fish('D:/datasources/spite/access_log.log2.txt',"D:/datasources/map_file")
    '''
    sfile=open(sourcefile,'r')
    dataline=sfile.readline()
    tempdata={}
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)
    while dataline:
        p_re=re.compile(r'(GET|POST)\s(.*?)\sHTTP/1.[01]',re.IGNORECASE)#正则表达式，只匹配http的POST 和 GET方法 V1.X的内容
        match = p_re.findall(dataline)
        if match:
            visit_url=match[0][1]
            if visit_url in tempdata:
                tempdata[visit_url]+=1
            else:
                tempdata[visit_url]=1
        dataline=sfile.readline()
    sfile.close()

    tlist=[]
    for key,value in sorted(tempdata.items(),key = lambda k:k[1],reverse=True):
        tlist.append(key+' '+str(value)+'\n')

    tfilename = os.path.join(target_dir,os.path.split(sourcefile)[1]+"_map.txt")
    tfile = open(tfilename,'a+')
    tfile.writelines(tlist)
    tfile.close()

def reduce_fish(sourcefloder,targetfile):
    '''
    :param sourcefloder:合并map文件夹下面内容到
    :param targetfile:目标文件
    :return:
    usage_eg:reduce_fish('D:/datasources/map_file/',"D:/datasources/map_file/reduce")
    '''
    tempdata={}
    p_re=re.compile(r'(.*?)(\d{1,}$)',re.IGNORECASE)
    for root,dirs,files in os.walk(sourcefloder):
        for file in files:
            if file.endswith('_map.txt'):
                sfile=open(os.path.abspath(os.path.join(root,file)),'r')
                dataline=sfile.readline()

                while dataline:
                    subdata=p_re.findall(dataline)
                    if subdata[0][0] in tempdata:
                        tempdata[subdata[0][0]]+=int(subdata[0][1])
                    else:
                        tempdata[subdata[0][0]] = int(subdata[0][1])
                    dataline=sfile.readline()
                sfile.close()
    tlist=[]
    for key,value in sorted(tempdata.items(),key=lambda k:k[1],reverse=True):
        tlist.append(key+' '+str(value) + '\n')
    tfilename=os.path.join(sourcefloder,targetfile+'_reduce.txt')
    tfile=open(tfilename,'a+')
    tfile.writelines(tlist)
    tfile.close()

def change_listall2str(t):
    '''
    :param t :一个元组，里面含有日期，float,long,等形式，将其全部转换为字符后返回一个列表
    :return:
    '''
    templist=[]
    for i in t:
        if isinstance(i,datetime):
            k=str(i)
        elif isinstance(i,long):
            k=str(i)
        elif isinstance(i,float):
            k=str(i)
        else:
            pass
        templist.append(i)
    return templist

if __name__=="__main__":
    pass
    # create_log_file(BASE_DIR+'/log_fun/')
    write_log('fun',u'weew','abort')

    # write_log('etl','dddddddddddddddddddddddddddddddddd','message')
    #reduce_fish('D:/datasources/map_file/',"D:/datasources/reduce")