#
# rpm spec-file for cryptmount
# Copyright 2006-2014, Holger Mueller & RW Penney
#
Summary:	Let ordinary users mount an encrypted file system
Name:		cryptmount
Version: 	5.0
Release:	1
License:	GPL
URL:		http://cryptmount.sourceforge.net
Group:		System/Filesystems
Source0:	http://sourceforge.net/projects/cryptmount/files/cryptmount-%{version}/%{name}-%{version}.tar.gz
BuildRequires:  libcryptsetup-devel libgcrypt-devel 
Requires:	libcryptsetup libgcrypt device-mapper
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
cryptmount is a utility for the GNU/Linux operating system which allows
an ordinary user to mount an encrypted filing system without requiring
superuser privileges. Filesystems can reside on raw disk partitions or
ordinary files, with cryptmount automatically configuring 
device-mapper and loopback devices before mounting.


%prep
%setup -n %{name}-%{version}
%{__perl} -pi.orig -e '
	s|^(\s*)chown(\s*root)|\1#chown\2|g;
	s|/etc/init.d|%{_initrddir}|g;
    ' Makefile.am Makefile.in


%build
%configure --enable-delegation --enable-fsck
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__install} -d -m0755 %{buildroot}%{_initrddir}
%{__install} -d -m0755 %{buildroot}%{_sbindir}
%{__install} -d -m0755 %{buildroot}/etc/modules-load.d
%{__install} -d -m0755 %{buildroot}/usr/lib/systemd/system
%{__make} DESTDIR=%{buildroot} install
%find_lang %{name}


%clean
%{__rm} -rf %{buildroot}


%files -f %{name}.lang
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README* RELNOTES ToDo
%doc %{_mandir}/man5/cmtab.5*
%doc %{_mandir}/man8/cryptmount*.8*
%doc %{_mandir}/*/man5/cmtab.5*
%doc %{_mandir}/*/man8/cryptmount*.8*
%config(noreplace) %{_sysconfdir}/cryptmount/
%config %{_initrddir}/cryptmount
%config /etc/modules-load.d/cryptmount.conf
%config /usr/lib/systemd/system/cryptmount.service
%{_sbindir}/cryptmount-setup
%{_libdir}/cryptmount/

%attr(4751, root, root) %{_bindir}/cryptmount


%post
/sbin/chkconfig --add cryptmount

%preun
if [ "$1" = 0 ]; then
    /sbin/chkconfig --del cryptmount
fi


%changelog
* Mon Apr 28 2014 RW Penney <cryptmount@rwpenney.org.uk> - 5.0
    -- Migrated LUKS functionality to use libcryptsetup
* Mon Dec 23 2013 RW Penney <cryptmount@rwpenney.org.uk> - 4.5
    -- Added support for TRIM on SSDs
* Wed May 21 2013 RW Penney <cryptmount@rwpenney.org.uk> - 4.4
    -- Added support systemd
* Thu Dec 29 2011 RW Penney <cryptmount@rwpenney.org.uk> - 4.3
    -- Added support for environmental variables in configuration file
* Tue May 03 2011 RW Penney <cryptmount@rwpenney.org.uk> - 4.2
    -- Added entropy-based protection against accidental swap formatting
* Wed Mar 10 2010 RW Penney <cryptmount@rwpenney.org.uk> - 4.1
    -- Improved compatability with cryptsetup-1.1
* Mon Jan 05 2009 RW Penney <cryptmount@rwpenney.org.uk> - 4.0
    -- Improved password fortification via iterated hashing
* Sun Jan 22 2006 Holger Mueller <holger@MAPS.euhm.de> - 0.1-1mr
    -- RPM spec created
