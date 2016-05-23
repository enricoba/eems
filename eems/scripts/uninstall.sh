#!/bin/bash


# main code
if [ $USER == "root" ] ; then
    # uninstalling eems using pip
    # pip uninstall eems -y

    # removing server files
    if [ -d /var/www/eems ]
        then
            echo "Removing var/www/eems:"
            rm -r /var/www/eems
            if [ $? -eq 0 ] ; then
                echo "  Successfully removed /var/www/eems"
                flag_01="true"
            else
                echo "  Failed to remove/var/www"
                echo "  Please clean up manually"
                flag_01="false"
            fi
        else
            flag_01="true"
    fi

    # removing apache configuration file
    if  [ -e /etc/apache2/sites-available/eems.conf ] ; then
        echo "Removing apache config file:"
        rm /etc/apache2/sites-available/eems.conf
        if [ $? -eq 0 ] ; then
            echo "  Successfully removed apache config  files"
            flag_02="true"
        else
            echo "  Failed to remove apache config files"
            echo "  Please clean up manually"
            flag_02="false"
        fi
    else
        flag_02="true"
    fi

    # removing apache configuration file link
    if  [ -e /etc/apache2/sites-enabled/eems.conf ] ; then
        echo "Removing apache config file link:"
        rm /etc/apache2/sites-enabled/eems.conf
        if [ $? -eq 0 ] ; then
            echo "  Successfully removed apache config file link"
            flag_03="true"
        else
            echo "  Failed to remove apache config file link"
            echo "  Please clean up manually"
            flag_03="false"
        fi
    else
        flag_03="true"
    fi

    # final check
    if  [ $flag_01 == "true" ] && [ $flag_02 == "true"  ] && [ $flag_03 == "true"  ] ; then
        echo -e "\e[92mSuccessfully uninstalled eems\e[0m"
    else
        echo -e "\e[31mFailed to uninstall eems\e[0m"
        echo "An error occurred during uninstall, please follow the manual steps"
    fi

else
    echo "Please run as *sudo*"
fi
