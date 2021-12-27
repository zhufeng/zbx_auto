import json
import readConf
import prettytable as table
from pyzabbix import ZabbixAPI

print ("I'm get_itmes()...", "\n");

# 读取配置文件中的zbx server信息
readConf.readConf();
zbxConn = readConf.zbxConn;
print (json.dumps(zbxConn, indent=4));


for conn in zbxConn:
    zapi = ZabbixAPI(conn['host']);
    zapi.login(conn['user'], conn['password']);
    # You can also authenticate using an API token instead of user/pass with Zabbix >= 5.4
    # zapi.login(api_token='xxxxx')
    print("Connected to Zabbix API Version %s" % zapi.api_version())

    hostTb = table.PrettyTable();
    hostTb.field_names = ["hostid", "host", "name"]

    for host in zapi.host.get(output="extend"):
        print(host['hostid'], host['host'], host['name']);
        # print (json.dumps(h, indent=4));
        hostTb.add_row([host['hostid'], host['host'], host['name']]);

        for item in zapi.item.get(filter={'hostid': host['hostid']}):
            # print (json.dumps(item, indent=4));
            print (item['itemid'], item['key_']);

            for his in zapi.history.get(itemids=item['itemid'],limit=3,history=1):
                # print (json.dumps(his, indent=4));
                print ("his", his['itemid'], his['value']);

        exit();

print (hostTb);
