%define name	vsftpd
%define version	2.0.5
%define	rel	4
%define	release	%mkrel %{rel}

Summary:	Very Secure File Transfer Protocol Daemon
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://vsftpd.beasts.org/
Source0:	ftp://vsftpd.beasts.org/users/cevans/%{name}-%{version}.tar.bz2
Source1:	vsftpd.xinetd
Source2:	vsftpd.pam
Source3:	vsftpd.ftpusers
Source4:	vsftpd.user_list
Source5:	vsftpd.init
Source6:	vsftpd_conf_migrate.sh
Source7:    vsftpd.service.bz2
Patch1:		vsftpd-1.1.3-rh.patch
Patch2:		vsftpd-1.0.1-missingok.patch
Patch3:		vsftpd-2.0.5-anon.patch
Patch4:		vsftpd-2.0.1-lib64.patch
Patch5:		vsftpd-2.0.1-tcp_wrappers.patch
Patch6:		vsftpd-1.5.1-libs.patch
Patch7:		vsftpd-2.0.2-signal.patch
Patch8:		vsftpd-1.2.1-conffile.patch
Patch9:		vsftpd-2.0.1-build_ssl.patch
Patch10:	vsftpd-2.0.1-server_args.patch
Patch11:	vsftpd-2.0.1-dir.patch
Patch12:	vsftpd-2.0.1-use_localtime.patch
Patch13:	vsftpd-1.2.1-nonrootconf.patch
Patch14:	vsftpd-2.0.3-background.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
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
BuildRequires:	libcap-devel openssl-devel pam-devel tcp_wrappers-devel

%description
A Very Secure FTP Daemon - written from scratch - by Chris "One Man Security
Audit Team" Evans.

%prep
%setup -q
%patch1   -p1 -b .orig
%patch2   -p1 -b .mok
%patch3   -p1 -b .anon
%patch4   -p1 -b .lib64
cp %{SOURCE1} .
%patch5   -p1 -b .tcp_wrap
%patch6   -p1 -b .libs
%patch7   -p1 -b .signal
%patch8   -p1
%patch9  -p1 -b .build_ssl
%patch10  -p1 -b .servers_args
%patch11  -p1 -b .dir
%patch12  -p1 -b .use_localtime
%patch13  -p1 -b .nonroot
%patch14  -p1 -b .background

%build
%serverbuild

%make CFLAGS="$RPM_OPT_FLAGS"
# should go to rh patch.
# Change a few defaults in the config:
perl -pi -e 's|#ls_recurse_enable|ls_recurse_enable|' vsftpd.conf
## Fix the /usr/local problem in the xinetd entry
#perl -pi -e 's|/usr/local/sbin/vsftpd|%{_sbindir}/vsftpd|' xinetd.d/vsftpd

%install
rm -rf %buildroot

install -m755 vsftpd -D %buildroot%{_sbindir}/vsftpd
install -m600 vsftpd.conf -D %buildroot%{_sysconfdir}/vsftpd/vsftpd.conf
install -m644 vsftpd.xinetd -D %buildroot%{_sysconfdir}/xinetd.d/vsftpd
install -m644 vsftpd.conf.5 -D %buildroot/%{_mandir}/man5/vsftpd.conf.5
install -m644 vsftpd.8 -D %buildroot%{_mandir}/man8/vsftpd.8
install -m644 RedHat/vsftpd.log -D %buildroot%{_sysconfdir}/logrotate.d/vsftpd
install -m644 %{SOURCE2}  -D %buildroot%{_sysconfdir}/pam.d/vsftpd
install -m600 %{SOURCE3}  -D %buildroot%{_sysconfdir}/vsftpd/ftpusers
install -m600 %{SOURCE4}  -D %buildroot%{_sysconfdir}/vsftpd/user_list
install -m 755 %{SOURCE5} -D %buildroot%{_initrddir}/vsftpd
install -m 744 %{SOURCE6} -D %buildroot%{_sysconfdir}/vsftpd/vsftpd_conf_migrate.sh

mkdir -p %buildroot/%{_sysconfdir}/avahi/services/
bzcat %{SOURCE7} > %buildroot/%{_sysconfdir}/avahi/services/%{name}.service
 
touch %buildroot%{_sysconfdir}/vsftpd/banned-emails
touch %buildroot%{_sysconfdir}/vsftpd/chroot-list
mkdir -p %buildroot/var/ftp/pub

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

%clean
rm -rf %buildroot

%files
%defattr(-, root, root)
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
%config(noreplace) %{_sysconfdir}/xinetd.d/vsftpd

%{_mandir}/*/*



