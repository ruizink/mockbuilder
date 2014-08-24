# fail fast if arch is not x86_64
%ifnarch x86_64
echo "ERROR: unsupported architecture: %{_arch}"
exit 1
%endif

# define working directories
%define _sourcedir %{_topdir}/SOURCES/
%define _builddir %{_topdir}/BUILD/

# define architecture
%define arch 64
%define other 32

# find activemq information
#%define activemq_tar apache-activemq-5.9.1-bin.tar.gz
#%define activemq_tar http://mirrors.fe.up.pt/pub/apache/activemq/5.9.1/apache-activemq-5.9.1-bin.tar.gz
#%define activemq_version %(echo %{activemq_tar} | perl -pe 's/apache-activemq-//; s/-bin\.tar\.gz$//')
%define activemq_version 5.9.1

# deduce rpm information
%define pkg_version %{activemq_version}
%define rpm_release 5
%define rpm_version %(echo %{pkg_version} | perl -pe 's/-/_/g')

# installation settings
%define activemq_share   /etc/activemq
%define activemq_home    %{activemq_share}-%{activemq_version}
%define activemq_logs   /var/log/activemq
%define activemq_data   /var/lib/activemq

Name: activemq
Version: %{rpm_version}
Release: %{rpm_release}%{?dist}
Summary: ActiveMQ
Group: System
License: ASL 2.0
Url: http://activemq.apache.org
Source0: http://mirrors.fe.up.pt/pub/apache/activemq/%{activemq_version}/apache-activemq-%{activemq_version}-bin.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{pkgversion}-%{release}-root
BuildRequires: perl
Requires: java >= 0:1.5.0
Requires: jpackage-utils

%description
ActiveMQ is a messaging platform distributed by the Apache Foundations.

%prep
echo "ActiveMQ version: %{activemq_version}"
echo "RPM version: %{rpm_version}-%{rpm_release}%{?dist}"
cd ..
%setup -q -n apache-activemq-%{pkg_version}

%build
# symlink the wrapper binaries
for name in wrapper libwrapper.so; do
  ln -s linux-x86-%{arch}/$name bin/$name
done
# remove the unwanted binary directories
rm -fr bin/linux-x86-%{other} bin/macosx
# temporary hack to set the proper configuration paths in XML files while DEV-3055 gets fixed
grep -l '{activemq.base}/conf/' `find webapps -name '*.xml'` | while read path; do
  perl -pi -e 's#\{activemq\.base\}/conf/#{activemq.conf}/#' $path
done

%install
rm -fr %{buildroot}
mkdir -p %{buildroot}%{activemq_home}
mv * %{buildroot}%{activemq_home}
rm -f %{buildroot}%{activemq_home}/activemq-all-*.jar
mkdir -p %{buildroot}%{activemq_logs}
mkdir -p %{buildroot}%{activemq_data}

%clean
rm -fr %{buildroot}

%post
# symlink the app directory
[ -e %{activemq_share} ] && rm -f %{activemq_share} || true
ln -s %{activemq_home} %{activemq_share}

%postun
# clean all the system when uninstalled
# check whether the package is being uninstalled ($1 == 0)  or upgraded ($1 == 1)
if [[ "$1" -eq "0" ]]; then
  rm -f %{activemq_share}
fi

%preun
# remove symlinks that may have been created when patching ActiveMQ
find %{activemq_home}/lib -type l -exec rm -f \{\} \;

%files
%attr(-,root,root) %{activemq_home}
%attr(-,jboss,ldap_logbot) %{activemq_logs}
%attr(-,jboss,root) %{activemq_data}
