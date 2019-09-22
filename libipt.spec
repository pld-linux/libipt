#
# Conditional build:
%bcond_without	xed	# ptxed utility
%bcond_without	tests	# unit tests

Summary:	Intel Processor Trace Decoder Library
Summary(pl.UTF-8):	Biblioteka dekodera Intel PT (śladów procesora Intel)
Name:		libipt
Version:	2.0.1
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/intel/libipt/releases
Source0:	https://github.com/intel/libipt/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	bae11676b72d341ecb9b33b9add84be8
URL:		https://github.com/intel/libipt
BuildRequires:	cmake >= 2.8.6
%{?with_xed:BuildRequires:	intel-xed-devel}
# C++ is required only for -DPTUNIT test "ptunit-cpp".
%{?with_tests:BuildRequires:	libstdc++-devel}
# pandoc for -DMAN
BuildRequires:	pandoc
ExclusiveArch:	%{ix86} %{x8664} x32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Intel Processor Trace (Intel PT) Decoder Library is Intel's
reference implementation for decoding Intel PT. It can be used as a
standalone library or it can be partially or fully integrated into
your tool.

%description -l pl.UTF-8
Biblioteka Intel PT (Intel Processor Trace - śladów procesora Intel)
to wzorcowa implementacja Intela do dekodowania Intel PT. Może służyć
jako biblioteka samodzielna lub zintegrowana we własne narzędzia.

%package devel
Summary:	Header files for Intel Processor Trace Decoder Library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki dekodera Intel PT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files needed to develop programs that
use the Intel Processor Trace (Intel PT) Decoder Library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów
wykorzystujących bibliotekę dekodera Intel PT (śladów procesora
Intel).

%package tools
Summary:	Intel Processor Trace tools
Summary(pl.UTF-8):	Narzędzia Intel PT
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description tools
Intel Processor Trace tools.

%description tools -l pl.UTF-8
Narzędzia Intel PT.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	-DDEVBUILD:BOOL=ON \
	-DFEATURE_ELF:BOOL=ON \
	-DMAN:BOOL=ON \
	-DPEVENT:BOOL=ON \
	-DPTDUMP:BOOL=ON \
	%{?with_tests:-DPTUNIT:BOOL=ON} \
	%{?with_xed:-DPTXED:BOOL=ON -DXED_INCLUDE=%{_includedir}/xed}
# -DSIDEBAND:BOOL=ON not yet: not installed, binaries depend on it

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
install build/bin/ptdump $RPM_BUILD_ROOT%{_bindir}
%if %{with xed}
install build/bin/ptxed $RPM_BUILD_ROOT%{_bindir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) %{_libdir}/libipt.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libipt.so.2

%files devel
%defattr(644,root,root,755)
%doc doc/{getting_started,howto_capture,howto_libipt}.md
%attr(755,root,root) %{_libdir}/libipt.so
%{_includedir}/intel-pt.h
%{_mandir}/man3/pt_*.3*

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ptdump
%if %{with xed}
%attr(755,root,root) %{_bindir}/ptxed
%endif
