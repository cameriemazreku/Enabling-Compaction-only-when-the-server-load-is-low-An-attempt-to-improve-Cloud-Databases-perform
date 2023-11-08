if [ "$#" -lt 1 ]; then
  echo "Usage: ./install_voltdb.sh INSTALLATION_PATH"
  exit 1
fi

# Install the required packages
sudo apt-get -y install build-essential python3 cmake valgrind ntp ccache gcc gcc-c++ git-all python3-httplib2 python-setuptools python3-dev apt-show-versions

#install java8
sudo apt-get install openjdk-8-jdk

# Make sure that Java 8 is the default
echo "Select Java 8"
sudo update-alternatives --config java

#install ant 
sudo apt-get install ant ant-optional

# Clone and build VoltDB
cd $1
sudo git clone https://github.com/voltdb/voltdb
cd voltdb

# Avoid "WARN: Strict java memory checking is enabled, don't do release builds
# or performance runs with this enabled. Invoke "ant clean" and "ant
# -Djmemcheck=NO_MEMCHECK" to disable."
ant -Djmemcheck=NO_MEMCHECK

PATH="$PATH:$(pwd)/bin/"
