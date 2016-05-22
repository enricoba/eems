#!/bin/bash



# hosts function
hosts() {
    echo "127.0.0.1 eems" >> /etc/hosts
}


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
    if [ chown -R www-data:www-data /var/www/eems ] && [ chown  root:root /var/www/eems ] ; then
        echo "  Successfully set up permissions"
    else
        echo "  Failed to set permissions"
        echo -e "\e[31mSetup failed and exited\e[0m"
        exit 1
    fi

    # copy apache2 files and enable site
    echo "Setting up apache2 configuration:"
    if  [ cp /usr/local/lib/python2.7/dist-packages/eems/data/eems.conf /etc/apache2/sites-available/ ] && \
        [ chown root:root /etc/apache2/sites-available/eems.conf ] && \
        [ chmod 644 /etc/apache2/sites-available/eems.conf ] && \
        [ a2ensite eems.conf ]
    then
        echo "  Successfully set up apache2 configuration"
    else
        echo "  Failed to set permissions"
        echo -e "\e[31mSetup failed and exited\e[0m"
        exit 1
    fi


    # add host "eems"
    echo "Adding eems to hosts"
    if [ hosts ] ; then
        echo "  Successfully added eems to hosts"
    else
        echo "  Failed to set permissions"
        echo -e "\e[31mSetup failed and exited\e[0m"
        exit 1
    fi


    # restart apache server
    if [ service apache2 restart ] ; then
        echo "  Successfully restarted apache2"
    else
        echo "  Failed to set permissions"
        echo -e "\e[31mSetup failed and exited\e[0m"
        exit 1
    fi

    echo -e "\e[92mSuccessfully installed eems!\e[0m"
    echo "Start monitoring at:"
    echo -e "  \e[4m\e[34mhttp://eems"
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
