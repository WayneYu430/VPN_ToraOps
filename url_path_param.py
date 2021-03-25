# 用于存放不同接口的基本参数
# 访问APi的URL是固定不变的，单独存放在变量文件中

NQSZ_base_url = 'https://101.226.250.250:4430/cgi-bin/' \
                'php-cgi/html/delegatemodule/WebApi.php?'

add_User_Cloud = {
    'url_param': 'controler=User&action=AddUserCloud'
}

ex_get_user_Info = {
    'url_param': 'controler=User&action=ExGetUserInfo'
}

add_Res_Cloud = {
    'url_param': 'controler=Resource&action=AddResourceCloud'
}

add_new_auth_role = {
    'url_param': 'controler=Role&action=AddRoleCloud'
}


