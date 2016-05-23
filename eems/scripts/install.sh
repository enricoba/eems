#!/bin/bash



# setup function
setup(){
    # create directories
    echo "Creating eems locations in /var/www/:"
    if [ -d /var/www/eems ] ; then
        echo "  Directory /var/www/eems already exists"
        echo "  Cleanup ..."
        rm -r /var/www/eems
        if [ $? -eq 0  ] ; then
            echo "  Successfully cleaned up"
        else
            echo "  Failed to clean up"
            echo -e "\e[31mSetup failed and exited\e[0m"
            exit 1
        fi
    fi

    mkdir /var/www/eems
    if [ $? -eq 0 ] ; then
        cp -r /usr/local/lib/python2.7/dist-packages/eems /var/www/eems/
        c_01=$?
        mv /var/www/eems/eems/data/eems.wsgi /var/www/eems/eems.wsgi
        c_02=$?
        if [ $c_01 -eq 0 ] && [ $c_02 -eq 0 ] ; then
            echo "  Successfully created eems directory and copied data"
        else
            echo "  Failed to copy eems data"
            echo -e "\e[31mSetup failed and exited\e[0m"
            exit 1
        fi
    else
        echo "  Failed to create eems location"
        echo -e "\e[31mSetup failed and exited\e[0m"
        exit 1
    fi

    # manage permissions for files
    # TODO permissions for var/www/eems/* files!

    # set permissions to local user
    echo "Setting up permissions for eems directories:"
    chown -R www-data:www-data /var/www/eems
    c_03=$?
    chown  root:root /var/www/eems
    c_04=$?

    if [ $c_03 -eq 0 ] && [ $c_04 -eq 0 ] ; then
        echo "  Successfully set up permissions"
    else
        echo "  Failed to set permissions"
        echo -e "\e[31mSetup failed and exited\e[0m"
        exit 1
    fi

    # copy apache2 files and enable site
    echo "Setting up apache2 configuration:"
    cp /usr/local/lib/python2.7/dist-packages/eems/data/eems.conf /etc/apache2/sites-available/
    c_05=$?
    chown root:root /etc/apache2/sites-available/eems.conf
    c_06=$?
    chmod 644 /etc/apache2/sites-available/eems.conf
    c_07=$?
    a2ensite eems.conf
    c_08=$?
    if  [ $c_05 -eq 0 ] && [ $c_06 -eq 0 ] && [ $c_07 -eq 0 ] && [ $c_08 -eq 0 ] ; then
        echo "  Successfully set up apache2 configuration"
    else
        echo "  Failed to set permissions"
        echo -e "\e[31mSetup failed and exited\e[0m"
        exit 1
    fi

    # restart apache server
    service apache2 restart
    c_10=$?
    if [ $c_10 -eq 0 ] ; then
        echo "  Successfully restarted apache2"
    else
        echo "  Failed to set permissions"
        echo -e "\e[31mSetup failed and exited\e[0m"
        exit 1
    fi

    echo -e "\e[92mSuccessfully installed eems!\e[0m"
    echo "Start monitoring at:"
    echo -e "  \e[4m\e[34mhttp://localhost/eems\e[0m"
    # TODO PRofile in Home Verzeichnis /home/user/eems abspeichern
}


if [ $USER == "root" ]
    then
        if [ -d /etc/apache2 ]
            then
                echo "apache2 is installed."
                if [ -e /etc/apache2/mods-available/wsgi.conf ]
                    then
                        echo "libapache2-mod-wsgi is installed."
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
