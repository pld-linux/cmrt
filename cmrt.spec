#
# Conditional build:
%bcond_with	static_libs	# static library

%define	libva_ver	1.2.0

Summary:	C for Media Runtime - Media GPU kernel manager for Intel G45 & HD Graphics family
Summary(pl.UTF-8):	C for Media Runtime - zarządca jądra multimedialnego GPU dla układów z rodzin Intel G45 i HD
Name:		cmrt
Version:	1.0.6
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/intel/cmrt/releases
Source0:	https://github.com/intel/cmrt/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	91f5845c9354cce44a5133337f4e881c
URL:		https://github.com/intel/cmrt
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	libdrm-devel >= 2.4.23
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libva-devel >= %{libva_ver}
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libva) >= 0.34
Requires:	libdrm >= 2.4.23
Requires:	libva >= %{libva_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C for Media Runtime - Media GPU kernel manager for Intel G45 & HD
Graphics family.

%description -l pl.UTF-8
C for Media Runtime - zarządca jądra multimedialnego GPU dla układów z
rodzin Intel G45 i HD.

%package jitter
Summary:	Online compiler to convert VirtualISA into Gen HW instructions
Summary(pl.UTF-8):	Kompilator w locie reprezentacji VirtualISA na instrukcje Gen HW
License:	distributable, non-free, closed source
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++ >= 6:4.8

%description jitter
Jitter (igfxcmjit32.so or igfxcmjit64.so) is an online compiler to
convert VirtualISA into Gen HW instruction, while VirtualISA is an
intermediate representation between CM source code and HW instruction.

%description jitter -l pl.UTF-8
Jitter (igfxcmjit32.so lub igfxcmjit64.so) to działający w locie
kompilator przekształcający reprezentację VirtualISA na instrukcje Gen
HW. VirtualISA to reprezentacja pośrednia między kodem źródłowym CM a
instrukcjami sprzętowymi.

%package devel
Summary:	Header files for CMRT library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CMRT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for CMRT library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki CMRT.

%package static
Summary:	Static CMRT library
Summary(pl.UTF-8):	Statyczna biblioteka CMRT
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static CMRT library.

%description static -l pl.UTF-8
Statyczna biblioteka CMRT.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%ifarch %{ix86}
install jitter/igfxcmjit32.so $RPM_BUILD_ROOT%{_libdir}
%endif
%ifarch %{x8664}
install jitter/igfxcmjit64.so $RPM_BUILD_ROOT%{_libdir}
%endif

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcmrt.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_libdir}/libcmrt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcmrt.so.1
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cmrt.conf

%ifarch %{ix86} %{x8664}
%files jitter
%defattr(644,root,root,755)
%doc jitter/{LICENSE,readme}.txt
%ifarch %{ix86}
%attr(755,root,root) %{_libdir}/igfxcmjit32.so
%endif
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/igfxcmjit64.so
%endif
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcmrt.so
%{_includedir}/cm_rt*.h
%{_pkgconfigdir}/libcmrt.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcmrt.a
%endif
