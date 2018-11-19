#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import config
import platform


# 读取配置获取文件

# 调用加固方法进加固

# 进行签名打包

def is_windows():
    sys_str = platform.system()
    if "Windosws" in sys_str:
        return 1
    else:
        return 0


def get_backslash():
    if is_windows() == 1:
        return "\\"
    else:
        return "/"


def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def create_dir(dir_path):
    try:
        os.makedirs(dir_path)
    except Exception:
        pass


def create_protected_output_path(dir_path):
    if not os.path.exists(dir_path):
        create_dir(dir_path)
    else:
        del_file(dir_path)


def create_channel_output_360_path(dir_path):
    if not os.path.exists(dir_path):
        create_dir(dir_path)
    else:
        del_file(dir_path)


def create_channel_output_legu_path(dir_path):
    if not os.path.exists(dir_path):
        create_dir(dir_path)
    else:
        del_file(dir_path)


def create_channel_output_no_protected_path(dir_path):
    if not os.path.exists(dir_path):
        create_dir(dir_path)
    else:
        del_file(dir_path)


# 获取360加固后的文件
def get_360_jiagu_apk_path(apk_dir_path):
    # 从加固后的目录中获取360加固过后的包
    list = os.listdir(apk_dir_path)
    for i in range(0, len(list)):
        path = os.path.join(apk_dir_path, list[i])
        if os.path.isfile(path) and path.endswith(".apk") and path.find("jiagu"):
            return path
            # 对文件进行判断
    return ""


# 寻找legu加固后的应用包
def get_legu_jiagu_apk_path(apk_dir_path):
    list = os.listdir(apk_dir_path)
    for i in range(0, len(list)):
        path = os.path.join(apk_dir_path, list[i])
        if "legu" in path:
            return path
            # 对文件进行判断
    return ""


def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)


def parent_dir():
    return cur_file_dir() + get_backslash()


def start_walle(jiagu_apk_path,
                channels,
                channels_output_file_path):
    zip_aligned_apk_path = jiagu_apk_path[0: -4] + "_aligned.apk"
    signed_apk_path = zip_aligned_apk_path[0:-4] + "_signed_.apk"
    print("-----------对齐-----------------------------------------------")
    legu_zipalign_shell = build_tools_path + "zipalign -v 4 " + jiagu_apk_path + " " + zip_aligned_apk_path
    os.system(legu_zipalign_shell)
    print("-----------签名-----------------------------------------------")
    sign_shell = build_tools_path + "apksigner sign --ks " + key_path + " --ks-key-alias " + key_alias + \
                 " -ks-pass " "pass:" + keystore_pw + " --key-pass pass:" + key_pw + " --out " + signed_apk_path + " " + zip_aligned_apk_path
    os.system(sign_shell)
    print("-----------check android v2 sign is ok--------------")
    check_v2_shell = "java -jar " + check_android_v2_signature_path + " " + signed_apk_path
    os.system(check_v2_shell)
    # 写入渠道
    print("----------写入渠道到应用包中")
    write_channel_shell = "java -jar " + wall_channel_writer_path + " batch -f " + channels + " " + signed_apk_path + " " + channels_output_file_path
    os.system(write_channel_shell)
    print("----------加固 签名 添加渠道完成--------------------")
    os.remove(zip_aligned_apk_path)
    os.remove(signed_apk_path)


def init_data():
    global protected_source_path, protected_output_path, key_path, key_pw, key_alias, keystore_pw, build_tools_path, check_android_v2_signature_path, wall_channel_writer_path
    # 初始化配置文件数据
    protected_source_path = parent_dir() + config.protected_source_path
    protected_output_path = parent_dir() + config.protected_output_path
    key_path = config.keystorePath
    key_pw = config.keyPassword
    key_alias = config.keyAlias
    keystore_pw = config.keystorePassword
    lib_path = parent_dir() + "lib" + get_backslash()
    build_tools_path = config.sdkBuildToolPath + get_backslash()
    check_android_v2_signature_path = lib_path + "CheckAndroidV2Signature.jar"
    wall_channel_writer_path = lib_path + "walle-cli-all.jar"
    # 初始化目录
    create_protected_output_path(protected_output_path)


# 无需加固的打包
def no_protected_package():
    no_protected_path = parent_dir() + config.no_protected_source_path
    channels_output_file_path3 = parent_dir() + config.no_protected_apk_output_channels
    create_channel_output_no_protected_path(channels_output_file_path3)
    channels = parent_dir() + config.no_protected_channels
    start_walle(no_protected_path, channels, channels_output_file_path3)


# 360打包
def _360_package():
    _360_jar_path = config._360_jar_path
    _360_login_account = config._360_login_account
    _360_channels = parent_dir() + config._360_jiagu_channels
    _360_secret = config._360_login_secret
    channels_output_file_path1 = parent_dir() + config._360_jiagu_apk_output_channels
    create_channel_output_legu_path(channels_output_file_path1)
    print("-------------start login 360 jiagu----------------------------")
    login_360_jiagu = "java -jar " + _360_jar_path + " -login " + _360_login_account + " " + _360_secret
    print(login_360_jiagu)
    os.system(login_360_jiagu)
    print("------------login 360 jiagu success---------------------------")
    print("------------start import sign file----------------------------")
    sign_file = "java -jar " + _360_jar_path + " -importsign " + key_path + " " + keystore_pw + " " + key_alias + " " + key_pw
    print(sign_file)
    os.system(sign_file)
    print("------------import sign file success--------------------------")
    print("------------start jiagu app-----------------------------------")
    start_jiagu_jar = "java -jar " + _360_jar_path + " -jiagu " + protected_source_path + " " + protected_output_path
    print(start_jiagu_jar)
    os.system(start_jiagu_jar)
    print("------------加固完毕-------------------------------------------")
    # 寻找360加固后的应用宝
    _360_jiagu_apk_path = get_360_jiagu_apk_path(protected_output_path)
    # 进行加固后的文件重新签名+渠道
    start_walle(_360_jiagu_apk_path, _360_channels, channels_output_file_path1)


# 乐固打包
def legu_package():
    legu_jar_path = parent_dir() + config.legu_jar_path
    legu_secret_id = config.legu_secretId
    legu_secret_key = config.legu_secret_key
    legu_channels = parent_dir() + config.legu_channels
    channels_output_file_path2 = parent_dir() + config.legu_jiagu_apk_output_channels
    create_channel_output_legu_path(channels_output_file_path2)
    # #legu加固并签名+渠道
    legu_test = "java -Dfile.encoding=utf-8 -jar " + legu_jar_path + " -sid " + legu_secret_id + " -skey " + \
                legu_secret_key + " -uploadPath " + protected_source_path + " -downloadPath " + protected_output_path
    print(legu_test)
    os.system(legu_test)
    legu_jiagu_apk_path = get_legu_jiagu_apk_path(protected_output_path)
    print("legu_jiagu_apk_path>>" + legu_jiagu_apk_path)
    # # 进行加固后的文件重新签名+渠道
    start_walle(legu_jiagu_apk_path,legu_channels, channels_output_file_path2)


# 初始化数据/配置/目录
init_data()
# 360加固
_360_package()
# 乐固加固
legu_package()
# 没有加固的应用
no_protected_package()

