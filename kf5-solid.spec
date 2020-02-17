%define		kdeframever	5.67
%define		qtver		5.9.0
%define		kfname		solid

Summary:	Desktop hardware abstraction
Name:		kf5-%{kfname}
Version:	5.67.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	0598657737a55b535d4bb0dbb9bba889
URL:		http://www.kde.org/
BuildRequires:	Qt5Concurrent-devel >= %{qtver}
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Qml-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5Xml-devel >= %{qtver}
BuildRequires:	bison
BuildRequires:	cmake >= 2.8.12
BuildRequires:	flex
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	ninja
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	xz
Requires:	kf5-dirs
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
Requires:	cmake >= 2.6.0

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%ninja_build

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
%attr(755,root,root) %ghost %{_libdir}/libKF5Solid.so.5
%attr(755,root,root) %{_libdir}/libKF5Solid.so.*.*
%dir %{_libdir}/qt5/qml/org/kde/solid
%{_libdir}/qt5/qml/org/kde/solid/qmldir
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/solid/libsolidextensionplugin.so
%{_datadir}/qlogging-categories5/solid.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/Solid
%{_includedir}/KF5/solid_version.h
%{_libdir}/cmake/KF5Solid
%attr (755,root,root) %{_libdir}/libKF5Solid.so
%{qt5dir}/mkspecs/modules/qt_Solid.pri
