%define name	pop-before-smtp
%define version 1.41
%define release 1

Summary:	Watch log for pop/imap auth, notify Postfix to allow relay
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source:		http://prdownloads.sourceforge.net/popbsmtp/pop-before-smtp-%{version}.tar.bz2
URL:		http://popbsmtp.sourceforge.net/
License:	BSD like
Group:		System/Servers
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prereq:		rpm-helper

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
rm -rf $RPM_BUILD_ROOT
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
%attr(0755, root, root) %{_sbindir}/pop-before-smtp
%attr(0755, root, root) %config(noreplace) %{_initrddir}/pop-before-smtp
%attr(0755, root, root) %config(noreplace) %{_sysconfdir}/pop-before-smtp-conf.pl

