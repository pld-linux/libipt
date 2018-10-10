Summary:	Intel Processor Trace Decoder Library
Name:		libipt
Version:	2.0
Release:	1
License:	BSD
Group:		Libraries
URL:		https://github.com/01org/processor-trace
Source0:	https://github.com/01org/processor-trace/archive/v%{version}.tar.gz
# Source0-md5:	d7cc87d42479d41870056a99591096cd
# c++ is required only for -DPTUNIT test "ptunit-cpp".
# pandoc is for -DMAN.
BuildRequires:	cmake
BuildRequires:	libstdc++-devel
BuildRequires:	pandoc
ExclusiveArch:	%{ix86} %{x8664}

%description
The Intel Processor Trace (Intel PT) Decoder Library is Intel's
reference implementation for decoding Intel PT. It can be used as a
standalone library or it can be partially or fully integrated into
your tool.

%package devel
Summary:	Header files and libraries for Intel Processor Trace Decoder Library
Requires:	%{name} = %{version}-%{release}
ExclusiveArch:	%{ix86} %{x8664}

%description devel
The %{name}-devel package contains the header files and libraries
needed to develop programs that use the Intel Processor Trace (Intel
PT) Decoder Library.

%prep
%setup -q -n processor-trace-%{version}

%build
install -d build
cd build
%cmake \
	-DPTUNIT:BOOL=ON \
	-DMAN:BOOL=ON \
	-DDEVBUILD:BOOL=ON \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
  DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %ghost %{_libdir}/%{name}.so.2
%attr(755,root,root) %{_libdir}/%{name}.so.*.*

%files devel
%defattr(644,root,root,755)
%doc doc/{getting_started,howto_libipt}.md
%{_includedir}/intel-pt.h
%attr(755,root,root) %{_libdir}/%{name}.so
%{_mandir}/man3/pt_*.3*
