#!/bin/bash


if [ $USER == "root" ]
    then
        echo "Uninstalling eems using pip"
        pip uninstall eems -y
        echo "Removing var/www/eems folder"
        rm -r /var/www/eems
        echo "Removing apache configuration files"
        rm /etc/apache2/sites-available/eems.conf
        rm /etc/apache2/sites-enabled/eems.conf
    else
        echo "Please run as *sudo*."
fi
