%define name	pop-before-smtp
%define version 1.42
%define release 3

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Watch log for pop/imap auth, notify Postfix to allow relay
License:	BSD like
Group:		System/Servers
URL:		http://popbsmtp.sourceforge.net/
Source:		http://prdownloads.sourceforge.net/popbsmtp/pop-before-smtp-%{version}.tar.bz2
Requires(pre):		rpm-helper
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Spam prevention requires preventing open relaying through email
servers. However, legit users want to be able to relay. If legit
users always stayed in one spot, they'd be easy to describe to the
daemon. However, what with roving laptops, logins from home, etc.,
legit users refuse to stay in one spot.

pop-before-smtp watches the mail log, looking for successful
pop/imap logins, and posts the originating IP address into a
database which can be checked by Postfix, to allow relaying for
people who have recently downloaded their email.

%prep
%setup -q
#%patch1 -p 1 -b .init-with-reload-and-maillog-location
perl -pi -e 's|/var/log/maillog|/var/log/mail/info|' README pop-before-smtp pop-before-smtp-conf.pl pop-before-smtp.init
%build
rm -rf %{buildroot}
pod2man pop-before-smtp > pop-before-smtp.8 2>/dev/null

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_initrddir},%{_sysconfdir},%{_sbindir},%{_mandir}/man8}
#cp pop-before-smtp.init	%{buildroot}%{_initrddir}/pop-before-smtp
cp contrib/init-redhat-alex	%{buildroot}%{_initrddir}/pop-before-smtp
cp pop-before-smtp-conf.pl	%{buildroot}%{_sysconfdir}
cp pop-before-smtp		%{buildroot}%{_sbindir}
cp pop-before-smtp.8		%{buildroot}%{_mandir}/man8

%post
%_post_service pop-before-smtp

%preun
%_post_service pop-before-smtp

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc README TODO COPYING contrib
%doc %{_mandir}/man8/*
%{_sbindir}/pop-before-smtp
%config(noreplace) %{_initrddir}/pop-before-smtp
%config(noreplace) %{_sysconfdir}/pop-before-smtp-conf.pl


%changelog
* Tue Sep 15 2009 Thierry Vignaud <tvignaud@mandriva.com> 1.42-2mdv2010.0
+ Revision: 441907
- rebuild

* Sun Jan 04 2009 Jérôme Soyer <saispo@mandriva.org> 1.42-1mdv2009.1
+ Revision: 324286
- New upstream release

* Fri Aug 01 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.41-4mdv2009.0
+ Revision: 259209
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.41-3mdv2009.0
+ Revision: 247132
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Dec 07 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.41-1mdv2008.1
+ Revision: 116178
- spec cleanup
- update to new version 1.41
- import pop-before-smtp


* Thu Jan 06 2005 Tibor Pittich <Tibor.Pittich@mandrake.org> 1.36-2mdk
- add config file into package

* Sun Nov 14 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.36-1mdk
- 1.36
- wipe out buildroot at the beginning of %%install

* Tue May  4 2004 Michael Scherer <misc@mandrake.org> 1.34-1mdk
- New release 1.34
- remove patch1, replaced by a perl oneliner
- clean Requires

* Tue Feb 24 2004 Lenny Cartier <lenny@mandrakesoft.com> 1.32-2mdk
- rebuild

* Fri Dec 27 2002 Alexander Skwar <ASkwar@DigitalProjects.com> 1.32-1mdk
- Updated URL
- 1.32

* Fri Mar  1 2002 Alexander Skwar <ASkwar@DigitalProjects.com> 1.28-1mdk
- First release for Mandrake Linux

