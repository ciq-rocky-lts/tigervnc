
#defining macros needed by SELinux
%global selinuxtype targeted
%global modulename vncsession

Name:           tigervnc
Version:        1.12.0
Release:        15%{?dist}.5
Summary:        A TigerVNC remote display system

%global _hardened_build 1

License:        GPLv2+
URL:            http://www.tigervnc.com

Source0:        %{name}-%{version}.tar.gz
Source1:        xvnc.service
Source2:        xvnc.socket
Source3:        10-libvnc.conf

# Backwards compatibility
Source5:        vncserver

Patch1:         tigervnc-use-gnome-as-default-session.patch

# Upstream patches
Patch50:        tigervnc-selinux-restore-context-in-case-of-different-policies.patch
Patch51:        tigervnc-fix-typo-in-mirror-monitor-detection.patch
Patch52:        tigervnc-root-user-selinux-context.patch
Patch53:        tigervnc-vncsession-restore-script-systemd-service.patch
# https://github.com/TigerVNC/tigervnc/pull/1513
Patch54:        tigervnc-fix-ghost-cursor-in-zaphod-mode.patch
# https://github.com/TigerVNC/tigervnc/pull/1510
Patch55:        tigervnc-add-new-keycodes-for-unknown-keysyms.patch
Patch56:        tigervnc-sanity-check-when-cleaning-up-keymap-changes.patch
Patch57:        tigervnc-selinux-allow-vncsession-create-vnc-directory.patch

# This is tigervnc-%%{version}/unix/xserver116.patch rebased on the latest xorg
Patch100:       tigervnc-xserver120.patch
# 1326867 - [RHEL7.3] GLX applications in an Xvnc session fails to start
Patch101:       0001-rpath-hack.patch

# Xorg CVEs
Patch201:       xorg-CVE-2023-5380.patch
Patch202:       xorg-CVE-2023-6377.patch
Patch203:       xorg-CVE-2023-6478.patch
Patch204:       xorg-CVE-2023-6816.patch
Patch205:       xorg-CVE-2024-0229-1.patch
Patch206:       xorg-CVE-2024-0229-2.patch
Patch207:       xorg-CVE-2024-0229-3.patch
Patch208:       xorg-CVE-2024-21885.patch
Patch209:       xorg-CVE-2024-21886-1.patch
Patch210:       xorg-CVE-2024-21886-2.patch

# CVE-2023-1393 tigervnc: xorg-x11-server: X.Org Server Overlay Window Use-After-Free Local Privilege Escalation Vulnerability
Patch110:       xorg-x11-server-composite-Fix-use-after-free-of-the-COW.patch

BuildRequires:  gcc-c++
BuildRequires:  libX11-devel, automake, autoconf, libtool, gettext, gettext-autopoint
BuildRequires:  libXext-devel, xorg-x11-server-source, libXi-devel
BuildRequires:  xorg-x11-xtrans-devel, xorg-x11-util-macros, libXtst-devel
BuildRequires:  libxkbfile-devel, openssl-devel, libpciaccess-devel
BuildRequires:  mesa-libGL-devel, libXinerama-devel, xorg-x11-font-utils
BuildRequires:  freetype-devel, libXdmcp-devel, libxshmfence-devel
BuildRequires:  libjpeg-turbo-devel, gnutls-devel, pam-devel
BuildRequires:  libdrm-devel, libXt-devel, pixman-devel
BuildRequires:  systemd, cmake, desktop-file-utils
BuildRequires:  libselinux-devel, selinux-policy-devel
BuildRequires:  libXfixes-devel, libXdamage-devel, libXrandr-devel
%if 0%{?fedora} > 24 || 0%{?rhel} >= 7
BuildRequires:  libXfont2-devel
%else
BuildRequires:  libXfont-devel
%endif

# TigerVNC 1.4.x requires fltk 1.3.3 for keyboard handling support
# See https://github.com/TigerVNC/tigervnc/issues/8, also bug #1208814
BuildRequires:  fltk-devel >= 1.3.3
BuildRequires:  xorg-x11-server-devel

Requires(post): coreutils
Requires(postun):coreutils

Requires:       hicolor-icon-theme
Requires:       tigervnc-license
Requires:       tigervnc-icons

%description
Virtual Network Computing (VNC) is a remote display system which
allows you to view a computing 'desktop' environment not only on the
machine where it is running, but from anywhere on the Internet and
from a wide variety of machine architectures.  This package contains a
client which will allow you to connect to other desktops running a VNC
server.

%package server
Summary:        A TigerVNC server
Requires:       perl-interpreter
Requires:       tigervnc-server-minimal = %{version}-%{release}
Requires:       (%{name}-selinux if selinux-policy-%{selinuxtype})
Requires:       xorg-x11-xauth
Requires:       xorg-x11-xinit
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires(post): systemd

%description server
The VNC system allows you to access the same desktop from a wide
variety of platforms.  This package includes set of utilities
which make usage of TigerVNC server more user friendly. It also
contains x0vncserver program which can export your active
X session.

%package server-minimal
Summary:        A minimal installation of TigerVNC server
Requires(post): chkconfig
Requires(preun):chkconfig

Requires:       mesa-dri-drivers, xkeyboard-config, xorg-x11-xkb-utils
Requires:       tigervnc-license, dbus-x11

%description server-minimal
The VNC system allows you to access the same desktop from a wide
variety of platforms. This package contains minimal installation
of TigerVNC server, allowing others to access the desktop on your
machine.

%package server-module
Summary:        TigerVNC module to Xorg
Requires:       xorg-x11-server-Xorg %(xserver-sdk-abi-requires ansic) %(xserver-sdk-abi-requires videodrv)
Requires:       tigervnc-license

%description server-module
This package contains libvnc.so module to X server, allowing others
to access the desktop on your machine.

%package license
Summary:        License of TigerVNC suite
BuildArch:      noarch

%description license
This package contains license of the TigerVNC suite

%package icons
Summary:        Icons for TigerVNC viewer
BuildArch:      noarch

%description icons
This package contains icons for TigerVNC viewer

%package selinux
Summary:        SELinux module for TigerVNC
BuildArch:      noarch
BuildRequires:  selinux-policy-devel
Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}
BuildRequires:  selinux-policy-devel
# Required for matchpathcon
Requires:       libselinux-utils
# Required for restorecon
Requires:       policycoreutils
%{?selinux_requires}

%description selinux
This package provides the SELinux policy module to ensure TigerVNC
runs properly under an environment with SELinux enabled.

%prep
%setup -q

cp -r /usr/share/xorg-x11-server-source/* unix/xserver
pushd unix/xserver
for all in `find . -type f -perm -001`; do
        chmod -x "$all"
done
%patch100 -p1 -b .xserver120-rebased
%patch101 -p1 -b .rpath
%patch110 -p1 -b .composite-Fix-use-after-free-of-the-COW
popd

%patch1 -p1 -b .use-gnome-as-default-session

# Upstream patches
%patch50 -p1 -b .selinux-restore-context-in-case-of-different-policies
%patch51 -p1 -b .fix-typo-in-mirror-monitor-detection
%patch52 -p1 -b .root-user-selinux-context
%patch53 -p1 -b .vncsession-restore-script-systemd-service
%patch54 -p1 -b .fix-ghost-cursor-in-zaphod-mode
%patch55 -p1 -b .add-new-keycodes-for-unknown-keysyms
%patch56 -p1 -b .sanity-check-when-cleaning-up-keymap-changes
%patch57 -p1 -b .selinux-allow-vncsession-create-vnc-directory

%build
%ifarch sparcv9 sparc64 s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpic"
%endif
export CXXFLAGS="$CFLAGS"

%{cmake} .
make %{?_smp_mflags}

pushd unix/xserver
autoreconf -fiv
%configure \
        --disable-xorg --disable-xnest --disable-xvfb --disable-dmx \
        --disable-xwin --disable-xephyr --disable-kdrive --disable-xwayland \
        --with-pic --disable-static \
        --with-default-font-path="catalogue:%{_sysconfdir}/X11/fontpath.d,built-ins" \
        --with-fontdir=%{_datadir}/X11/fonts \
        --with-xkb-output=%{_localstatedir}/lib/xkb \
        --enable-install-libxf86config \
        --enable-glx --disable-dri --enable-dri2 --disable-dri3 \
        --disable-unit-tests \
        --disable-config-hal \
        --disable-config-udev \
        --with-dri-driver-path=%{_libdir}/dri \
        --without-dtrace \
        --disable-devel-docs \
        --disable-selective-werror

make %{?_smp_mflags}
popd

# Build icons
pushd media
make
popd

# SELinux
pushd unix/vncserver/selinux
make
popd


%install
%make_install

pushd unix/xserver/hw/vnc
make install DESTDIR=%{buildroot}
popd

pushd unix/vncserver/selinux
make install DESTDIR=%{buildroot}
popd


# Install systemd unit file
install -m644 %{SOURCE1} %{buildroot}%{_unitdir}/xvnc@.service
install -m644 %{SOURCE2} %{buildroot}%{_unitdir}/xvnc.socket

# Install desktop stuff
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,24x24,48x48}/apps

pushd media/icons
for s in 16 24 48; do
install -m644 tigervnc_$s.png %{buildroot}%{_datadir}/icons/hicolor/${s}x$s/apps/tigervnc.png
done
popd

install -m 755 %{SOURCE5} %{buildroot}/%{_bindir}/vncserver

%find_lang %{name} %{name}.lang

# remove unwanted files
rm -f  %{buildroot}%{_libdir}/xorg/modules/extensions/libvnc.la

mkdir -p %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/10-libvnc.conf

%post server
%systemd_post xvnc.service
%systemd_post xvnc.socket

%preun server
%systemd_preun xvnc.service
%systemd_preun xvnc.socket

%postun server
%systemd_postun xvnc.service
%systemd_postun xvnc.socket

%pre selinux
%selinux_relabel_pre -s %{selinuxtype}

%post selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2
%selinux_relabel_post -s %{selinuxtype}

%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
    %selinux_relabel_post -s %{selinuxtype}
fi


%files -f %{name}.lang
%doc README.rst
%{_bindir}/vncviewer
%{_datadir}/applications/*
%{_mandir}/man1/vncviewer.1*

%files server
%config(noreplace) %{_sysconfdir}/pam.d/tigervnc
%config(noreplace) %{_sysconfdir}/tigervnc/vncserver-config-defaults
%config(noreplace) %{_sysconfdir}/tigervnc/vncserver-config-mandatory
%config(noreplace) %{_sysconfdir}/tigervnc/vncserver.users
%{_unitdir}/vncserver@.service
%{_unitdir}/xvnc@.service
%{_unitdir}/xvnc.socket
%{_bindir}/x0vncserver
%{_bindir}/vncserver
%{_sbindir}/vncsession
%{_libexecdir}/vncserver
%{_libexecdir}/vncsession-start
%{_libexecdir}/vncsession-restore
%{_mandir}/man1/x0vncserver.1*
%{_mandir}/man8/vncserver.8*
%{_mandir}/man8/vncsession.8*
%{_docdir}/tigervnc/HOWTO.md

%files server-minimal
%{_bindir}/vncconfig
%{_bindir}/vncpasswd
%{_bindir}/Xvnc
%{_mandir}/man1/Xvnc.1*
%{_mandir}/man1/vncpasswd.1*
%{_mandir}/man1/vncconfig.1*

%files server-module
%{_libdir}/xorg/modules/extensions/libvnc.so
%config %{_sysconfdir}/X11/xorg.conf.d/10-libvnc.conf

%files license
%{_docdir}/tigervnc/LICENCE.TXT

%files icons
%{_datadir}/icons/hicolor/*/apps/*

%files selinux
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.*
%ghost %verify(not md5 size mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}

%changelog
* Tue Jan 30 2024 mhink <mhink@ciq.com> 1.12.0-15.5
- CVE-2023-6816 CVE-2024-0229 CVE-2024-21885 CVE-2024-21886
* Wed Jan 03 2024 mhink <mhink@ciq.com> - 1.12.0-15.4
- CVE Rollups from upstream: Patches by Jan Grulich <jgrulich@redhat.com>
- Fix CVE-2023-5380 tigervnc: xorg-x11-server: Use-after-free bug in DestroyWindow
- Fix CVE-2023-5367 tigervnc: xorg-x11-server: Out-of-bounds write in XIChangeDeviceProperty/RRChangeOutputProperty
  Resolves: RHEL-15229
- Fix CVE-2023-6377 tigervnc: xorg-x11-server: out-of-bounds memory reads/writes in XKB button actions
  Resolves: RHEL-18409
- Fix CVE-2023-6478 tigervnc: xorg-x11-server: out-of-bounds memory read in RRChangeOutputProperty and RRChangeProviderProperty
  Resolves: RHEL-18421
- Updated fix for CVE-2023-6377 tigervnc: xorg-x11-server: out-of-bounds memory reads/writes in XKB button actions
  Resolves: RHEL-18409

*Mon Mar 27 2023 Jan Grulich <jgrulich@redhat.com> - 1.12.0-15
- xorg-x11-server: X.Org Server Overlay Window Use-After-Free Local Privilege Escalation Vulnerability
  Resolves: bz#2180305

* Tue Feb 21 2023 Jan Grulich <jgrulich@redhat.com> - 1.12.0-14
- SELinux: allow vncsession create .vnc directory
  Resolves: bz#2164704

* Wed Feb 15 2023 Jan Grulich <jgrulich@redhat.com> - 1.12.0-13
- Add sanity check when cleaning up keymap changes
  Resolves: bz#2169960

* Mon Feb 06 2023 Jan Grulich <jgrulich@redhat.com> - 1.12.0-12
- xorg-x11-server: DeepCopyPointerClasses use-after-free leads to privilege elevation
  Resolves: bz#2167058

* Tue Dec 20 2022 Tomas Popela <tpopela@redhat.com> - 1.12.0-11
- Rebuild for xorg-x11-server CVE-2022-46340 follow up fix

* Fri Dec 16 2022 Jan Grulich <jgrulich@redhat.com> - 1.12.0-10
- Rebuild for xorg-x11-server CVEs
  Resolves: CVE-2022-4283 (bz#2154233)
  Resolves: CVE-2022-46340 (bz#2154220)
  Resolves: CVE-2022-46341 (bz#2154223)
  Resolves: CVE-2022-46342 (bz#2154225)
  Resolves: CVE-2022-46343 (bz#2154227)
  Resolves: CVE-2022-46344 (bz#2154229)

* Thu Dec 08 2022 Jan Grulich <jgrulich@redhat.com> - 1.12.0-9
- Bump build version to fix upgrade path
  Resolves: bz#1437569

* Fri Nov 18 2022 Jan Grulich <jgrulich@redhat.com> - 1.12.0-8
- x0vncserver: add new keysym in case we don't find matching keycode
  Resolves: bz#1437569

* Wed Aug 24 2022 Jan Grulich <jgrulich@redhat.com> - 1.12.0-7
- x0vncserver: fix ghost cursor in zaphod mode (better version)
  Resolves: bz#2109679

* Wed Aug 17 2022 Jan Grulich <jgrulich@redhat.com> - 1.12.0-6
- x0vncserver: fix ghost cursor in zaphod mode
  Resolves: bz#2109679

* Tue May 31 2022 Jan Grulich <jgrulich@redhat.com> - 1.12.0-5
- BR: libXdamage, libXfixes, libXrandr
  Resolves: bz#2088733

* Tue Feb 08 2022 Jan Grulich <jgrulich@redhat.com> - 1.12.0-4
- Added vncsession-restore script for SELinux policy migration
  Fix SELinux context for root user
  Resolves: bz#2021892

* Fri Jan 21 2022 Jan Grulich <jgrulich@redhat.com> - 1.12.0-3
- Fix crash in vncviewer
  Resolves: bz#2021892

* Fri Jan 14 2022 Jan Grulich <jgrulich@redhat.com> - 1.12.0-2
- Remove unavailable option from vncserver script
  Resolves: bz#2021892

* Fri Jan 14 2022 Jan Grulich <jgrulich@redhat.com> - 1.12.0-1
- 1.12.0
  Resolves: bz#2021892

* Mon Jul 19 2021 Jan Grulich <jgrulich@redhat.com> - 1.11.0-9
- Fix logout from VNC session using vncserver
  Resolves: bz#1983706

* Tue Jun 01 2021 Jan Grulich <jgrulich@redhat.com> - 1.11.0-8
- Run all SELinux RPM macros on correct package
  Resolves: bz#1907963

* Mon May 17 2021 Jan Grulich <jgrulich@redhat.com> - 1.11.0-7
- SELinux improvements
  Resolves: bz#1907963

* Tue Dec 15 2020 Jan Grulich <jgrulich@redhat.com> - 1.11.0-6
- Use GNOME as default session
  Resolves: bz#1853608

* Thu Dec 03 2020 Jan Grulich <jgrulich@redhat.com> - 1.11.0-5
- Make sure we log properly output to journal (actually log to syslog)
  Resolves: bz#1841537

* Thu Dec 03 2020 Jan Grulich <jgrulich@redhat.com> - 1.11.0-4
- Make sure we log properly output to journal
  Resolves: bz#1841537

* Wed Nov 18 2020 Jan Grulich <jgrulich@redhat.com> - 1.11.0-3
- vncserver: ignore new "session" parameter from the new systemd support
  Resolves: bz#1897504

* Wed Nov 18 2020 Jan Grulich <jgrulich@redhat.com> - 1.11.0-2
- Revert removal of vncserver
  Resolves: bz#1897504
- Correctly start vncsession as a daemon
  Resolves: bz#1897498

* Tue Oct 20 2020 Jan Grulich <jgrulich@redhat.com> - 1.11.0-1
- Update to 1.11.0
  Resolves: bz#1880985
- Backport fix to allow Tigervnc use boolean values in config files
  Resolves: bz#1883415

* Wed Sep 30 2020 Jan Grulich <jgrulich@redhat.com> - 1.10.1-8
- Tolerate specifying -BoolParam 0 and similar
  Resolves: bz#1883415

* Wed Jul 08 2020 Jan Grulich <jgrulich@redhat.com> - 1.10.1-7
- Enable server module on s390x
  Resolves: bz#1854925

* Fri Jul 03 2020 Jan Grulich <jgrulich@redhat.com> - 1.10.1-6
- Remove trailing spaces in user name
  Resolves: bz#1852432

* Thu Jun 25 2020 Jan Grulich <jgrulich@redhat.com> - 1.10.1-5
- Install the HOWTO file to correct location
- Add /usr/bin/vncserver file informing users to read the HOWTO.md file
  Resolves: bz#1790443

* Mon Jun 15 2020 Jan Grulich <jgrulich@redhat.com> - 1.10.1-4
- Improve SELinux policy
  Resolves: bz#1790443

* Mon Jun 15 2020 Jan Grulich <jgrulich@redhat.com> - 1.10.1-3
- Add a HOWTO.md file with instructions how to start VNC server
  Resolves: bz#1790443

* Tue May 26 2020 Jan Grulich <jgrulich@redhat.com> - 1.10.1-2
- Make the systemd service run also for root user
  Resolves: bz#1790443

* Mon Apr 27 2020 Jan Grulich <jgrulich@redhat.com> - 1.10.1-1
- Update to 1.10.1
  Resolves: bz#1806992

- Add proper systemd support
  Resolves: bz#1790443

* Tue Jan 28 2020 Jan Grulich <jgrulich@redhat.com> - 1.9.0-13
- Bump build because of z-stream
  Resolves: bz#1671714

* Wed Dec 11 2019 Jan Grulich <jgrulich@redhat.com> - 1.9.0-12
- Fix installation of systemd files
  Resolves: bz#1671714

* Wed Nov 20 2019 Jan Grulich <jgrulich@redhat.com> - 1.9.0-11
- Use wrapper script to workaround systemd issues
  Resolves: bz#1671714

* Fri Jul 12 2019 Jan Grulich <jgrulich@redhat.com> - 1.9.0-10
- Do not return returncode indicating error when running "vncserver -list"
  Resolves: bz#1727860

* Fri Feb 08 2019 Jan Grulich <jgrulich@redhat.com> - 1.9.0-9
- Make tigervnc systemd service a user service
  Resolves: bz#1639846

* Mon Jan 21 2019 Jan Grulich <jgrulich@redhat.com> - 1.9.0-8
- Kill the session automatically only when Gnome is installed
  Resolves: bz#1665876

* Tue Nov 20 2018 Jan Grulich <jgrulich@redhat.com> - 1.9.0-7
- Improve coverity scan fixes
  Resolves: bz#1602714

  Inform whether view-only password is used or not
  Resolves: bz#1639169

  Backport fixes from RHEL 7
  Resolves: bz#1651254

* Tue Oct 09 2018 Jan Grulich <jgrulich@redhat.com> - 1.9.0-6
- Do not crash passwd when using malloc perturb checks
  Resolves: bz#1637086

* Mon Oct 08 2018 Jan Grulich <jgrulich@redhat.com> - 1.9.0-5
- Improve coverity scan fixes
  Resolves: bz#1602714

* Wed Oct 03 2018 Jan Grulich <jgrulich@redhat.com> - 1.9.0-4
- Improve coverity scan fixes
  Resolves: bz#1602714

* Wed Oct 03 2018 Jan Grulich <jgrulich@redhat.com> - 1.9.0-3
- Fix some coverity scan issues
  Resolves: bz#1602714

* Wed Aug 01 2018 Jan Grulich <jgrulich@redhat.com> - 1.9.0-2
- Remove dependency on initscripts

* Tue Jul 17 2018 Jan Grulich <jgrulich@redhat.com> - 1.9.0-1
- Update to 1.9.0 + sync with Fedora

* Tue Jun 12 2018 Adam Jackson <ajax@redhat.com> - 1.8.0-10
- Fix GLX initialization with Xorg 1.20

* Tue May 29 2018 Jan Grulich <jgrulich@redhat.com> - 1.8.0-9
- Build against Xorg 1.20

* Mon May 14 2018 Jan Grulich <jgrulich@redhat.com> - 1.8.0-8
- Drop BR: ImageMagick

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.0-6
- Remove obsolete scriptlets

* Fri Dec 15 2017 Jan Grulich <jgrulich@redhat.com> - 1.8.0-5
- Properly initialize tigervnc when started as systemd service

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 1.8.0-2
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Wed May 17 2017 Jan Grulich <jgrulich@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Thu Apr 20 2017 Jan Grulich <jgrulich@redhat.com> - 1.7.90-1
- Update to 1.7.90 (beta)

* Thu Apr 06 2017 Jan Grulich <jgrulich@redhat.com> - 1.7.1-4
- Added systemd unit file for xvnc
  Resolves: bz#891802

* Tue Apr 04 2017 Jan Grulich <jgrulich@redhat.com> - 1.7.1-3
- Bug 1438704 - CVE-2017-7392 CVE-2017-7393 CVE-2017-7394
                CVE-2017-7395 CVE-2017-7396 tigervnc: various flaws
  + other upstream related fixes

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Jan Grulich <jgrulich@redhat.com> - 1.7.1-1
- Update to 1.7.1

* Mon Jan  9 2017 Hans de Goede <hdegoede@redhat.com> - 1.7.0-6
- Fix -inetd no longer working (rhbz#1408724)

* Wed Nov 30 2016 Jan Grulich <jgrulich@redhat.com> - 1.7.0-5
- Fix broken vncserver.service file

* Wed Nov 23 2016 Jan Grulich <jgrulich@redhat.com> - 1.7.0-4
- Improve instructions in vncserver.service
  Resolves: bz#1397207

* Tue Oct  4 2016 Hans de Goede <hdegoede@redhat.com> - 1.7.0-3
- Update tigervnc-1.7.0-xserver119-support.patch to also request write
  notfication when necessary

* Mon Oct  3 2016 Hans de Goede <hdegoede@redhat.com> - 1.7.0-2
- Add patches for use with xserver-1.19
- Rebuild against xserver-1.19
- Cleanup specfile a bit

* Mon Sep 12 2016 Jan Grulich <jgrulich@redhat.com> - 1.7.0-1
- Update to 1.7.0

* Mon Jul 18 2016 Jan Grulich <jgrulich@redhat.com> - 1.6.90-1
- Update to 1.6.90 (1.7.0 beta)

* Wed Jun 01 2016 Jan Grulich <jgrulich@redhat.com> - 1.6.0-6
- Try to pickup upstream fix for compatibility with gtk vnc clients

* Wed Jun 01 2016 Jan Grulich <jgrulich@redhat.com> - 1.6.0-5
- Re-enable patch4 again, will need to find a way to make this work on both sides

* Mon May 23 2016 Jan Grulich <jgrulich@redhat.com> - 1.6.0-4
- Utilize system-wide crypto policies
  Resolves: bz#1179345
- Try to disable patch4 as it was previously written to support an
  older version of a different client and breaks some other usage
  Resolves: bz#1280440

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Jan Grulich <jgrulich@redhat.com> - 1.6.0-2
- Update systemd service file
  Resolves: bz#1211789

* Mon Jan 04 2016 Jan Grulich <jgrulich@redhat.com> - 1.6.0-1
- Update to 1.6.0

* Tue Dec 01 2015 Jan Grulich <jgrulich@redhat.com> - 1.5.90-1
- Update to 1.5.90 (1.6.0 beta)

* Thu Nov 19 2015 Jan Grulich <jgrulich@redhat.com> - 1.5.0-4
- rebuild against final xorg server 1.18 release (bug #1279146)

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 1.5.0-3
- xorg server 1.18 ABI rebuild

* Fri Aug 21 2015 Jan Grulich <jgrulich@redhat.com> - 1.5.0-2
- Do not fail with -inetd option

* Wed Aug 19 2015 Jan Grulich <jgrulich@redhat.com> - 1.5.0-1
- 1.5.0

* Tue Aug 04 2015 Kevin Fenzi <kevin@scrye.com> - 1.4.3-12
- Rebuild to fix broken deps and build against xorg 1.18 prerelease

* Thu Jun 25 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-11
- Rebuilt (bug #1235603).

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Kalev Lember <kalevlember@gmail.com> - 1.4.3-8
- Rebuilt for nettle soname bump

* Wed Apr 22 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-7
- Removed incorrect parameters from vncviewer manpage (bug #1213199).

* Tue Apr 21 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-6
- Use full git hash for GitHub tarball release.

* Fri Apr 10 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-5
- Explicit version build dependency for fltk (bug #1208814).

* Thu Apr  9 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-4
- Drop upstream xorg-x11-server patch as it is now built (bug #1210407).

* Thu Apr  9 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-3
- Apply upstream patch to fix byte order (bug #1206060).

* Fri Mar  6 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-2
- Don't disable Xinerama extension (upstream #147).

* Mon Mar  2 2015 Tim Waugh <twaugh@redhat.com> - 1.4.3-1
- 1.4.3.

* Tue Feb 24 2015 Tim Waugh <twaugh@redhat.com> - 1.4.2-3
- Use calloc instead of xmalloc.
- Removed unnecessary configure flags.

* Wed Feb 18 2015 Rex Dieter <rdieter@fedoraproject.org> 1.4.2-2
- rebuild (fltk)

* Fri Feb 13 2015 Tim Waugh <twaugh@redhat.com> - 1.4.2-1
- Rebased xserver116.patch against xorg-x11-server-1.17.1.
- Allow build against xorg-x11-server-1.17.
- 1.4.2.

* Tue Sep  9 2014 Tim Waugh <twaugh@redhat.com> - 1.3.1-11
- Added missing part of xserver114.patch (bug #1137023).

* Wed Sep  3 2014 Tim Waugh <twaugh@redhat.com> - 1.3.1-10
- Fix build against xorg-x11-server-1.16.0 (bug #1136532).

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 15 2014 Tim Waugh <twaugh@redhat.com> - 1.3.1-8
- Input reset fixes from upstream (bug #1116956).
- No longer need ppc64le patch as it's now in xorg-x11-server.
- Rebased xserver114.patch again.

* Fri Jun 20 2014 Hans de Goede <hdegoede@redhat.com> - 1.3.1-7
- xserver 1.15.99.903 ABI rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Tim Waugh <twaugh@redhat.com> 1.3.1-5
- Keep pointer in sync when using module (upstream bug #152).

* Mon Apr 28 2014 Adam Jackson <ajax@redhat.com> 1.3.1-4
- Add version interlocks for -server-module

* Mon Apr 28 2014 Hans de Goede <hdegoede@redhat.com> - 1.3.1-3
- xserver 1.15.99-20140428 git snapshot ABI rebuild

* Mon Apr  7 2014 Tim Waugh <twaugh@redhat.com> 1.3.1-2
- Allow build with dri3 and present extensions (bug #1063392).

* Thu Mar 27 2014 Tim Waugh <twaugh@redhat.com> 1.3.1-1
- 1.3.1 (bug #1078806).
- Add ppc64le support (bug #1078495).

* Wed Mar 19 2014 Tim Waugh <twaugh@redhat.com> 1.3.0-15
- Disable dri3 to enable building (bug #1063392).
- Fixed heap-based buffer overflow (CVE-2014-0011, bug #1050928).

* Fri Feb 21 2014 Tim Waugh <twaugh@redhat.com> 1.3.0-14
- Enabled hardened build (bug #955206).

* Mon Feb 10 2014 Tim Waugh <twaugh@redhat.com> 1.3.0-13
- Clearer xstartup file (bug #923655).

* Tue Jan 14 2014 Tim Waugh <twaugh@redhat.com> 1.3.0-12
- Fixed instructions in systemd unit file.

* Fri Jan 10 2014 Tim Waugh <twaugh@redhat.com> 1.3.0-11
- Fixed viewer crash when cursor has not been set (bug #1038701).

* Thu Dec 12 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-10
- Avoid invalid read when ZRLE connection closed (upstream bug #133).

* Tue Dec  3 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-9
- Fixed build failure with -Werror=format-security (bug #1037358).

* Thu Nov 07 2013 Adam Jackson <ajax@redhat.com> 1.3.0-8
- Rebuild against xserver 1.15RC1

* Tue Sep 24 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-7
- Removed incorrect patch (for unexpected key_is_down). Fixes stuck
  keys bug (bug #989502).

* Thu Sep 19 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-6
- Fixed typo in 10-libvnc.conf (bug #1009111).

* Wed Sep 18 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-5
- Better fix for PIDFile problem (bug #983232).

* Mon Aug  5 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-4
- Fixed doc-related build failure (bug #992790).

* Wed Jul 24 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-3
- Avoid PIDFile problems in systemd unit file (bug #983232).
- libvnc.so: don't use unexported key_is_down function.
- Don't use shebang in vncserver script.

* Fri Jul 12 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-2
- Renumbered patches.
- libvnc.so: don't use unexported GetMaster function (bug #744881 again).

* Mon Jul  8 2013 Tim Waugh <twaugh@redhat.com> 1.3.0-1
- 1.3.0.

* Wed Jul  3 2013 Tim Waugh <twaugh@redhat.com> 1.2.80-0.18.20130314svn5065
- Removed systemd_requires macro in order to fix the build.

* Wed Jul  3 2013 Tim Waugh <twaugh@redhat.com> 1.2.80-0.17.20130314svn5065
- Synchronise manpages and --help output (bug #980870).

* Mon Jun 17 2013 Adam Jackson <ajax@redhat.com> 1.2.80-0.16.20130314svn5065
- tigervnc-setcursor-crash.patch: Attempt to paper over a crash in Xvnc when
  setting the cursor.

* Sat Jun 08 2013 Dennis Gilmore <dennis@ausil.us> 1.2.80-0.15.20130314svn5065
- bump to rebuild and pick up bugfix causing X to crash on ppc and arm

* Thu May 23 2013 Tim Waugh <twaugh@redhat.com> 1.2.80-0.14.20130314svn5065
- Use systemd rpm macros (bug #850340).  Moved systemd requirements
  from main package to server sub-package.
- Applied Debian patch to fix busy loop when run from inetd in nowait
  mode (bug #920373).
- Added dependency on xorg-x11-xinit to server sub-package so that
  default window manager can be found (bug #896284, bug #923655).
- Fixed bogus changelog date.

* Thu Mar 14 2013 Adam Jackson <ajax@redhat.com> 1.2.80-0.13.20130314svn5065
- Less RHEL customization

* Thu Mar 14 2013 Adam Tkac <atkac redhat com> - 1.2.80-0.12.20130314svn5065
- include /etc/X11/xorg.conf.d/10-libvnc.conf sample configuration (#712482)
- vncserver now honors specified -geometry parameter (#755947)

* Tue Mar 12 2013 Adam Tkac <atkac redhat com> - 1.2.80-0.11.20130307svn5060
- update to r5060
- split icons to separate package to avoid multilib issues

* Tue Feb 19 2013 Adam Tkac <atkac redhat com> - 1.2.80-0.10.20130219svn5047
- update to r5047 (X.Org 1.14 support)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.80-0.9.20121126svn5015
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 1.2.80-0.8.20121126svn5015
- rebuild due to "jpeg8-ABI" feature drop

* Wed Jan 16 2013 Adam Tkac <atkac redhat com> 1.2.80-0.7.20121126svn5015
- rebuild

* Tue Dec 04 2012 Adam Tkac <atkac redhat com> 1.2.80-0.6.20121126svn5015
- rebuild against new fltk

* Mon Nov 26 2012 Adam Tkac <atkac redhat com> 1.2.80-0.5.20121126svn5015
- update to r5015
- build with -fpic instead of -fPIC on all archs except s390/sparc

* Wed Nov  7 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.80-0.4.20120905svn4996
- Build with -fPIC to fix FTBFS on ARM

* Wed Oct 31 2012 Adam Jackson <ajax@redhat.com> 1.2.80-0.3.20120905svn4996
- tigervnc12-xorg113-glx.patch: Fix to only init glx on the first server
  generation

* Fri Sep 28 2012 Adam Jackson <ajax@redhat.com> 1.2.80-0.2.20120905svn4996
- tigervnc12-xorg113-glx.patch: Re-enable GLX against xserver 1.13

* Fri Aug 17 2012 Adam Tkac <atkac redhat com> 1.2.80-0.1.20120905svn4996
- update to 1.2.80
- remove deprecated patches
  - tigervnc-102434.patch
  - tigervnc-viewer-reparent.patch
  - tigervnc11-java7.patch
- patches merged
  - tigervnc11-xorg111.patch
  - tigervnc11-xorg112.patch

* Fri Aug 10 2012 Dave Airlie <airlied@redhat.com> 1.1.0-10
- fix build against newer X server

* Mon Jul 23 2012 Adam Jackson <ajax@redhat.com> 1.1.0-9
- Build with the Composite extension for feature parity with other X servers

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 19 2012 Dave Airlie <airlied@redhat.com> 1.1.0-7
- fix building against X.org 1.13

* Wed Apr 04 2012 Adam Jackson <ajax@redhat.com> 1.1.0-6
- RHEL exclusion for -server-module on ppc* too

* Mon Mar 26 2012 Adam Tkac <atkac redhat com> - 1.1.0-5
- clean Xvnc's /tmp environment in service file before startup
- fix building against the latest JAVA 7 and X.Org 1.12

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Adam Tkac <atkac redhat com> - 1.1.0-3
- don't build X.Org devel docs (#755782)
- applet: BR generic java-devel instead of java-gcj-devel (#755783)
- use runuser to start Xvnc in systemd service file (#754259)
- don't attepmt to restart Xvnc session during update/erase (#753216)

* Fri Nov 11 2011 Adam Tkac <atkac redhat com> - 1.1.0-2
- libvnc.so: don't use unexported GetMaster function (#744881)
- remove nasm buildreq

* Mon Sep 12 2011 Adam Tkac <atkac redhat com> - 1.1.0-1
- update to 1.1.0
- update the xorg11 patch
- patches merged
  - tigervnc11-glx.patch
  - tigervnc11-CVE-2011-1775.patch
  - 0001-Use-memmove-instead-of-memcpy-in-fbblt.c-when-memory.patch

* Thu Jul 28 2011 Adam Tkac <atkac redhat com> - 1.0.90-6
- add systemd service file and remove legacy SysV initscript (#717227)

* Thu May 12 2011 Adam Tkac <atkac redhat com> - 1.0.90-5
- make Xvnc buildable against X.Org 1.11

* Tue May 10 2011 Adam Tkac <atkac redhat com> - 1.0.90-4
- viewer can send password without proper validation of X.509 certs
  (CVE-2011-1775)

* Wed Apr 13 2011 Adam Tkac <atkac redhat com> - 1.0.90-3
- fix wrong usage of memcpy which caused screen artifacts (#652590)
- don't point to inaccessible link in sysconfig/vncservers (#644975)

* Fri Apr 08 2011 Adam Tkac <atkac redhat com> - 1.0.90-2
- improve compatibility with vinagre client (#692048)

* Tue Mar 22 2011 Adam Tkac <atkac redhat com> - 1.0.90-1
- update to 1.0.90

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.90-0.32.20110117svn4237
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Adam Tkac <atkac redhat com> 1.0.90-0.31.20110117svn4237
- fix libvnc.so module loading

* Mon Jan 17 2011 Adam Tkac <atkac redhat com> 1.0.90-0.30.20110117svn4237
- update to r4237
- patches merged
  - tigervnc11-optionsdialog.patch
  - tigervnc11-rh607866.patch

* Fri Jan 14 2011 Adam Tkac <atkac redhat com> 1.0.90-0.29.20101208svn4225
- improve patch for keyboard issues

* Fri Jan 14 2011 Adam Tkac <atkac redhat com> 1.0.90-0.28.20101208svn4225
- attempt to fix various keyboard-related issues (key repeating etc)

* Fri Jan 07 2011 Adam Tkac <atkac redhat com> 1.0.90-0.27.20101208svn4225
- render "Ok" and "Cancel" buttons in the options dialog correctly

* Wed Dec 15 2010 Jan Görig <jgorig redhat com> 1.0.90-0.26.20101208svn4225
- added vncserver lock file (#662784)

* Fri Dec 10 2010 Adam Tkac <atkac redhat com> 1.0.90-0.25.20101208svn4225
- update to r4225
- patches merged
  - tigervnc11-rh611677.patch
  - tigervnc11-rh633931.patch
  - tigervnc11-xorg1.10.patch
- enable VeNCrypt and PAM support

* Mon Dec 06 2010 Adam Tkac <atkac redhat com> 1.0.90-0.24.20100813svn4123
- rebuild against xserver 1.10.X
- 0001-Return-Success-from-generate_modkeymap-when-max_keys.patch merged

* Wed Sep 29 2010 jkeating - 1.0.90-0.23.20100813svn4123
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Adam Tkac <atkac redhat com> 1.0.90-0.22.20100420svn4030
- drop xorg-x11-fonts-misc dependency (#636170)

* Tue Sep 21 2010 Adam Tkac <atkac redhat com> 1.0.90-0.21.20100420svn4030
- improve patch for #633645 (fix tcsh incompatibilities)

* Thu Sep 16 2010 Adam Tkac <atkac redhat com> 1.0.90-0.20.20100813svn4123
- press fake modifiers correctly (#633931)
- supress unneeded debug information emitted from initscript (#633645)

* Wed Aug 25 2010 Adam Tkac <atkac redhat com> 1.0.90-0.19.20100813svn4123
- separate Xvnc, vncpasswd and vncconfig to -server-minimal subpkg (#626946)
- move license to separate subpkg and Requires it from main subpkgs
- Xvnc: handle situations when no modifiers exist well (#611677)

* Fri Aug 13 2010 Adam Tkac <atkac redhat com> 1.0.90-0.18.20100813svn4123
- update to r4123 (#617973)
- add perl requires to -server subpkg (#619791)

* Thu Jul 22 2010 Adam Tkac <atkac redhat com> 1.0.90-0.17.20100721svn4113
- update to r4113
- patches merged
  - tigervnc11-rh586406.patch
  - tigervnc11-libvnc.patch
  - tigervnc11-rh597172.patch
  - tigervnc11-rh600070.patch
  - tigervnc11-options.patch
- don't own %%{_datadir}/icons directory (#614301)
- minor improvements in the .desktop file (#616340)
- bundled libjpeg configure requires nasm; is executed even if system-wide
  libjpeg is used

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 1.0.90-0.16.20100420svn4030
- build against system-wide libjpeg-turbo (#494458)
- build no longer requires nasm

* Mon Jun 28 2010 Adam Tkac <atkac redhat com> 1.0.90-0.15.20100420svn4030
- vncserver: accept <+optname> option when specified as the first one

* Thu Jun 24 2010 Adam Tkac <atkac redhat com> 1.0.90-0.14.20100420svn4030
- fix memory leak in Xvnc input code (#597172)
- don't crash when receive negative encoding (#600070)
- explicitly disable udev configuration support
- add gettext-autopoint to BR

* Mon Jun 14 2010 Adam Tkac <atkac redhat com> 1.0.90-0.13.20100420svn4030
- update URL about SSH tunneling in the sysconfig file (#601996)

* Fri Jun 11 2010 Adam Tkac <atkac redhat com> 1.0.90-0.12.20100420svn4030
- use newer gettext
- autopoint now uses git instead of cvs, adjust BuildRequires appropriately

* Thu May 13 2010 Adam Tkac <atkac redhat com> 1.0.90-0.11.20100420svn4030
- link libvnc.so "now" to catch "undefined symbol" errors during Xorg startup
- use always XkbConvertCase instead of XConvertCase (#580159, #586406)
- don't link libvnc.so against libXi.la, libdix.la and libxkb.la; use symbols
  from Xorg instead

* Thu May 13 2010 Adam Tkac <atkac redhat com> 1.0.90-0.10.20100420svn4030
- update to r4030 snapshot
- patches merged to upstream
  - tigervnc11-rh522369.patch
  - tigervnc11-rh551262.patch
  - tigervnc11-r4002.patch
  - tigervnc11-r4014.patch

* Thu Apr 08 2010 Adam Tkac <atkac redhat com> 1.0.90-0.9.20100219svn3993
- add server-applet subpackage which contains Java vncviewer applet
- fix Java applet; it didn't work when run from web browser
- add xorg-x11-xkb-utils to server Requires

* Fri Mar 12 2010 Adam Tkac <atkac redhat com> 1.0.90-0.8.20100219svn3993
- add French translation to vncviewer.desktop (thanks to Alain Portal)

* Thu Mar 04 2010 Adam Tkac <atkac redhat com> 1.0.90-0.7.20100219svn3993
- don't crash during pixel format change (#522369, #551262)

* Mon Mar 01 2010 Adam Tkac <atkac redhat com> 1.0.90-0.6.20100219svn3993
- add mesa-dri-drivers and xkeyboard-config to -server Requires
- update to r3993 1.0.90 snapshot
  - tigervnc11-noexecstack.patch merged
  - tigervnc11-xorg18.patch merged
  - xserver18.patch is no longer needed

* Wed Jan 27 2010 Jan Gorig <jgorig redhat com> 1.0.90-0.5.20091221svn3929
- initscript LSB compliance fixes (#523974)

* Fri Jan 22 2010 Adam Tkac <atkac redhat com> 1.0.90-0.4.20091221svn3929
- mark stack as non-executable in jpeg ASM code
- add xorg-x11-xauth to Requires
- add support for X.Org 1.8
- drop shave sources, they are no longer needed

* Thu Jan 21 2010 Adam Tkac <atkac redhat com> 1.0.90-0.3.20091221svn3929
- drop tigervnc-xorg25909.patch, it has been merged to X.Org upstream

* Thu Jan 07 2010 Adam Tkac <atkac redhat com> 1.0.90-0.2.20091221svn3929
- add patch for upstream X.Org issue #25909
- add libXdmcp-devel to build requires to build Xvnc with XDMCP support (#552322)

* Mon Dec 21 2009 Adam Tkac <atkac redhat com> 1.0.90-0.1.20091221svn3929
- update to 1.0.90 snapshot
- patches merged
  - tigervnc10-compat.patch
  - tigervnc10-rh510185.patch
  - tigervnc10-rh524340.patch
  - tigervnc10-rh516274.patch

* Mon Oct 26 2009 Adam Tkac <atkac redhat com> 1.0.0-3
- create Xvnc keyboard mapping before first keypress (#516274)

* Thu Oct 08 2009 Adam Tkac <atkac redhat com> 1.0.0-2
- update underlying X source to 1.6.4-0.3.fc11
- remove bogus '-nohttpd' parameter from /etc/sysconfig/vncservers (#525629)
- initscript LSB compliance fixes (#523974)
- improve -LowColorSwitch documentation and handling (#510185)
- honor dotWhenNoCursor option (and it's changes) every time (#524340)

* Fri Aug 28 2009 Adam Tkac <atkac redhat com> 1.0.0-1
- update to 1.0.0
- tigervnc10-rh495457.patch merged to upstream

* Mon Aug 24 2009 Karsten Hopp <karsten@redhat.com> 0.0.91-0.17
- fix ifnarch s390x for server-module

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.0.91-0.16
- rebuilt with new openssl

* Tue Aug 04 2009 Adam Tkac <atkac redhat com> 0.0.91-0.15
- make Xvnc compilable

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.91-0.14.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Adam Tkac <atkac redhat com> 0.0.91-0.13.1
- don't write warning when initscript is called with condrestart param (#508367)

* Tue Jun 23 2009 Adam Tkac <atkac redhat com> 0.0.91-0.13
- temporary use F11 Xserver base to make Xvnc compilable
- BuildRequires: libXi-devel
- don't ship tigervnc-server-module on s390/s390x

* Mon Jun 22 2009 Adam Tkac <atkac redhat com> 0.0.91-0.12
- fix local rendering of cursor (#495457)

* Thu Jun 18 2009 Adam Tkac <atkac redhat com> 0.0.91-0.11
- update to 0.0.91 (1.0.0 RC1)
- patches merged
  - tigervnc10-rh499401.patch
  - tigervnc10-rh497592.patch
  - tigervnc10-rh501832.patch
- after discusion in upstream drop tigervnc-bounds.patch
- configure flags cleanup

* Thu May 21 2009 Adam Tkac <atkac redhat com> 0.0.90-0.10
- rebuild against 1.6.1.901 X server (#497835)
- disable i18n, vncviewer is not UTF-8 compatible (#501832)

* Mon May 18 2009 Adam Tkac <atkac redhat com> 0.0.90-0.9
- fix vncpasswd crash on long passwords (#499401)
- start session dbus daemon correctly (#497592)

* Mon May 11 2009 Adam Tkac <atkac redhat com> 0.0.90-0.8.1
- remove merged tigervnc-manminor.patch

* Tue May 05 2009 Adam Tkac <atkac redhat com> 0.0.90-0.8
- update to 0.0.90

* Thu Apr 30 2009 Adam Tkac <atkac redhat com> 0.0.90-0.7.20090427svn3789
- server package now requires xorg-x11-fonts-misc (#498184)

* Mon Apr 27 2009 Adam Tkac <atkac redhat com> 0.0.90-0.6.20090427svn3789
- update to r3789
  - tigervnc-rh494801.patch merged
- tigervnc-newfbsize.patch is no longer needed
- fix problems when vncviewer and Xvnc run on different endianess (#496653)
- UltraVNC and TightVNC clients work fine again (#496786)

* Wed Apr 08 2009 Adam Tkac <atkac redhat com> 0.0.90-0.5.20090403svn3751
- workaround broken fontpath handling in vncserver script (#494801)

* Fri Apr 03 2009 Adam Tkac <atkac redhat com> 0.0.90-0.4.20090403svn3751
- update to r3751
- patches merged
  - tigervnc-xclients.patch
  - tigervnc-clipboard.patch
  - tigervnc-rh212985.patch
- basic RandR support in Xvnc (resize of the desktop)
- use built-in libjpeg (SSE2/MMX accelerated encoding on x86 platform)
- use Tight encoding by default
- use TigerVNC icons

* Tue Mar 03 2009 Adam Tkac <atkac redhat com> 0.0.90-0.3.20090303svn3631
- update to r3631

* Tue Mar 03 2009 Adam Tkac <atkac redhat com> 0.0.90-0.2.20090302svn3621
- package review related fixes

* Mon Mar 02 2009 Adam Tkac <atkac redhat com> 0.0.90-0.1.20090302svn3621
- initial package, r3621
