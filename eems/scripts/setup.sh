#!/bin/bash


# setup function
setup(){
    # create HOME directories
    echo "Creating EEMS home directory:"
    if [ -d /home/$actual_user/eems ] ; then
        echo "  EEMS home directory already exists"
        echo "  using existing personal data"
        chown www-data:www-data /home/$actual_user/eems
        if [ $? -eq 0  ] ; then
            echo "  Successfully set EEMS home directory permissions"
        else
            echo "  Failed to set permissions for EEMS home directory"
            echo -e "\e[31mSetup failed and exited\e[0m"
            exit 1
        fi
    else
        mkdir /home/$actual_user/eems
        c_13=$?
        chown www-data:www-data /home/$actual_user/eems
        c_14=$?
        if [ $c_13 -eq 0 ] && [ $c_14 -eq 0 ] ; then
            echo "  Successfully created EEMS home directory"
        else
            echo "  Failed create EEMS home directory"
            echo -e "\e[31mSetup failed and exited\e[0m"
            exit 1
        fi
    fi

    # create SERVER directories
    echo "Creating EEMS server directory and copying data:"
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
            echo "  Successfully created EEMS server directory and copied data"
        else
            echo "  Failed to copy EEMS data"
            echo -e "\e[31mSetup failed and exited\e[0m"
            exit 1
        fi
    else
        echo "  Failed to create EEMS server directory"
        echo -e "\e[31mSetup failed and exited\e[0m"
        exit 1
    fi

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
    if [ -e /etc/apache2/sites-available/eems.conf ] ; then
        echo "  Apache2 config file already exists"
        echo "  Cleanup ..."
        rm /etc/apache2/sites-available/eems.conf
        c_11=$?
        rm /etc/apache2/sites-enabled/eems.conf
        c_12=$?
        if [ $c_11 -eq 0 ] && [ $c_12 -eq 0 ] ; then
            echo "  Successfully cleaned up"
        else
            echo "  Failed to clean up"
            echo -e "\e[31mSetup failed and exited\e[0m"
            exit 1
        fi
    fi
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
}


if [ $USER == "root" ] ; then
    actual_user=$1
    echo "Looking for required packages (apache2 and libapache2-mod-wsgi):"
    if [ -d /etc/apache2 ] ; then
        echo "  Successfully determined package apache2"
        if [ -e /etc/apache2/mods-available/wsgi.conf ]
            then
                echo "  Successfully determined package libapache2-mod-wsgi"
                setup
                exit 0
            else
                echo "  Failed to determine package libapache2-mod-wsgi"
                read -p "Do you want to install libapache2-mod-wsgi automatically? (y/n) (y): " answer_1
                case "$answer_1" in
                    Yes|yes|Y|y|"")
                        echo "  Running apt-get update: "
                        apt-get update
                        echo "  Installing package libapache2-mod-wsgi"
                        apt-get install libapache2-mod-wsgi -y
                        if [ $? -eq 0 ] ; then
                            echo "  Successfully installed package libapache2-mod-wsgi"
                            setup
                            exit 0
                        else
                            echo "  Failed to install package libapache2-mod-wsgi"
                            echo -e "\e[31mAutomatic installation failed\e[0m"
                            echo "Please install libapache2-mod-wsgi manually and restart the setup afterwards"
                            exit 1
                        fi
                        ;;
                    No|no|N|n)
                        echo -e "\e[31mAutomatic installation aborted\e[0m"
                        echo "Please install libapache2-mod-wsgi manually and restart the setup afterwards"
                        exit 1
                        ;;
                    *)
                        exit 1
                        ;;
                esac
        fi
    else
        echo "  Failed to determine package apache2"
        echo "  Failed to determine package libapache2-mod-wsgi"
        read -p "Do you want to install apache2 and libapache2-mod-wsgi mod automatically? (y/n) (y): " answer_2
        case "$answer_2" in
            Yes|yes|Y|y|"")
                echo "  Running apt-get update: "
                apt-get update
                echo "  Installing packages apache2 and libapache2-mod-wsgi"
                apt-get install apache2 libapache2-mod-wsgi -y
                if [ $? -eq 0 ] ; then
                    echo "  Successfully installed packages apache2 and libapache2-mod-wsgi"
                    setup
                    exit 0
                else
                    echo "  Failed to install packages apache2 and libapache2-mod-wsgi"
                    echo -e "\e[31mAutomatic installation failed\e[0m"
                    echo "Please install apache2 and libapache2-mod-wsgi manually and restart the setup afterwards"
                    exit 1
                fi
                ;;
            No|no|N|n)
                echo -e "\e[31mAutomatic installation aborted\e[0m"
                echo "Please install apache2 and libapache2-mod-wsgi manually and restart the setup afterwards"
                exit 1
                ;;
            *)
                exit 1
                ;;
        esac
    fi
else
    echo "Please run as sudo."
fi
