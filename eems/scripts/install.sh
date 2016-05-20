#!/bin/bash


setup(){
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

}


if [ $USER == "root" ]
    then
        if [ -d /etc/apache2 ]
            then
                # echo "apache2 is installed."
                if [ -f /etc/apache2/mods-available/wsgi.conf ]
                    then
                        # echo "libapache2-mod-wsgi is installed."
                        setup
                        exit 1
                    else
                        echo "libapache2-mod-wsgi is not installed."
                        read -p "Do you want to install *libapache2-mod-wsgi* automatically? (y/n) (y): " answer_1
                        case "$answer_1" in
                            Yes|yes|Y|y|"")
                                echo "install libapache2-mod-wsgi"
                                apt-get update
                                apt-get install libapache2-mod-wsgi -y
                                setup
                                ;;
                            No|no|N|n)
                                echo "Automatic installation aborted."
                                echo "To use eems, please install *libapache2-mod-wsgi* manually."
                                exit 1
                                ;;
                            *)
                                exit 1
                                ;;
                        esac
                fi
            else
                echo "apache2 is not installed."
                read -p "Do you want to install *apache2* and *libapache2-mod-wsgi* mod automatically? (y/n) (y): " answer_2
                case "$answer_2" in
                    Yes|yes|Y|y|"")
                        echo "install *apache2* and *libapache2-mod-wsgi*"
                        apt-get update
                        apt-get install apache2 libapache2-mod-wsgi -y
                        setup
                        ;;
                    No|no|N|n)
                        echo "Automatic installation aborted."
                        echo "To use eems, please install *apache2* and *libapache2-mod-wsgi* manually."
                        exit 1
                        ;;
                    *)
                        exit 1
                        ;;
                esac
        fi
    else
        echo "Please run as *sudo*."
fi
