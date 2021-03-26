import requests
import time
# sha256加密
import hashlib
# 忽略https证书验证的警告
import urllib3
import datetime
import url_path_param
import ast


urllib3.disable_warnings()
# 全局变量，使用input方式获得
NQSZ_base_url = url_path_param.NQSZ_base_url
# 设置请求头
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'charset': 'UTF-8'
}
vpn_key = ''

# 新建用户需要的信息
name = ''
passwd = 'hxzq123'
parent_group = ''
phone = ''
gqsj = 0
ex_time = '2022-02-24'
user_note = ''

# 新建资源需要的信息
rec_name = ''
addr_str = ''
rctype = 1  # TCP资源
note = ''
rc_grp_name = ''

#

def user_client():
    print('=========VPN Client=========')
    print('------choose an option------')
    option = -1
    while int(option) != 0:
        print('1. 添加新用户')
        print('2. 创建资源，建立对应关系')
        print('0. 退出客户端')
        # print('The option is ', option)
        option = input()
        if int(option) == 1:
            global name
            name = input("输入用户名:")
            # 输入用户名，检查是否重复
            exit_user = search_exit_user(name)
            if not exit_user:
                # time.sleep(3)
                print('----无此用户，新建用户输入对应信息----')
                global phone
                phone = input("输入手机号:")
                print('----1-宁桥路客户\n----2-南方中心客户\n----3-外高桥机房')
                user_path = input("请选择用户路径:")
                global parent_group
                if int(user_path) == 1:
                    parent_group = '/奇点客户/宁桥路客户'
                elif int(user_path) == 2:
                    parent_group = '/奇点客户/南方中心客户'
                elif int(user_path) == 3:
                    parent_group = '/奇点客户/外高桥机房'
                global user_note
                user_note = input("请输入备注：")
                add_new_user()
                # print('User name is', name, '\nPhone is ', phone, '\nuserpath is ', parent_group)
            else:
                name = input("确认用户名:")
        elif int(option) == 2:
            global rc_grp_name
            print('----1-宁桥路\n----2-南方中心\n----3-外高桥机房')
            rc_path = input("请选择资源路径:")
            if int(rc_path) == 1:
                rc_grp_name = '宁桥路机房'
            elif int(rc_path) == 2:
                rc_grp_name = '南方中心机房'
            elif int(rc_path) == 3:
                rc_grp_name = '外高桥机房'
            global rec_name
            rec_name = input("请输入资源名称：")
            global addr_str
            addr_str = input("请输入资源地址：")
            sys_type = input("请选择机器类型：\n1. Linux\n2. Windows\n")
            if int(sys_type) == 1:
                addr_str += '/22:22'
            elif int(sys_type) == 2:
                addr_str += '/3389:3389'
            add_new_rec()
            print('==========新建资源完成===========')
            time.sleep(3)
            auth_user_rec()
            print('==========建立角色授权完成=========')
        else:
            pass


def auth_user_rec():
    timestamp = int(time.time())
    url_param = resol_url_param(url_path_param.add_new_auth_role.get('url_param'))

    url_param_data_new_auth_role = {
        'timestamp': timestamp,
        'name': rec_name,
        'rcNamesStr': rec_name,
        'userNamesStr': name
    }
    data = get_token_data(url_param, url_param_data_new_auth_role, timestamp)
    add_new_auth_role_url = url_path_param.add_new_auth_role.get('url_param')
    res = get_request(add_new_auth_role_url, data)
    print('------授权用户：', name, '---资源名称：', rec_name)
    print(res.content)


def add_new_rec():
    timestamp = int(time.time())
    url_param = resol_url_param(url_path_param.add_Res_Cloud.get('url_param'))

    url_param_data_new_rec = {
        'timestamp': timestamp,
        'name': rec_name,
        'addr_str': addr_str,
        'rctype': rctype,
        'note': note,
        'rc_grp_name': rc_grp_name,
    }

    data = get_token_data(url_param, url_param_data_new_rec, timestamp)
    add_new_rec_url = url_path_param.add_Res_Cloud.get('url_param')
    res = get_request(add_new_rec_url, data)
    print('--------新建资源---------')
    print(res.text)


def search_exit_user(username):
    # 是否存在用户
    exist_user = False
    timestamp = int(time.time())
    url_param = resol_url_param(url_path_param.ex_get_user_Info.get('url_param'))
    url_param_search_user = {
        'timestamp': timestamp,
        'username': username
    }
    url_param.update(url_param_search_user)
    data = get_token_data(url_param, url_param_search_user, timestamp)
    print('-------Search User----', data)
    search_user_url_path = url_path_param.ex_get_user_Info.get('url_param')

    res = get_request(search_user_url_path, data)
    res.json()
    # print(res.json())
    if res.json().get('code') == 0:
        exist_user = True
        print('----------存在同名用户-----------')
    return exist_user


def add_new_user():
    # 获取秒级时间戳
    timestamp = int(time.time())
    # 计算params
    # 获取url中的原始参数
    url_param = resol_url_param(url_path_param.add_User_Cloud.get('url_param'))
    # 获取不同请求接口需要放入body中的参数
    url_param_data_Adduser = {
        'timestamp': timestamp,
        'name': name,
        'passwd': passwd,
        'parent_group': parent_group,
        'phone': phone,
        'gqsj': gqsj,
        'ex_time': ex_time,
        'note': user_note
    }
    data = get_token_data(url_param, url_param_data_Adduser, timestamp)
    print('-------add New User----', data)

    add_new_user_url_path = url_path_param.add_User_Cloud.get('url_param')
    # 调用封装的request
    res = get_request(add_new_user_url_path, data)
    print(res.content)


# Helper Function
# 根据不同url的param返回请求主体中的data字符串
def get_token_data(url_param, url_param_data, timestamp):

    # 拼接api含有的param和请求体的params，但未改变url_param_data_Adduser
    url_param.update(url_param_data)
    query_string = create_param(url_param)
    # sha256加密拼接的字符串
    sinfor_apitoken = get_sinfor_apitoken(query_string, url_param_data, timestamp)
    data = 'sinfor_apitoken=' + sinfor_apitoken

    return data


# 将字符串解析为字典
def resol_url_param(url_string):
    url_param = {}
    lt = str(url_string).split('&')
    for i in lt:
        llt = str(i).split('=')
        url_param[llt[0]] = llt[1]
    return url_param


# 封装一个request方法，便于各个API接口调用
def get_request(url, data):
    req_url = NQSZ_base_url + url
    res = requests.post(req_url, data=data.encode('utf8'), verify=False, headers=headers)
    return res


def get_sinfor_apitoken(query_string, request_param, timestamp):
    # 传入的是query_string
    # 需要手动拼接一下待加密的字符串
    sha256_param = query_string + str(timestamp) + vpn_key
    print('-------加密字段', sha256_param)

    sha256 = hashlib.sha256(sha256_param.encode('utf8'))
    # 拼接apiToken字段
    tokenlt = []
    tokenlt.append(str(sha256.hexdigest()))
    for i in request_param:
        tokenlt.append(i + '=' + str(request_param[i]))
    sinfor_apitoken = '&'.join(tokenlt)
    return sinfor_apitoken


# 用于排序param，返回拼接好的字段
def create_param(param):
    lt = []
    # 对params排序
    for i in sorted(param):
        lt.append(i+'='+str(param[i]))
    query_string = '&'.join(lt)
    # 使用& 拼接querystring
    return query_string


def set_ex_time():
    # 获取当前时间，并格式化显示
    # 用户设置1年的过期时间
    now_time = datetime.datetime.now() + datetime.timedelta(days=365)
    # print(now_time.strftime('%Y-%m-%d'))
    ex_time = now_time.strftime('%Y-%m-%d')
    return ex_time


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # help(requests)
    # NQ_SZ()
    # set_ex_time()
    user_client()

