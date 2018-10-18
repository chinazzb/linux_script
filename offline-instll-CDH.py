# -*- coding: utf-8 -*-
#!/usr/bin/python
#python: 2.7.x
#organization: China Poka
#Author: Duan Yu
#Date: 2018-09-18
#version: 0.0.1


#sotware
#CDH CM JDK mysql-connect5.1.47 my.cnf

#all software packages /opt/tar


import time
import os



#get write ip and hostname,scp /etc/hosts all hosts
def configHosts():
    #get ip and hostname

    ipHostNameStr = raw_input("demo:172.16.2.1 hadoop-dn2,172.16.2.2 hadoop-dn3\n"
                              "Please input in the corresponding format"
                              "\ninput all ip and host:\n")
    print("按照此格式输出:172.16.2.1 hadoop-dn2,172.16.2.2 hadoop-dn3\n以逗号为分隔符\n输入你的全部主机")
    print("check your ip and host:\n请检查解析后的格式是否正确:")
    ipHostNameArray = []
    ipHostNameArray = ipHostNameStr.split(',')
    for i in range(len(ipHostNameArray)):
        print(ipHostNameArray[i])
    print("If it's error\n. restart this script == ctrl+c\nPerform the next step after 6 seconds")
    print("如果格式错误,ctrl+c 退出脚本，再次运行\n6秒后执行下一步")
    time.sleep(6)

    #wirte file
    hostsFile = open("/etc/hosts","a")
    for i in range(len(ipHostNameArray)):

        try:
            hostsFile.write(ipHostNameArray[i]+"\n")
        except BaseException as BaseError:
            errorMessage = str(BaseError)
            os._exit(1)
        finally:
            if errorMessage != None:
                print(errorMessage)
    hostsFile.close()
    print("Successfully write to the hosts file\n"
          "写入hosts文件成功")
    return 0

# ssh-copy-id(think overs)
def sshCopyId():#doing
    print('test')

# add Reop
def systemReop(systemType):
    if systemType == 'Centos' or 'Redhat':
        print("this is host system:Centos or Redhat")
        print("Sorry, this operating system is currently not supported. ")
        #add repo
    if systemType == 'SLES':
        print("this is host system:SLES")
        #add  repo
        os.system("rm -rf /etc/zypp/repos.d/*")
        os.system("mkdir -p /opt/iso/SLES12")
        os.system("mount -o loop /opt/tar/SLE-12-SP3-Server-DVD-x86_64-GM-DVD1.iso /opt/iso/SLES12")
        os.system("zypper ar file:///opt/iso/SLES12/ SLES12")

#install software
def installSoftware():
    #system and database type
    systemType = rawInput.systemType()
    DBType = rawInput.DBType()

    #rely install
    #installSoftwareSystem(systemType,DBType)

    #JDK install
    #installSoftwareJDK()

    #CM install
    installSoftwareCM(DBType)

#install JDK
def installSoftwareJDK():
    JDKFileName = rawInput.JDKFileName()
    if 'rpm' in JDKFileName:
        os.system("rpm -ivh /opt/tar/" + JDKFileName)
    elif 'tar.gz' in JDKFileName:
        os.system("tar zxvf /opt/tar/" + JDKFileName + " -C /usr/java/")
    JAVA_HOME = rawInput.JAVAHOME()
    profile = open("/etc/profile","a")
    try:
        profile.write("export JAVA_HOME=/usr/java/" + JAVA_HOME + "\n")
        profile.write("export PATH=$JAVA_HOME/bin:$PATH\n")
    except BaseException as BaseError:
        errorMessage = str(BaseError)
        print(errorMessage)
        print("Fatal error occurred, exit script\出现致命错误退出脚本")
        os._exit(1)
    finally:
        profile.close()
    os.system("source /etc/profile")
    print("JDK configuration Successfully\nJDK配置成功")

#install CM
def installSoftwareCM(DBType):
    #install cloudera-manager
    CMHOME="/opt"
    CMFileNmae = rawInput.CMFileName()
    CMVersion = rawInput.CMversion()
    CMType = rawInput.CMType()
    CDHFileName = rawInput.CDHFileName()
    #create cloudera-manager user group
    CMDir = CMHOME + "/cm-" + CMVersion
    CDHDir = "/opt/cloudera/parcel-repo"
    os.system("mkdir "+CMHOME)
    os.system("tar xvfz /opt/tar" + CMFileNmae + "-C " + CMHOME)
    os.system('useradd --system '
              '--home=' + CMDir + '/run/cloudera-scm-server'
                                  '--no-create-home '
                                  '--shell=/bin/false '
                                  '--comment "Cloudera SCM User" cloudera-scm')
    os.system("groupadd cloudera-scm")
    os.system("chown -R cloudera-scm:cloudera-scm /opt/c*")


    #server
    if 'server' in CMType:
        os.system("mkdir /var/lib/cloudera-scm-server")
        os.system("chown cloudera-scm:cloudera-scm /var/lib/cloudera-scm-server")

        #scm database connect
        if "mysql" in DBType:
            os.system("tar zxvf /opt/tar/mysql-connector-java-5.1.47.tar.gz -C /opt/tar/")
            os.system("mkdir -p /usr/share/java")
            os.system("cp /opt/tar/mysql-connector-java-5.1.47/mysql-connector-java-5.1.47-bin.jar "
                      "/usr/share/java/mysql-connector-java.jar")

        print("Please input:scm123")
        os.system(CMDir + "/share/cmf/schema/scm_prepare_database.sh " + DBType + " scm scm")
        #CDH move CMHOME+"
        os.system("mv /opt/tar/" + CDHFileName + " " + CDHDir )
        os.system("mv /opt/tar/" + CDHFileName + ".sha1 " + CDHDir + CDHFileName + "sha")

        #cloudera-scm user start cloudera-scm-server
        os.system("sudo -u cloudera-scm" + CMDir + "/etc/init.d/cloudera-scm-" + CMType + " start ")

        #default file
        CMDefaultServerFileRead = open(CMDir + "/etc/default/cloudera-scm-server").readlines()
        CMDefaultServerFileWrite = open(CMDir + "/etc/default/cloudera-scm-server","r+")
        for defaultServerStr in CMDefaultServerFileRead:
            CMDefaultServerFileWrite.write(defaultServerStr.replace("export CMF_SUDO_CMD=\" \""),"#export CMF_SUDO_CMD=\" \"")
        CMDefaultServerFileWrite.close()

        #init file
        os.system("cp " + CMDir + "/etc/init.d/cloudera-scm-" + CMType + " /etc/init.d/cloudera-scm-" + CMType)
        os.system("chkconfig clouder-scm-" + CMType + " on")
        CMInitServerFileRead = open("/etc/init.d/cloudera-scm-server").readlines()
        CMInitServerFileWrite = open("/etc/init.d/cloudera-scm-server","r+")
        for initStr in CMInitServerFileRead:
            CMInitServerFileWrite.write(initStr.replace("CMF_DEFAULTS=${CMF_DEFAULTS:-/etc/default}",
                                                        "CMF_DEFAULTS=" + CMDir + "/etc/default"))
        CMInitServerFileWrite.close()

    #agent
    if 'agent' in CMType:
        #defult file
        CMDefaultAgentFileRead = open(CMDir + "/etc/default/cloudera-scm-agent").readlines()
        CMDefaultAgentFileWrite = open(CMDir + "/etc/default/cloudera-scm-agent","r+")
        for defaultAgentStr in CMDefaultAgentFileRead:
            CMDefaultAgentFileWrite.write(defaultAgentStr.replace("export CMF_SUDO_CMD=\" \""),"#export CMF_SUDO_CMD=\" \"")
        CMDefaultAgentFileWrite.close()

        #init.d file
        os.system("cp " + CMDir + "/etc/init.d/cloudera-scm-" + CMType + " /etc/init.d/cloudera-scm-" + CMType)
        os.system("chkconfig clouder-scm-" + CMType + " on")
        CMInitAgentFileRead = open("/etc/init.d/cloudera-scm-" + CMType).readlines()
        CMInitAgentFileWrite = open("/etc/init.d/cloudera-scm-" + CMType,"r+")
        for initStr in CMInitAgentFileRead:
            CMInitAgentFileWrite.write(initStr.replace("CMF_DEFAULTS=${CMF_DEFAULTS:-/etc/default}",
                                                       "CMF_DEFAULTS=" + CMDir + "/etc/default"))
        CMInitAgentFileWrite.close()

        #server host
        CMAgentConfRead = open(CMDir + "/etc/cloudera-scm-agent/config.ini").readlines()
        CMAgentConfWrite = open(CMDir + "/etc/cloudera-scm-agent/config.ini","r+")
        CMServerHostName = rawInput.ServerHost()
        for agentConf in CMAgentConfRead:
            CMAgentConfWrite.write(agentConf.replace("server_host=localhost","server_host=" + CMServerHostName))
        CMAgentConfWrite.close()

        #chkconfig cloudera-scm-agent
        os.system("cp " + CMDir + "/etc/init.d/cloudera-scm-" + CMType + " /etc/init.d/cloudera-scm-" + CMType+ "")
        os.system("chkconfig clouder-scm-" + CMType + " on")


# install system software
def installSoftwareSystem(systemType,DBType):
        #install system software
        systemReop(systemType)
        if 'Centos' or 'Redhat' in systemType:
            print("Sorry, this operating system is currently not supported. ")
            os._exit(0)
        if 'SLES' in systemType:
            os.system("zypper install -y gcc gcc-c++")
            os.system("zypper install -y" + DBType)
            os.system("systemctl start" + DBType)
            os.system("systemctl enable" + DBType)
            #Configuration database type
            if 'mysql' in DBType:
                print("Follow the prompts:\n根据提示进行操作:")
                os.system("/usr/bin/mysql_secure_installation")
                os.system("mv /etc/my.cnf /etc/my.cnf.bak")
                os.system("cp /opt/tar/my.cnf /etc/my.cnf")
                os.system("systemctl restart" + DBType)
                #Configuration scm user database
                os.system("mysql -uroot -p -e 'CREATE DATABASE scm DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci' \n")
                print("Please mysql root passowrd:\n请输入mysql root 密码:")
                os.system("mysql -uroot -p -e \"GRANT ALL ON scm.* TO scm@'%' IDENTIFIED BY 'scm123+'\" \n")
            if 'postgresql' in DBType:
                print("Sorry, this operating database is currently not supported. ")
                os._exit(0)

        #jdk
        os.system("mkdir /usr/java/")

#all raw_input idea
class rawInput():
    @staticmethod
    def systemType():
        return raw_input("demo:Centos Redhat SLES\n选择操作系统")
    @staticmethod
    def DBType():
        return raw_input("demo:mysql postgresql\nChoose database type\n选择数据库类型")
    @staticmethod
    def JAVAHOME():
        return raw_input("demo:ls /usr/java\nPlease input java version dir name\n请输入java版本号目录名")
    @staticmethod
    def CMFileName():
        return raw_input("Please input clouder-manager file name:\n请输入clouder-manager文件名称:")
    @staticmethod
    def CMVersion():
        return raw_input("Please input clouder-manager Version:\n请输入clouder-manager版本号:")
    @staticmethod
    def CDHFileName():
        return raw_input("Please input CDH file name:\n请输入CDH文件名称:")
    @staticmethod
    def DataBaseConnect():
        return raw_input("input database-connect file name:\n请输入数据库连接器文件名称:")
    @staticmethod
    def JDKFileName():
        return raw_input("Please input jdk file name:\n请输入jdk文件名称:")
    @staticmethod
    def CMType():
        return raw_input("demo:server agent\ninput CM Type file name:\n请输入CM 类型:")
    @staticmethod
    def ServerHost():
        return raw_input("demo:linux-cm\ninput CM server host name:\n请输入CM服务端主机名:")


if __name__ == '__main__':
    configHosts()
    installSoftware()
