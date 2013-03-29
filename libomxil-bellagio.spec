#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Bellagio OpenMAX Integration Layer implementation
Summary(pl.UTF-8):	Implementacja Bellagio standardu OpenMAX Integration Layer
Name:		libomxil-bellagio
Version:	0.9.3
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/omxil/%{name}-%{version}.tar.gz
# Source0-md5:	a1de827fdb75c02c84e55f740ca27cb8
Patch0:		%{name}-link.patch
URL:		http://omxil.sourceforge.net/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libtool
BuildRequires:	sed >= 4.0
Provides:	OpenMAX-IL = 1.1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# module references RM_{Deinit,Init} symbols from resource manager
%define		skip_post_check_so	.*%{_libdir}/omxloaders/libomxdynamicloader\.so.*

%description
This is an Open Source implementation of the OpenMAX Integration Layer
(IL) API version 1.1.2, specified by the Khronos group (see
<http://www.khronos.org/openmax/>).

%description -l pl.UTF-8
Ten pakiet jest mającą otwarte źródła implementacją standardu OpenMAX
Integration Layer (IL) w wersji 1.1.2, opisanego przez Khronos Group
(<http://www.khronos.org/openmax/>).

%package devel
Summary:	Header files for Bellagio OpenMAX IL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Bellagio OpenMAX IL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	OpenMAX-IL-devel = 1.1.2

%description devel
Header files for Bellagio OpenMAX IL library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Bellagio OpenMAX IL.

%package static
Summary:	Static Bellagio OpenMAX IL library
Summary(pl.UTF-8):	Statyczna biblioteka Bellagio OpenMAX IL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	OpenMAX-IL-static = 1.1.2

%description static
Static Bellagio OpenMAX IL library.

%description static -l pl.UTF-8
Statyczna biblioteka Bellagio OpenMAX IL.

%package apidocs
Summary:	Bellagio OpenMAX IL API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Bellagio OpenMAX IL
Group:		Documentation

%description apidocs
API and internal documentation for Bellagio OpenMAX IL library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Bellagio OpenMAX IL.

%prep
%setup -q
%patch0 -p1

# unhandled case enum value warnings when using gcc 4.6
sed -i -e 's/-Werror//' configure.ac

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	docdir=/unwanted

%{__rm} -r $RPM_BUILD_ROOT/unwanted

# libomxil-bellagio.la kept - no Libs.private in .pc (-ldl -lpthread needed)

# dlopened modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{bellagio,omxloaders}/libomx*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/omxregister-bellagio
%attr(755,root,root) %{_libdir}/libomxil-bellagio.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libomxil-bellagio.so.0
%dir %{_libdir}/bellagio
%attr(755,root,root) %{_libdir}/bellagio/libomxaudio_effects.so*
%attr(755,root,root) %{_libdir}/bellagio/libomxclocksrc.so*
%attr(755,root,root) %{_libdir}/bellagio/libomxvideosched.so*
%dir %{_libdir}/omxloaders
%attr(755,root,root) %{_libdir}/omxloaders/libomxdynamicloader.so*
%{_mandir}/man1/omxregister-bellagio.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libomxil-bellagio.so
%{_libdir}/libomxil-bellagio.la
%{_includedir}/bellagio
%{_includedir}/OMX_Audio.h
%{_includedir}/OMX_Component.h
%{_includedir}/OMX_ContentPipe.h
%{_includedir}/OMX_Core.h
%{_includedir}/OMX_IVCommon.h
%{_includedir}/OMX_Image.h
%{_includedir}/OMX_Index.h
%{_includedir}/OMX_Other.h
%{_includedir}/OMX_Types.h
%{_includedir}/OMX_Video.h
%{_pkgconfigdir}/libomxil-bellagio.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libomxil-bellagio.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/libomxil-bellagio/html/*
%endif
