#!/bin/bash


if [ $USER == "root" ]
    then
        # create directories
        mkdir /var/www/eems
        mkdir /var/www/eems/eems
        mkdir /var/www/eems/eems/data

        # copy WSGI script
        cp /usr/local/lib/python2.7/dist-packages/eems/data/eems.wsgi /var/www/eems/

        # copy database files
        cp -a /usr/local/lib/python2.7/dist-packages/eems/data/db /var/www/eems/eems/data/

        # copy python modules
        cp -a /usr/local/lib/python2.7/dist-packages/eems/support /var/www/eems/eems/
        cp -a /usr/local/lib/python2.7/dist-packages/eems/sensors /var/www/eems/eems/

        # copy init file
        cp /usr/local/lib/python2.7/dist-packages/eems/__init__.py /var/www/eems/eems/

        # copy templates and static files
        cp -a /usr/local/lib/python2.7/dist-packages/eems/static /var/www/eems/eems/
        cp -a /usr/local/lib/python2.7/dist-packages/eems/templates /var/www/eems/eems/

        # manage permissions for files
        # TODO permissions for var/www/eems/* files!

        # set permissions to local user
        chown -R www-data:www-data /var/www/eems
        chown  root:root /var/www/eems

        # copy apache2 files and enable site
        cp /usr/local/lib/python2.7/dist-packages/eems/data/eems.conf /etc/apache2/sites-available/
        chown root:root /etc/apache2/sites-available/eems.conf
        chmod 644 /etc/apache2/sites-available/eems.conf
        a2ensite eems.conf

        # add host "eems"
        echo "127.0.0.1       eems" >> /etc/hosts

        # restart apache server
        service apache2 restart

    else
        echo "Please run as *sudo*"
fi
