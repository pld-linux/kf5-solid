#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.115
%define		qtver		5.15.2
%define		kfname		solid

Summary:	Desktop hardware abstraction
Name:		kf5-%{kfname}
Version:	5.115.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	4bc3f8554b526f0e39d8c2a6f228a988
URL:		http://www.kde.org/
BuildRequires:	Qt5Concurrent-devel >= %{qtver}
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Qml-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Xml-devel >= %{qtver}
BuildRequires:	bison >= 3.0
BuildRequires:	cmake >= 3.16
BuildRequires:	flex
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	libimobiledevice-devel
BuildRequires:	libmount-devel
BuildRequires:	libplist-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	xz
Requires:	Qt5Core >= %{qtver}
Requires:	Qt5DBus >= %{qtver}
Requires:	Qt5Gui >= %{qtver}
Requires:	Qt5Qml >= %{qtver}
Requires:	Qt5Xml >= %{qtver}
Requires:	kf5-dirs
Suggests:	media-player-info
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
Solid is a device integration framework. It provides a way of querying
and interacting with hardware independently of the underlying
operating system.

It provides the following features for application developers:

- Hardware Discovery
- Power Management
- Network Management


%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qtver}
Requires:	cmake >= 3.16

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md TODO
%attr(755,root,root) %{_bindir}/solid-hardware5
%ghost %{_libdir}/libKF5Solid.so.5
%attr(755,root,root) %{_libdir}/libKF5Solid.so.*.*
%dir %{_libdir}/qt5/qml/org/kde/solid
%{_libdir}/qt5/qml/org/kde/solid/qmldir
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/solid/libsolidextensionplugin.so
%{_datadir}/qlogging-categories5/solid.categories
%{_datadir}/qlogging-categories5/solid.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/Solid
%{_libdir}/cmake/KF5Solid
%{_libdir}/libKF5Solid.so
%{qt5dir}/mkspecs/modules/qt_Solid.pri
