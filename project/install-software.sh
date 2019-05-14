#!/usr/bin/env bash
# simple script menu

function mainMenu {
 clear
 echo
 echo -e "\t\t\tinstallation software\n"
 echo -e "\t1. first installation python2.6 configparser"
 echo -e "\t2. installation nginx v1.14.2"
 echo -e "\t3. installation tomcat v8.5.39"
 echo -e "\t4. installation db2 v10.5"
 echo -e "\t5. installation mariadb v10.3"
 echo -e "\t6. installation project"
 echo -e "\t0. Exit menu"
 echo -en "\tEnter an option:"
 read  option 
}

function projectMenu {
 clear
 echo 
 echo -e "\t\t\tproject selection\n"
 echo -e "\t1. installation largecash"
 echo -e "\t2. installation evaluate"
 echo -e "\t3. modify project db.properties"
 echo -e "\t0. return main menu"
 echo -en "\tEnter an option:"
 read projectOption
}

function projectWhile {
 while [ 1 ]
 do
  projectMenu
  case $projectOption in
  0)
   break ;;
  1)
   echo "Sorry,Not finished yet" ;;
  2)
   echo "Sorry,Not finished yet" ;;
  3)
   /usr/bin/python ./script/project-modify-conf.py ;;
  *)
   clear
   echo "Sorry, wrong selection" ;;
   esac
   echo -en "\n\n\t\t\tHit any key to continue"
   read -n 1 line
 done
}

while [ 1 ]
do
 mainMenu
 case $option in
 0)
 break ;;
 1)
 /usr/bin/python ./script/install-configparser.py ./software/configparser-py2.6.tar ;; 
 2)
 /usr/bin/python ./script/linux-install-nginx.py ;;
 3)
 /usr/bin/python ./script/linux-install-tomcat.py ;;
 4)
 /usr/bin/python ./script/linux-install-db2.py ;;
 5)
 /usr/bin/python ./script/linux-install-mariadb.py ;;
 6)
  projectWhile ;;
 *)
 clear
 echo "Sorry, wrong selection" ;;
 esac
 echo -en "\n\n\t\t\tHit any key to continue"
 read -n 1 line
done
clear
