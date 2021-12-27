import os
import sys
import json
import configparser


# 读取配置文件[连接/分类/标签信息]
def readConf():
    print ("I'm readConf()...");

    global zbxConn;

    # 修复configparser读取文件时左边总为小写
    cfg = configparser.RawConfigParser();
    cfg.optionxform = str;

    # 适配.gitignore防止自用登录信息被git push泄露
    if os.path.exists('zbx-login1.ini'):
        cfg.read_file(open("zbx-login1.ini"));
        print ("Reading zbx-login1.ini...");
    else:
        cfg.read_file(open("zbx-login.ini"));
        print ("Reading zbx-login.ini...");
    # print (cfg.sections());

    # ini配置文件允许定义多个zbx server
    # 遍历ini配置文件中带有zabbix的section
    # 并将它存入zbxConn列表中
    # 多个zbx server必须以[zabbix]开头，可以后面接数字
    # 如[zabbix1] [zabbix2]等
    zbxConn = [];
    for i,elem in enumerate(cfg.sections()):
        # sections里面有以zabbix开头的部分
        if 'zabbix' in elem:
            # print (json.dumps(elem,indent=4));
            zbxConn.append(cfg._sections[elem]);

            # 判断ini配置中是否存在必需配置项
            if (cfg.has_option(elem,'host')) and (cfg.has_option(elem,'user')) \
                    and (cfg.has_option(elem,'password')) :
                pass;
            else:
                print (elem + " : cfg file has NO HOST/USER/PASSWD Defined!!! Terminated!!!\n");
                exit();

            # 判断配置文件中host/user/password是否合法
            if len(cfg[elem]['host']) == 0 or len(cfg[elem]['user']) == 0 or\
                    len(cfg[elem]['password']) == 0 :
                print (elem + " : HOST/USER/PASSWORD is EMPTY!!! Terminated!!!\n");
                exit();

            # print ("end... " + elem);

    # print (json.dumps(zbxConn, indent=4));

    print ("readConf done!...\n");
