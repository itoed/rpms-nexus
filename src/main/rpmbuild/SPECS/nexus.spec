Name:           %{_name}
Version:        %{_version}
Release:        %{_release}
Summary:        Sonatype Nexus Repository Manager
License:        None
Requires:       shadow-utils
AutoReqProv:    no
Source0:        %{name}-%{version}-bundle.tar.gz
Source1:        nexus

%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress

%define         localdir /usr/local

%description
Nexus is an open source repository manager for Maven and other repository
formats like P2, NuGet, static sites, RPM and more.

%prep
%setup -q -c

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{localdir}
install -dm 755 %{buildroot}%{localdir}/sonatype-work
install -dm 755 %{buildroot}/var/run/nexus
install -dm 755 %{buildroot}/etc/init.d

# The nexus directory
cp -r %{name}-%{version}-%{release} %{buildroot}%{localdir}

# Versionless link to the current version directory
ln -s %{name}-%{version}-%{release} %{buildroot}%{localdir}/nexus

# Overwrite the initd script
# (The version in the 2.7.2 bundle has a problem with exit
# code of the status function.
# See https://issues.sonatype.org/browse/NEXUS-6682
# for details)
cp %{SOURCE1} %{buildroot}%{localdir}/nexus/bin/

# Link to initd script
ln -s %{localdir}/nexus/bin/nexus %{buildroot}/etc/init.d

%pre
getent group nexus > /dev/null || groupadd -r nexus
getent passwd nexus > /dev/null || \
    useradd -r -g nexus -d %{_usr}/local/nexus -s /bin/sh -c "Sonatype Nexus" nexus

%files
%defattr(-,nexus,nexus,-)
%{localdir}/nexus
%{localdir}/%{name}-%{version}-%{release}
%{localdir}/sonatype-work
%attr(-,root,root) /etc/init.d/nexus

%changelog
* Sun Jul 27 2014 Eduardo Ito <ed@fghijk.local> - 2.7.2-03
- Copy initd script with status function exit code fix from Sonatype's GitHub master branch

* Mon Apr 28 2014 Eduardo Ito <itoed@fqdnok.com> - 2.7.1-01
- Use an empty sonatype-work directory

* Sat Feb 1 2014 Eduardo Ito <itoed@fqdnok.com> - 2.7.1-01
- Update nexus version

* Thu Dec 19 2013 Eduardo Ito <itoed@fqdnok.com> - 2.6.4-02
- Initial version of the package
