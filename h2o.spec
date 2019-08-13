%define __jar_repack 0
%define _prefix /opt
%define debug_package %{nil}

Summary: H2O Ai Platform
Name: h2o
Version: %{h2o_version}.%{h2o_release}
Release: %{build_number}%{?dist}
License: Apache License, Version 2.0
Group: Applications
Source0:  https://h2o-release.s3.amazonaws.com/h2o/master/%{h2o_release}/h2o-%{h2o_version}.%{h2o_release}.tar.gz
URL: http://www.h2o.ai
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prefix: /opt
Requires: java >= 1.8
Requires(pre): shadow-utils
Requires: zookeeper >= 3.3.4

Vendor: Apache Software Foundation
Packager: Ivan Dyachkov <ivan.dyachkov@klarna.com>
Provides: h2o

%description
H2O Ai Platform


%prep
%setup -n %{tarball_name}

%build
rm -f libs/*

%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/h2o-%{version}
mkdir $RPM_BUILD_ROOT%{_prefix}/h2o-%{version}/bin
cp -rf * $RPM_BUILD_ROOT%{_prefix}/h2o-%{version}/.
%if ( 0%{?rhel} && 0%{?rhel} <= 6 )
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
# install -m 755 bin/h2o.sh $RPM_BUILD_ROOT/etc/rc.d/init.d/h2o
%else
mkdir -p $RPM_BUILD_ROOT/etc/systemd/system/
# install -m 644 bin/h2o.service $RPM_BUILD_ROOT/etc/systemd/system/
%endif
mkdir -p $RPM_BUILD_ROOT/var/log/h2o

%clean
rm -rf $RPM_BUILD_ROOT

%pre

# Create user and group
getent group h2o >/dev/null || groupadd -r h2o
getent passwd h2o >/dev/null || \
			 useradd -r -g h2o -d /opt/h2o -s /bin/bash \
			  -c "OrientDB Account" h2o

exit 0

%post
alternatives --install /opt/h2o h2ohome /opt/%{name}-%{version} %{int_version}

if [ $1 = 1 ]; then
    /sbin/chkconfig --add h2ohome
fi

if [ -d "/opt/h2o" ]; then
	echo -n "Copying previous configs... "
	cp -rf /opt/h2o/config/* /opt/%{name}-%{version}/config/ 2>/dev/null
	echo "done."
fi
alternatives --install /opt/h2o h2ohome  /opt/%{name}-%{version} %{int_version}

%preun
# When the last version of a package is erased, $1 is 0
if [ $1 = 0 ]; then
    /sbin/service h2o stop >/dev/null
    /sbin/chkconfig --del h2o
fi

%postun
# When the last version of a package is erased, $1 is 0
# Otherwise it's an upgrade and we need to restart the service
if [ $1 -ge 1 ]; then
    /sbin/service h2o stop >/dev/null 2>&1
    sleep 1
    /sbin/service h2o start >/dev/null 2>&1
fi

alternatives --remove h2ohome  /opt/%{name}-%{version}



%files
%defattr(-,root,root)
%attr(0755,h2o,h2o) %dir /opt/h2o-%{version}
%attr(0755,h2o,h2o) /opt/h2o-%{version}/*

%if ( 0%{?rhel} && 0%{?rhel} <= 6 )
# %attr(0775,root,orientdb) /etc/rc.d/init.d/orientdb
%else
# %attr(0775,root,orientdb) /etc/systemd/system/orientdb.service
%endif

%attr(0755,h2o,h2o) %dir /var/log/h2o

