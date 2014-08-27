# Mockbuilder

Mockbuilder is a tool that allows you to instanciate a virtual machine pre-configured with a working Mock environment.

It uses Vagrant and Chef to create and provision a virtual machine.

In a nutshell, Mock allows you to build RPM packages targetted to a different distribution than the one where your building the RPMs. It does this by jailing rpmbuild environments with chroot.

If you want to know more details on Vagrant, Chef or Mock, you may want to check these out:

- [Vagrant](https://docs.vagrantup.com/v2/getting-started/index.html)
- [Chef](http://www.getchef.com/chef/)
- [Mock Project](http://fedoraproject.org/wiki/Projects/Mock)

## usage

##### 1. First things first... fetch the code

```
$ git clone https://github.com/ruizink/mockbuilder.git
```

##### 2. Create and provision the VM

```
$ cd mockbuilder
$ vagrant up
```

##### 3. Login into the VM

```
$ vagrant ssh
```

## requirements

You want to make sure you have these components installed on your local machine:

- [Download VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Download Vagrant](https://www.vagrantup.com/downloads.html)
- [Download Git](http://git-scm.com/downloads)

## what can you with it ?

I assume that you're familiar with the rpmbuild process already know what Mock is. (Scroll to the top in case you've missed it)

To get things going you'll need at least 2 things with you:

- a .spec file
- the sources

##### 1. Create your _mypackage_ rpmbuild environment

```
$ cp -rp packages/buildroot.clean packages/<mypackage>
$ cd packages/<mypackage>
```

##### 2. Generate the SRPM for _mypackage_

```
$ rpmbuild -bs SPECS/<mypackage>.spec
```

##### 3. Generate _mypakcage_ RPM for the distribution that I need

```
$ mock -r <dist> SRPMS/<mypackage>-<version>-<release>.src.rpm
```

(Supported _dist_ at the moment include: el5-x86_64, el6-x86_64 and el7-x86_64)

## example

##### Generate an RPM package for tomcat7 to install on a el5-x86_64 machine

```
$ #### Create build environemnt
$ cp -rp packages/buildroot.clean packages/tomcat7
$ cd packages/tomcat7
$
$ #### Copy the spec file and sources
$ wget -P SPECS/ https://raw.github.com/nmilford/rpm-tomcat7/master/tomcat7.spec
$ wget -P SOURCES/ https://raw.github.com/nmilford/rpm-tomcat7/master/tomcat7.init
$ wget -P SOURCES/ https://raw.github.com/nmilford/rpm-tomcat7/master/tomcat7.sysconfig
$ wget -P SOURCES/ https://raw.github.com/nmilford/rpm-tomcat7/master/tomcat7.logrotate
$ wget -P SOURCES/ http://download.openpkg.org/components/cache/tomcat/apache-tomcat-7.0.41.tar.gz
$
$ #### Build the SRPM
$ rpmbuild -bs SPECS/tomcat7.spec
$
$ #### Build the RPMs for el5-x86_64
$ mock -r el5-x86_64 SRPMS/tomcat7-7.0.41-1.src.rpm
$
$ #### Check the results
$ ls -1 /var/lib/mock/el5-x86_64/result/tomcat7*.rpm
/var/lib/mock/el5-x86_64/result/tomcat7-7.0.41-1.noarch.rpm
/var/lib/mock/el5-x86_64/result/tomcat7-7.0.41-1.src.rpm

```

## author

Mário Santos
@\_ruizink\_
