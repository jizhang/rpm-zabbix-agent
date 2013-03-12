Summary: Zabbix Agent
Name: zabbix-agent
Version: 2.0.5
Release: 1
Group: Networking/Admin
Source: zabbix-2.0.5.tar.gz
Packager: Ji ZHANG <jizhang@anjuke.com>
License: GPLv2
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
Zabbix Agent

%prep
cd $RPM_BUILD_DIR
rm -fr zabbix-2.0.5
tar zxf $RPM_SOURCE_DIR/zabbix-2.0.5.tar.gz

%build
cd $RPM_BUILD_DIR/zabbix-2.0.5
./configure --prefix=/usr/local/zabbix-agent --enable-agent

%install
cd $RPM_BUILD_DIR/zabbix-2.0.5
make install DESTDIR=$RPM_BUILD_ROOT
install -D -m0755 $RPM_SOURCE_DIR/zabbix_agentd $RPM_BUILD_ROOT/etc/init.d/zabbix_agentd

%clean
rm -fr $RPM_BUILD_ROOT

%files
/usr/local/zabbix-agent
/etc/init.d/zabbix_agentd

%post
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

