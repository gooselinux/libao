Name:           libao
Version:        0.8.8
Release:        7.1%{?dist}
Summary:        Cross Platform Audio Output Library
Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://xiph.org/ao/
Source0:        http://downloads.xiph.org/releases/ao/%{name}-%{version}.tar.gz
Source1:        ao.req
Patch0:         libao-0.8.8-bigendianfix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  esound-devel >= 0.2.8
BuildRequires:  arts-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  pulseaudio-lib-devel
%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE1}

%description
Libao is a cross platform audio output library. It currently supports
ESD, OSS, Solaris, and IRIX.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
# needed because of disabled internal dependency generator.  sheesh
Requires:       %{_libdir}/libao.so.2

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1

sed -i "s/-O20/$RPM_OPT_FLAGS/" configure
sed -i "s/-ffast-math//" configure
# 216108
sed -i "s/= -version-info/= -export-symbols-regex '^ao_.*' -version-info/" src/Makefile.in


%build
%configure
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" install

# remove unpackaged files from the buildroot
find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;


%clean 
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES COPYING README
%{_libdir}/libao.so.*
%{_libdir}/ao
%{_mandir}/man5/*

%files devel
%defattr(-,root,root,-)
%doc doc/*.html doc/*.c doc/*.css
%{_includedir}/ao
%{_libdir}/libao.so
%{_libdir}/pkgconfig/ao.pc
%{_datadir}/aclocal/ao.m4


%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.8.8-7.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jul  6 2008 Hans de Goede <j.w.r.degoede@hhs.nl> - 0.8.8-5
- Fix pulseaudio sound output on bigendian archs (bz 454165), patch by
  Ian Chapman

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.8.8-4
- Autorebuild for GCC 4.3

* Thu Nov 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 0.8.8-3
- Minor packaging cleanups for merge review (bz 225986)

* Wed Nov 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 0.8.8-2
- Fix multilib conflict (bz 341891)
- Fix Source0 and URL urls

* Wed Nov  7 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.8.8-1
- Updated to 0.8.8 (bz 316731)
- Cleaned up the SPEC
- Added PulseAudio support
- Made build parallel
- Killed rpaths
- Changed the kludges to use sed

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 0.8.6-5
- Rebuild for build ID

* Fri Jan 12 2007 Behdad Esfahbod <besfahbo@redhat.com> - 0.8.6-5
- Require libao.so.2 explicitly in -devel package
- Resolves: #221980

* Tue Nov 21 2006 Behdad Esfahbod <besfahbo@redhat.com> - 0.8.6-4
- Only export namespaced symbols. (bug 216108)

* Mon Jul 24 2006 Ray Strode <rstrode@redhat.com> - 0.8.6-3
- remove all .la files (bug 199058)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.8.6-2.1
- rebuild

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 0.8.6-2
- rebuild for -devel deps

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.8.6-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.8.6-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 09 2005 John (J5) Palmieri <johnp@redhat.com> 0.8.6-1
- update to 0.8.6

* Wed Mar 03 2005 John (J5) Palmieri <johnp@redhat.com> 0.8.5-3
- rebuild with gcc 4.0

* Thu Sep 02 2004 Colin Walters <walters@redhat.com>
- Update to 0.8.5
- Delete upstreamed patch libao-0.8.4-alsa10.patch

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Dec 11 2003 Bill Nottingham <notting@redhat.com> 0.8.4-1
- update to 0.8.4
- fix alsa09 plugin to work with alsa-1.0.0pre

* Wed Oct 22 2003 Bill Nottingham <notting@redhat.com> 0.8.3-5
- fix dependency blacklisting (#100917)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 0.8.3-2
- remove unpackaged files from the buildroot

* Fri Jul 18 2002 Bill Nottingham <notting@redhat.com> 0.8.3-1
- update to 0.8.3

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Mar 14 2002 Bill Nottingham <notting@redhat.com>
- hm, where did that esd output plugin go?

* Tue Jan  1 2002 Bill Nottingham <notting@redhat.com>
- update to 0.8.2

* Tue Aug 14 2001 Bill Nottingham <notting@redhat.com>
- update to 0.8.0

* Fri Jul 20 2001 Bill Nottingham <notting@redhat.com>
- split this off from the vorbis package, as something else now requires it

* Tue Jul 10 2001 Bill Nottingham <notting@redhat.com>
- own %%{_libdir}/ao
- I love libtool

* Tue Jun 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add links from library major version numbers in rpms

* Tue Jun 19 2001 Bill Nottingham <notting@redhat.com>
- update to rc1

* Fri May  4 2001 Oliver Paukstadt <oliver.paukstadt@millenux.com>
- fixed perl line in spec file to set optims correctly

* Tue Mar 20 2001 Bill Nottingham <notting@redhat.com>
- fix alpha/ia64, again
- use optflags, not -O20 -ffast-math (especially on alpha...)

* Mon Feb 26 2001 Bill Nottingham <notting@redhat.com>
- fix license tag

* Mon Feb 26 2001 Bill Nottingham <notting@redhat.com>
- beta4

* Fri Feb  9 2001 Bill Nottingham <notting@redhat.com>
- fix alpha/ia64

* Thu Feb  8 2001 Bill Nottingham <notting@redhat.com>
- update CVS in prep for beta4

* Wed Feb 07 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed bugzilla bug #25391. ogg123 now usses the OSS driver by default if
  none was specified.

* Tue Jan  9 2001 Bill Nottingham <notting@redhat.com>
- update CVS, grab aRts backend for libao

* Thu Dec 27 2000 Bill Nottingham <notting@redhat.com>
- update CVS

* Fri Dec 01 2000 Bill Nottingham <notting@redhat.com>
- rebuild because of broken fileutils

* Mon Nov 13 2000 Bill Nottingham <notting@redhat.com>
- hack up specfile some, merge some packages

* Sat Oct 21 2000 Jack Moffitt <jack@icecast.org>
- initial spec file created
