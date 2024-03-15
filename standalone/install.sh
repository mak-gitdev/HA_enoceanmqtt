#!/bin/sh

#==================================================
# UTILITIES
#==================================================
usage ()
{
    printf "Usage:\n"
    printf "   ./install.sh [-b <branch> | --branch <branch>] | [-v <version> | --version <version>] [-d <install_dir> | --dir <install_dir>]\n"
    printf "\n"
    printf "<branch> :\n"
    printf "   develop       : Install the HEAD of the development branch\n"
    printf "   master        : Install the HEAD of the master branch (stable) (not recommended at the moment)\n"
    printf "   support-eltako: Install the HEAD of the support-eltako branch (only for tests purposes)\n"
    printf "\n"
    printf "<version>        : The version to install. Mutually exclusive with <branch>\n"
    printf "\n"
    printf "<install_dir>    : The installation directory. If not specified, './' is used\n"
    printf "\n"
}


package_install()
{
    printf "\n==================================================\n"
    printf "Install %s\n\n" $1
    pip3 install --user $1
    printf "\n"
}

#==================================================
# CHECK USER
#==================================================
if [ "$(id -u)" = "0" ]; then
    printf "[ERROR]: Install script should not be run as root. Do not use sudo nor log as root user to run the script.\n"
    exit 1
fi

#==================================================
# SAVE CURRENT DIRECTORY
#==================================================
CALL_DIR=$(pwd)

#==================================================
# GET USER OPTIONS
#==================================================
BRANCH=
VERSION=
INSTALL_DIR="./"

while [ $# -gt 0 ]; do
  case "$1" in
    -b | --branch )  BRANCH="$2"                         ; shift 2 ;;
    -v | --version ) VERSION="$2"                        ; shift 2 ;;
    -d | --dir )     INSTALL_DIR="$2"                    ; shift 2 ;;
    -h | --help )                                  usage ; exit  0 ;;
    * )              printf "Unknown option $1\n"; usage ; exit  1 ;;
  esac
done

#==================================================
# CHECK OPTIONS
#==================================================
printf "\n"
printf "VERSION = ${VERSION}\nBRANCH= ${BRANCH}\nINSTALL_DIR= ${INSTALL_DIR}\n\n"

if [ "${VERSION:+true}" = "${BRANCH:+true}" ]; then
    printf "[ERROR]: Please indicate either the version or the branch to install.\n\n"
    exit 1
fi

if [ ! -z "${BRANCH}" ] && [ "${BRANCH}" != "master" ] && [ "${BRANCH}" != "develop" ] && [ "${BRANCH}" != "support-eltako" ]; then
    printf "[ERROR]: Unknown branch ${BRANCH}\n"
    exit 1
fi

if [ ! -z "${BRANCH}" ]; then
    printf "[INFO]: Installer will install HEAD of branch %s in directory %s\n" ${BRANCH} ${INSTALL_DIR}
else
    printf "[INFO]: Installer will install version %s in directory %s\n" ${VERSION##--} ${INSTALL_DIR}
fi

#==================================================
# INSTALLATION
#==================================================
printf "\n==================================================\n"
printf "Entering install directory: ${INSTALL_DIR}\n\n"
cd ${INSTALL_DIR}

package_install pyyaml==6.0.1
package_install tinydb==4.7.1

printf "\n==================================================\n"
printf "Install Custom Python EnOcean Library\n\n"
pip3 install --user --force-reinstall git+https://github.com/mak-gitdev/enocean.git

printf "\n==================================================\n"
printf "Install enocean-mqtt\n\n"
rm -rf enocean-mqtt
git clone -b master --single-branch --depth 1 https://github.com/embyt/enocean-mqtt.git
cd enocean-mqtt && pip3 install --user -e . && cd ..

printf "\n==================================================\n"
printf "Install Home Assistant overlay\n\n"
if [ ! -z "${BRANCH}" ]; then
    printf "Installing HEAD of branch %s\n" ${BRANCH}
    git clone -b ${BRANCH} --single-branch --depth 1 https://github.com/mak-gitdev/HA_enoceanmqtt.git
    printf "Date: $(date '+%Y-%m-%d %H:%M:%S')\nBranch: ${BRANCH}\n" > HA_enoceanmqtt/enoceanmqtt/overlays/homeassistant/VERSION
    cd HA_enoceanmqtt && printf "Commit ID: $(git rev-parse --short HEAD)" >> enoceanmqtt/overlays/homeassistant/VERSION && cd ..
else
    if [ -z "${VERSION##*.*.*}" ]; then
        printf "Installing development version ${VERSION%-*}\n"
    else
        printf "Installing stable version ${VERSION%-*}\n"
    fi
    wget -nv -O "app.tar.gz" "https://github.com/mak-gitdev/HA_enoceanmqtt/archive/refs/tags/${VERSION%-*}.tar.gz" && \
    printf "Extracting app.tar.gz\n" && tar xzf "app.tar.gz" && rm "app.tar.gz" && \
    mv -v "HA_enoceanmqtt-${VERSION%-*}" HA_enoceanmqtt && \
    printf "Date: $(date '+%Y-%m-%d %H:%M:%S')\nVersion: ${VERSION}\n" > HA_enoceanmqtt/enoceanmqtt/overlays/homeassistant/VERSION
fi
cp -rf HA_enoceanmqtt/enoceanmqtt enocean-mqtt
cp -f  HA_enoceanmqtt/standalone/enoceanmqtt* enocean-mqtt
rm -rf HA_enoceanmqtt

printf "\n==================================================\n"
printf "Going back to installer directory: ${CALL_DIR}\n\n"
cd ${CALL_DIR}
