#!/bin/bash


if [ $USER == "root" ]
    then
        # uninstalling eems using pip
        pip uninstall eems -y

        # removing server files
        if [ -d /var/www/eems ]
            then
                echo "Removing var/www/eems:"
                rm -r /var/www/eems
                echo "  Successfully removed /var/www/eems"
        fi

        # removing apache configuration file
        if [ -f  /etc/apache2/sites-available/eems.conf ]
            then
                echo "Removing apache configuration file eems.conf:"
                rm /etc/apache2/sites-available/eems.conf
                echo "  Successfully removed eems.conf"
        fi

        # removing apache configuration file link
        if [ /etc/apache2/sites-enabled/eems.conf ]
            then
                echo "Removing apache configuration link to eems.conf"
                rm /etc/apache2/sites-enabled/eems.conf
                echo "  Successfully removed link to eems.conf"
        fi
    else
        echo "Please run as *sudo*"
fi
