#!/bin/sh

usage ()
{
    printf "Usage:\n"
    printf "   ./install.sh <version> [install_dir]\n"
    printf "\n"
    printf "<version> :\n"
    printf "   --dev   : Install the latest development version\n"
    printf "   --stable: Install the latest stable version (not recommended at the moment)\n"
    printf "\n"
    printf "[install_dir]: The installation directory. If not specified, './' is used\n"
    printf "\n"
}


package_install()
{
    printf "\nCheck if %s is installed ... " $1
    pip3 show $1 > /dev/null 2>&1
    if [ $? -eq 1 ]; then
        printf "NO\n"
        printf "==================================================\n"
        printf "===> Install %s\n" $1
        pip3 install --user $1
    else
        printf "OK !\n"
        printf "==================================================\n"
    fi
}

if [ $# -eq 0 ]; then
    usage
fi

CALL_DIR=$(pwd)
VERSION=$1
INSTALL_DIR=$2

if [ "${VERSION}" != "--dev" ] && [ "${VERSION}" != "--stable" ]; then
    printf "Unknown version: %s\nExiting\n" ${VERSION}
    exit 1
fi

if [ -z ${INSTALL_DIR} ]; then
    INSTALL_DIR="./"
fi

printf "\nInstaller will install latest %s version in directory %s\n" ${VERSION##--} ${INSTALL_DIR}

cd ${INSTALL_DIR}

package_install pyyaml
package_install tinydb

printf "\nClone enocean-mqtt\n"
printf "==================================================\n\n"
git clone https://github.com/embyt/enocean-mqtt.git

printf "\nInstall enocean-mqtt\n"
printf "==================================================\n\n"
cd enocean-mqtt && pip3 install --user -e . && cd ..

printf "\nInstall Home Assistant overlay\n"
printf "==================================================\n\n"
if [ "${VERSION}" = "--dev" ]; then
    printf "Installing latest development version\n"
    git clone -b develop --single-branch --depth 1 https://github.com/mak-gitdev/HA_enoceanmqtt.git
else
    printf "Installing latest stable version\n"
    git clone -b master --single-branch --depth 1 https://github.com/mak-gitdev/HA_enoceanmqtt.git
fi
cp -rf HA_enoceanmqtt/enoceanmqtt enocean-mqtt
cp -rf HA_enoceanmqtt/enocean/protocol/EEP.xml $(find / -path ./HA_enoceanmqtt -prune -o -name "EEP.xml" -print -quit 2>/dev/null)
rm -rf HA_enoceanmqtt

cd ${CALL_DIR}
