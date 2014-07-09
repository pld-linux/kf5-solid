# TODO:
# - dir /usr/include/KF5 not packaged
# /usr/lib/qt5/qml/org/kde not packaged
%define         _state          stable
%define		orgname		solid

Summary:	Desktop hardware abstraction
Name:		kf5-%{orgname}
Version:	5.0.0
Release:	0.1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	ftp://ftp.kde.org/pub/kde/%{_state}/frameworks/%{version}/%{orgname}-%{version}.tar.xz
# Source0-md5:	c79868c1de10553a51126c75d5a122a6
URL:		http://www.kde.org/
BuildRequires:	Qt5Concurrent-devel
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5DBus-devel
BuildRequires:	Qt5Gui-devel >= 5.3.1
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	Qt5Xml-devel >= 5.2.0
BuildRequires:	bison
BuildRequires:	cmake >= 2.8.12
BuildRequires:	flex
BuildRequires:	kf5-extra-cmake-modules >= 1.0.0
BuildRequires:	qt5-linguist
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	udev-devel
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
Summary:	Header files for %{orgname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{orgname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{orgname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{orgname}.

%prep
%setup -q -n %{orgname}-%{version}

%build
install -d build
cd build
%cmake \
	-DBIN_INSTALL_DIR=%{_bindir} \
	-DKCFG_INSTALL_DIR=%{_datadir}/config.kcfg \
	-DPLUGIN_INSTALL_DIR=%{qt5dir}/plugins \
	-DQT_PLUGIN_INSTALL_DIR=%{qt5dir}/plugins \
	-DQML_INSTALL_DIR=%{qt5dir}/qml \
	-DIMPORTS_INSTALL_DIR=%{qt5dirs}/imports \
	-DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
	-DLIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DKF5_LIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DKF5_INCLUDE_INSTALL_DIR=%{_includedir} \
	-DECM_MKSPECS_INSTALL_DIR=%{qt5dir}/mkspecs/modules \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/ install \
        DESTDIR=$RPM_BUILD_ROOT

%find_lang %{orgname}5_qt --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{orgname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md TODO
%attr(755,root,root) %{_bindir}/solid-hardware5
%attr(755,root,root) %ghost %{_libdir}/libKF5Solid.so.5
%attr(755,root,root) %{_libdir}/libKF5Solid.so.5.0.0
%dir %{qt5dir}/qml/org/kde/solid
%attr(755,root,root) %{qt5dir}/qml/org/kde/solid/libsolidextensionplugin.so
%{qt5dir}/qml/org/kde/solid/qmldir

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/Solid
%{_includedir}/KF5/solid_version.h
%{_libdir}/cmake/KF5Solid
%attr (755,root,root) %{_libdir}/libKF5Solid.so
%{qt5dir}/mkspecs/modules/qt_Solid.pri
