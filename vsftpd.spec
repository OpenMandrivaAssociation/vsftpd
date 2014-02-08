Summary:	Very Secure File Transfer Protocol Daemon
Name:		vsftpd
Version:	2.3.4
Release:	7
License:	GPLv2+
Group:		System/Servers
URL:		http://vsftpd.beasts.org/
Source0:	ftp://vsftpd.beasts.org/users/cevans/%{name}-%{version}.tar.gz
Source1:	vsftpd.xinetd
Source2:	vsftpd.pam
Source3:	vsftpd.ftpusers
Source4:	vsftpd.user_list
Source5:	vsftpd.init
Source6:	vsftpd_conf_migrate.sh
Source7:	vsftpd.service.bz2
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
# Mandriva patches
Patch101:	vsftpd-2.0.5-anon.patch
Patch102:	vsftpd-2.0.1-server_args.patch
Patch103:	vsftpd-2.2.2-use_localtime.patch
Patch104:	vsftpd-2.3.2-chowngroup.patch
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

%patch101 -p1 -b .anon
%patch102 -p1 -b .server_args
%patch103 -p1 -b .use_localtime
%patch104 -p1 -b .chowngroup

%build
%serverbuild

%make CFLAGS="%optflags" LINK="%ldflags -lcrypto"
# should go to rh patch.
# Change a few defaults in the config:
perl -pi -e 's|#ls_recurse_enable|ls_recurse_enable|' vsftpd.conf
## Fix the /usr/local problem in the xinetd entry
#perl -pi -e 's|/usr/local/sbin/vsftpd|%{_sbindir}/vsftpd|' xinetd.d/vsftpd

%install
rm -rf %buildroot

install -m755 vsftpd -D %buildroot%{_sbindir}/vsftpd
install -m600 vsftpd.conf -D %buildroot%{_sysconfdir}/vsftpd/vsftpd.conf
install -m644 vsftpd.xinetd -D %buildroot%{_sysconfdir}/xinetd.d/vsftpd-xinetd
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
%config(noreplace) %{_sysconfdir}/xinetd.d/vsftpd-xinetd

%{_mandir}/*/*





%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.4-2mdv2011.0
+ Revision: 670777
- mass rebuild

* Fri Mar 18 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.4-1
+ Revision: 646421
- 2.3.4

* Sat Oct 02 2010 Funda Wang <fwang@mandriva.org> 2.3.2-1mdv2011.0
+ Revision: 582417
- New version 2.3.2

* Wed Apr 07 2010 Funda Wang <fwang@mandriva.org> 2.2.2-4mdv2010.1
+ Revision: 532512
- rebuild

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.2-3mdv2010.1
+ Revision: 511656
- rebuilt against openssl-0.9.8m

* Mon Feb 15 2010 Frederik Himpe <fhimpe@mandriva.org> 2.2.2-2mdv2010.1
+ Revision: 506334
- Add default runlevels to the init script in order ot make sure that
  add-service rpm-helper service does not disable it on upgrade

* Thu Feb 11 2010 Frederik Himpe <fhimpe@mandriva.org> 2.2.2-1mdv2010.1
+ Revision: 504314
- Update to new version 2.2.2
- Rediff patches

* Sat Aug 01 2009 Frederik Himpe <fhimpe@mandriva.org> 2.1.2-2mdv2010.0
+ Revision: 405283
- Sync patches with Fedora. Remove patches which were merged upstream
  or merged by Fedora in another patch. This fixes vsftpd because the
  tcp_wrappers patch was disabled while tcp_wrapper were still enabled
  in the default config file

* Sat May 30 2009 Frederik Himpe <fhimpe@mandriva.org> 2.1.2-1mdv2010.0
+ Revision: 381323
- Update to new version 2.1.2
- Rediff localtime patch

  + Bruno Cornec <bcornec@mandriva.org>
    - Update to upstream 2.1.0
    - Remove now useless patches 2, 4, 5, 7, 13 and 15 in spec file

* Sun Nov 30 2008 Bruno Cornec <bcornec@mandriva.org> 2.0.7-2mdv2009.1
+ Revision: 308313
- Update tag to 2 to avoid conflicts with exiting 1 tag in 2009.0

* Fri Nov 28 2008 Bruno Cornec <bcornec@mandriva.org> 2.0.7-1mdv2009.1
+ Revision: 307433
- Fix #38452  https://qa.mandriva.com/show_bug.cgi?id=38452
- Update to 2.0.7
- Fix bug #32712 https://qa.mandriva.com/show_bug.cgi?id=32712

* Sun Aug 10 2008 Emmanuel Andry <eandry@mandriva.org> 2.0.7-1mdv2009.0
+ Revision: 270430
- New version
- fix license
- drop patch 15 (fixed upstream)
- add lsb compliant init from fedora

* Mon Jul 07 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0.5-14mdv2009.0
+ Revision: 232375
- rebuilt against new libcap

* Thu Feb 14 2008 Bruno Cornec <bcornec@mandriva.org> 2.0.5-13mdv2008.1
+ Revision: 167726
- Fix using old (now broken) PAM config. This is incompatible with previous mandriva versions and thus cannot serve as a backport use. (Cf: /usr/share/doc/pam/README.0.99.3.0.update.urpmi - Thanks O. Blin for the ref).

* Wed Jan 23 2008 Thierry Vignaud <tv@mandriva.org> 2.0.5-12mdv2008.1
+ Revision: 157278
- rebuild with fixed %%serverbuild macro

* Mon Jan 21 2008 Bruno Cornec <bcornec@mandriva.org> 2.0.5-11mdv2008.1
+ Revision: 155571
- Fix a bug with pam content for authenticated logins where it wasn't working at all

* Wed Jan 09 2008 Bruno Cornec <bcornec@mandriva.org> 2.0.5-10mdv2008.1
+ Revision: 147264
- Fix #36604: modprobe capability doesn't issue error messages anymore (fix proposed by Frederik Himpe)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Nov 20 2007 Bruno Cornec <bcornec@mandriva.org> 2.0.5-9mdv2008.1
+ Revision: 110687
- Fix #35609: connection to vsftp server fails with 500 OOPS: cap_set_proc

* Sat Sep 22 2007 Anne Nicolas <ennael@mandriva.org> 2.0.5-8mdv2008.0
+ Revision: 92224
- rebuild after failure

* Wed Jul 04 2007 Andreas Hasenack <andreas@mandriva.com> 2.0.5-7mdv2008.0
+ Revision: 48263
- rebuild with new serverbuild macro (-fstack-protector-all)

  + Bruno Cornec <bcornec@mandriva.org>
    - Hare is the related patch file
    - Add support for a new option (chown_groupname) for vsftpd

* Wed May 02 2007 Bruno Cornec <bcornec@mandriva.org> 2.0.5-5mdv2008.0
+ Revision: 20647
- Addition of the relative patch
- Fix a bug where anon_umask wasn't taken in account during uploads for the anon account

* Fri Apr 27 2007 Bruno Cornec <bcornec@mandriva.org> 2.0.5-4mdv2008.0
+ Revision: 18546
- Updated tag to 4
- Add fedora's background patch to allow for a correct startup
- Fix bug #28868 by using daemon as in fedora


* Wed Feb 07 2007 Bruno Cornec <Bruno.Cornec@mandriva.org> 2.0.5-3mdv2007.0
+ Revision: 117184
- Revert previous modification as the patch was already done in the config file of vsftpd (but patch wasn't closed)
- Add a patch for vsftpd to solve bug #15989, by changing the pam config file name from ftp to vsftpd
- vsftpd init script now LSB compliant (Fix: http://qa.mandriva.com/show_bug.cgi?id=28333)

* Thu Aug 10 2006 Bruno Cornec <Bruno.Cornec@mandriva.org> 2.0.5-2mdv2007.0
+ Revision: 54797
- Forgot to include sysstr.h for str_getpwnam declaration

* Thu Aug 10 2006 Bruno Cornec <Bruno.Cornec@mandriva.org> 2.0.5-1mdv2007.0
+ Revision: 54685
- Updated to 2.0.5 + modification of anon.patch accordingly
- import vsftpd-2.0.4-2mdv2007.0

* Tue May 30 2006 Bruno Cornec <bcornec@mandriva.org> 2.0.4-2mdk
- xinetd is not mandatory.
- xinetd conf file delivered (off by default)

* Fri Mar 10 2006 Jerome Soyer <saispo@mandriva.org> 2.0.4-1mdk
- New release 2.0.4

* Fri Mar 03 2006 Michael Scherer <misc@mandriva.org> 2.0.3-3mdk
- add avahi service discovery file 
- fix pam stack
- fix PreReq

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.3-2mdk
- rebuilt against openssl-0.9.8a

* Mon Jun 13 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.0.3-1mdk
- 2.0.3
- compile with $RPM_OPT_FLAGS
- fix executable-marked-as-config-file
- %%{1}mdv2007.1

* Wed Mar 09 2005 Daouda LO <daouda@mandrakesoft.com> 2.0.2-3mdk
o Wed Mar  9 2005 Daouda LO <daouda@mandrakesoft.com> 2.0.2-2mdk
   - s/vsftpd/proftpd/ in post_service 

 o Wed Mar  9 2005 Daouda LO <daouda@mandrakesoft.com> 2.0.2-1mdk
  - 2.0.2
  - import fedora patches
   x use xferlog for upload/download logging
   x build with tcp_wrappers, pam and ssl support
   x mv all conf file to /etc/vsftpd.conf
   x standalone vsftpd init script
   x ship with migration script
  - mv xinetd file to docdir

* Sat Nov 13 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.0.1-3mdk
- fix buildrequires

* Tue Oct 12 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.1-2mdk
- put back lib64 fix erroneously removed from last release

* Tue Jul 27 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.0.1-1mdk
- 2.0.1
- drop P0 (fixed upstream)
- cosmetics

* Wed Apr 28 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.2.2-1mdk
- macros
- removed redundant requires
- Anne Nicolas <ennael@mandrake.org> 
 - release 1.2.2 (bug fixes)
 - fix unstability under extreme load

