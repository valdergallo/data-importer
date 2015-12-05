# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|

  # proxy config
  if Vagrant.has_plugin?("vagrant-proxyconf")
    # config.proxy.http     = "http://87.254.212.121:8080"
    # config.proxy.https    = "http://87.254.212.121:8080"
    config.proxy.no_proxy = "localhost,127.0.0.1"
  end

  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "hashicorp/precise32"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 8010, host: 8010

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update -y
    sudo apt-get install -y python-setuptools
    sudo apt-get install -y python-dev
    sudo apt-get install -y build-essential
    sudo apt-get install -y git
    sudo apt-get install -y sqlite
    sudo apt-get install -y vim
    sudo easy_install virtualenv
    sudo easy_install pip
    sudo easy_install virtualenvwrapper
    # config default programs
    wget -O ~/.vimrc https://gist.githubusercontent.com/valdergallo/2979412/raw/84f99d85dcc7d8 9d38cb79ad58e1a08a99db58ad/vimrc
    wget -O ~/.screenrc https://gist.githubusercontent.com/valdergallo/2979409/raw/59d3e9c14d417977bed5071c6226d55acf43cec6/screenrc
    wget -O ~/.gitconfig https://gist.githubusercontent.com/valdergallo/3427676/raw/da8224e818d12fdbaa366747b92a02b25f2fa70d/.gitconfig
    mkdir ~/.vim
    source /usr/local/bin/virtualenvwrapper.sh
    echo "source /usr/local/bin/virtualenvwrapper.sh " >> ~/.bashrc
    ln -s /vagrant work_home
  SHELL
end
