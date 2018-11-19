#!/usr/bin/python  
#-*-coding:utf-8-*-
#360加固的jar包路径
_360_jar_path = "lib/360jiagu/jiagu.jar"
_360_login_account = "xxx"
_360_login_secret = "xxx"

legu_jar_path = "lib/ms-shield.jar"
legu_secretId = "xxx"
legu_secret_key = "xxx"

#需要加固的源apk包
protected_source_path = "app-release.apk"
#不需要加固的源apk包
no_protected_source_path = "app-release-no-protected.apk"
#需要加固的文件的输出目录
protected_output_path = "output_apk"
#360加固的包签名渠道配置文件
_360_jiagu_channels = "channels-1"
#legu加固的包签名渠道配置文件
legu_channels = "channels-2"
#不需要加固的包签名渠道配置文件
no_protected_channels = "channels-3"
#360加固包经过重新签名后的包存放位置
_360_jiagu_apk_output_channels = "channels-360"
#legu加固包经过重新签名后的包存放位置
legu_jiagu_apk_output_channels = "channels-legu"
#没有加固包经过重新签名后的包存放位置
no_protected_apk_output_channels = "channels-no-protected"

#keystore信息
#Windows 下路径分割线请注意使用\\转义
keystorePath = "xxx"
keyAlias = "xxx"
keystorePassword = "xxx"
keyPassword = "xxx"

#Android SDK buidtools path , please use above 25.0+
sdkBuildToolPath = "xxx"


#加固后的源文件所在文件夹路径(...path),注意结尾不要带分隔符，默认在此文件夹根目录
protectedSourceApkDirPath = ""
#渠道包输出路径，默认在此文件夹Channels目录下
channelsOutputFilePath = ""
#渠道名配置文件路径，默认在此文件夹根目录
channelFilePath = ""

