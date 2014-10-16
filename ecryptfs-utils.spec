Summary:	The eCryptfs mount helper and support libraries
Name:		ecryptfs-utils
Version:	104
Release:	2
License:	GPL v2+
Group:		Base
Source0:	http://launchpad.net/ecryptfs/trunk/%{version}/+download/%{name}_%{version}.orig.tar.gz
# Source0-md5:	6ae93822bcf0d15470516c30a3deee32
Patch0:		%{name}-sh.patch
Patch1:		%{name}-configure.patch
Patch2:		%{name}-link.patch
URL:		http://ecryptfs.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gpgme-devel
BuildRequires:	keyutils-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libtool
BuildRequires:	nss-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	perl-tools-pod
BuildRequires:	pkg-config
Requires:	%{name}-libs = %{version}-%{release}
Requires:	keyutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
eCryptfs is a stacked cryptographic filesystem that ships in Linux
kernel versions 2.6.19 and above. This package provides the mount
helper and supporting libraries to perform key management and mount
functions.

Install ecryptfs-utils if you would like to mount eCryptfs.

%package libs
Summary:	The eCryptfs library
Group:		Libraries

%description libs
eCryptfs library.

%package devel
Summary:	The eCryptfs userspace development package
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Userspace development files for eCryptfs.

%package -n pam-pam_ecryptfs
Summary:	A PAM module - ecryptfs
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description -n pam-pam_ecryptfs
A PAM module - ecryptfs.

%package -n python-ecryptfs
Summary:	eCryptfs python module
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description -n python-ecryptfs
eCryptfs python module.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static	\
	--enable-gpg		\
	--enable-openssl	\
	--enable-pam
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}
rm -f %{py_sitedir}/%{name}/*.la

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README THANKS doc/{ecryptfs-faq.html,ecryptfs-pkcs11-helper-doc.txt}

%attr(755,root,root) %{_bindir}/ecryptfs-add-passphrase
%attr(755,root,root) %{_bindir}/ecryptfs-find
%attr(755,root,root) %{_bindir}/ecryptfs-insert-wrapped-passphrase-into-keyring
%attr(755,root,root) %{_bindir}/ecryptfs-manager
%attr(755,root,root) %{_bindir}/ecryptfs-migrate-home
%attr(755,root,root) %{_bindir}/ecryptfs-mount-private
%attr(755,root,root) %{_bindir}/ecryptfs-recover-private
%attr(755,root,root) %{_bindir}/ecryptfs-rewrap-passphrase
%attr(755,root,root) %{_bindir}/ecryptfs-rewrite-file
%attr(755,root,root) %{_bindir}/ecryptfs-setup-private
%attr(755,root,root) %{_bindir}/ecryptfs-setup-swap
%attr(755,root,root) %{_bindir}/ecryptfs-stat
%attr(755,root,root) %{_bindir}/ecryptfs-umount-private
%attr(755,root,root) %{_bindir}/ecryptfs-unwrap-passphrase
%attr(755,root,root) %{_bindir}/ecryptfs-verify
%attr(755,root,root) %{_bindir}/ecryptfs-wrap-passphrase
%attr(755,root,root) %{_bindir}/ecryptfsd

%attr(755,root,root) /sbin/mount.ecryptfs
%attr(4755,root,root) /sbin/mount.ecryptfs_private
%attr(755,root,root) /sbin/umount.ecryptfs_private
%attr(755,root,root) /sbin/umount.ecryptfs

%{_datadir}/%{name}

%{_mandir}/man1/ecryptfs-*.1*
%{_mandir}/man1/mount.ecryptfs_private.1*
%{_mandir}/man1/umount.ecryptfs_private.1*
%{_mandir}/man7/ecryptfs.7*
%{_mandir}/man8/ecryptfs-*.8*
%{_mandir}/man8/ecryptfsd.8*
%{_mandir}/man8/mount.ecryptfs.8*
%{_mandir}/man8/umount.ecryptfs.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libecryptfs.so.?
%attr(755,root,root) %{_libdir}/libecryptfs.so.*.*.*
%dir %{_libdir}/ecryptfs
%attr(755,root,root) %{_libdir}/ecryptfs/libecryptfs_key_mod_gpg.so
%attr(755,root,root) %{_libdir}/ecryptfs/libecryptfs_key_mod_openssl.so
%attr(755,root,root) %{_libdir}/ecryptfs/libecryptfs_key_mod_passphrase.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libecryptfs.so
%{_libdir}/libecryptfs.la
%{_includedir}/ecryptfs.h
%{_pkgconfigdir}/libecryptfs.pc

%files -n pam-pam_ecryptfs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_ecryptfs.so
%{_mandir}/man8/pam_ecryptfs.8*

%files -n python-ecryptfs
%defattr(644,root,root,755)
%dir %{py_sitedir}/%{name}
%attr(755,root,root) %{py_sitedir}/%{name}/_libecryptfs.so*
%dir %{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}/libecryptfs.py[co]

