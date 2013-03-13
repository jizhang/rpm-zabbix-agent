Summary: Zabbix Agent
Name: zabbix-agent
Version: 2.0.5
Release: 1
Group: Networking/Admin
Source: zabbix-2.0.5.tar.gz
Packager: Ji ZHANG <jizhang@anjuke.com>
License: GPLv2
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%define prefix /usr/local/zabbix-agent

%description
Zabbix Agent

%prep
cd $RPM_BUILD_DIR
rm -fr zabbix-2.0.5
tar zxf $RPM_SOURCE_DIR/zabbix-2.0.5.tar.gz
patch -p0 < $RPM_SOURCE_DIR/path.patch

%build
cd $RPM_BUILD_DIR/zabbix-2.0.5
./configure --prefix=%{prefix} --enable-agent

%install
cd $RPM_BUILD_DIR/zabbix-2.0.5
make install DESTDIR=$RPM_BUILD_ROOT
install -D -m0755 $RPM_SOURCE_DIR/zabbix_agentd $RPM_BUILD_ROOT/etc/init.d/zabbix_agentd
mkdir -p $RPM_BUILD_ROOT/%{prefix}/var

%clean
rm -fr $RPM_BUILD_ROOT

%files
%dir %{prefix}
%{prefix}/bin
%{prefix}/sbin
%dir %{prefix}/etc
%config(noreplace) %{prefix}/etc/*.conf
%config(noreplace) %{prefix}/etc/*.conf.d
%{prefix}/share
%attr(755,zabbix,zabbix) %{prefix}/var
%attr(755,root,root) /etc/init.d/zabbix_agentd

%post
if [ $1 -eq 1 ]; then
    user_check="`grep zabbix /etc/passwd | wc -l`"
    group_check="`grep zabbix /etc/group | wc -l`"

    if [[ $user_check -eq 0 ]];
    then
        groupadd zabbix
    fi

    if [[ $group_check -eq 0 ]];
    then
        useradd -M -s /sbin/nologin -g zabbix zabbix
    fi

    chkconfig --add zabbix_agentd
    chkconfig --level 345 zabbix_agentd on
    service zabbix_agentd start
fi

%preun
if [ $1 -eq 0 ]; then
    service zabbix_agentd stop
    chkconfig --del zabbix_agentd
fi

%postun
if [ $1 -ge 1 ]; then
    service zabbix_agentd condrestart
fi

