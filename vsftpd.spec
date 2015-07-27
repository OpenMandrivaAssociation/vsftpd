Summary:	Very Secure File Transfer Protocol Daemon

Name:		vsftpd
Version:	3.0.3
Release:	1
License:	GPLv2+
Group:		System/Servers
URL:		http://vsftpd.beasts.org/
Source0:	https://security.appspot.com/downloads/%{name}-%{version}.tar.gz
Source10:	https://security.appspot.com/downloads/%{name}-%{version}.tar.gz.asc
Source1:	vsftpd.xinetd
Source2:	vsftpd.pam
Source3:	vsftpd.ftpusers
Source4:	vsftpd.user_list
Source5:	vsftpd.init
Source6:	vsftpd_conf_migrate.sh
Source7:	vsftpd.service.bz2
Source8:	vsftpd.service
# Fedora patches
# Build patches
Patch1:		vsftpd-2.1.0-libs.patch
Patch2: 	vsftpd-2.1.0-build_ssl.patch
Patch3: 	vsftpd-2.1.0-tcp_wrappers.patch
# Use /etc/vsftpd/ instead of /etc/
Patch4:		vsftpd-2.2.2-configuration.patch
# These need review
Patch5: 	vsftpd-2.2.2-pam_hostname.patch
Patch6: 	vsftpd-close-std-fds.patch
Patch7: 	vsftpd-2.1.0-filter.patch
Patch8: 	vsftpd-2.0.5-greedy.patch
Patch9: 	vsftpd-2.1.0-userlist_log.patch
Patch10:	vsftpd-2.2.2-trim.patch
Patch12: 	vsftpd-2.2.2-daemonize_plus.patch
Patch13:	vsftpd-2.3.4-listen_ipv6.patch
Patch101:	vsftpd-2.0.5-anon.patch
Patch102:	vsftpd-2.0.1-server_args.patch
Patch103:	vsftpd-2.2.2-use_localtime.patch
Patch104:	vsftpd-3.0.2-chowngroup.patch
Patch105:	vsftpd-drop-newpid-from-clone.patch
Requires(pre):		rpm-helper
Requires(post):    	rpm-helper
Requires(postun):  	rpm-helper
Requires(preun):    rpm-helper
Requires:	pam >= 0.59, libcap, openssl, logrotate
Provides:	ftpserver
Conflicts:	wu-ftpd
Conflicts:	proftpd
Conflicts:	ncftpd
Conflicts:	pure-ftpd
BuildRequires:	libcap-devel
BuildRequires:	pam-devel
BuildRequires:	openssl-devel
BuildRequires:	tcp_wrappers-devel

%description
A Very Secure FTP Daemon - written from scratch - by Chris "One Man Security
Audit Team" Evans.

%prep
%setup -q
cp %{SOURCE1} .
%patch1 -p1 -b .libs
%patch2 -p1 -b .build_ssl
%patch3 -p1 -b .tcp_wrappers
%patch4 -p1 -b .configuration
%patch5 -p1 -b .pam_hostname
%patch6 -p1 -b .close_fds
%patch7 -p1 -b .filter
%patch8 -p1 -b .greedy
%patch9 -p1 -b .userlist_log
%patch10 -p1 -b .trim
%patch12 -p1 -b .daemonize_plus
%patch13 -p1 -b .ipv6

%patch101 -p1 -b .anon
%patch102 -p1 -b .server_args
%patch103 -p1 -b .use_localtime
%patch104 -p1 -b .chowngroup
%patch105 -p1 -b .newpid

%build
%serverbuild

%make CFLAGS="%{optflags}" LINK="%{ldflags}"
# should go to rh patch.
# Change a few defaults in the config:
perl -pi -e 's|#ls_recurse_enable|ls_recurse_enable|' vsftpd.conf
## Fix the /usr/local problem in the xinetd entry
#perl -pi -e 's|/usr/local/sbin/vsftpd|%{_sbindir}/vsftpd|' xinetd.d/vsftpd

%install
install -m755 vsftpd -D %{buildroot}%{_sbindir}/vsftpd
install -m600 vsftpd.conf -D %{buildroot}%{_sysconfdir}/vsftpd/vsftpd.conf
install -m644 vsftpd.xinetd -D %{buildroot}%{_sysconfdir}/xinetd.d/vsftpd-xinetd
install -m644 vsftpd.conf.5 -D %{buildroot}/%{_mandir}/man5/vsftpd.conf.5
install -m644 vsftpd.8 -D %{buildroot}%{_mandir}/man8/vsftpd.8
install -m644 RedHat/vsftpd.log -D %{buildroot}%{_sysconfdir}/logrotate.d/vsftpd
install -m644 %{SOURCE2}  -D %{buildroot}%{_sysconfdir}/pam.d/vsftpd
install -m600 %{SOURCE3}  -D %{buildroot}%{_sysconfdir}/vsftpd/ftpusers
install -m600 %{SOURCE4}  -D %{buildroot}%{_sysconfdir}/vsftpd/user_list
install -m 755 %{SOURCE5} -D %{buildroot}%{_initrddir}/vsftpd
install -m 744 %{SOURCE6} -D %{buildroot}%{_sysconfdir}/vsftpd/vsftpd_conf_migrate.sh
install -m644 %{SOURCE8} -D %{buildroot}/lib/systemd/system/vsftpd.service

mkdir -p %{buildroot}/%{_sysconfdir}/avahi/services/
bzcat %{SOURCE7} > %{buildroot}/%{_sysconfdir}/avahi/services/%{name}.service
 
touch %{buildroot}%{_sysconfdir}/vsftpd/banned-emails
touch %{buildroot}%{_sysconfdir}/vsftpd/chroot_list
mkdir -p %{buildroot}/var/ftp/pub

%post
%_post_service vsftpd
if [ -x /usr/sbin/xinetd ];then
%_post_service xinetd
fi

%pre
%_pre_useradd ftp /var/ftp /bin/false

%postun
%_postun_userdel ftp

%preun
%_preun_service vsftpd
if [ -x /usr/sbin/xinetd ];then
%_post_service xinetd
fi

%files
%doc FAQ INSTALL BUGS AUDIT Changelog LICENSE README README.security REWARD SPEED TODO 
%doc BENCHMARKS COPYING SECURITY/ EXAMPLE/ TUNING SIZE vsftpd.xinetd
%{_sbindir}/vsftpd
%{_initrddir}/vsftpd
%attr(0555,ftp,ftp) %dir /var/ftp
%attr(2555,ftp,ftp) %dir /var/ftp/pub
%attr(700,root,root) %dir %{_sysconfdir}/vsftpd
%config(noreplace) %{_sysconfdir}/vsftpd/*
%config(noreplace) %{_sysconfdir}/pam.d/vsftpd
%config(noreplace) %{_sysconfdir}/logrotate.d/vsftpd
%config(noreplace) %{_sysconfdir}/avahi/services/%{name}.service
%config(noreplace) %{_sysconfdir}/xinetd.d/vsftpd-xinetd
/lib/systemd/system/vsftpd.service
%{_mandir}/*/*
