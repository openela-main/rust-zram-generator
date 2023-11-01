%global crate zram-generator

Name:           rust-%{crate}
Version:        0.3.2
Release:        7%{?dist}
Summary:        Systemd unit generator for zram swap devices

License:        MIT
URL:            https://crates.io/crates/%{crate}
Source:         %{crates_source}
Source1:        %{crate}-v%{version}-vendor.tar.gz
Source2:        zram-generator.conf
Source3:        zram-generator.8
Source4:        zram-generator.conf.5

ExclusiveArch:  %{rust_arches}

BuildRequires:  git
BuildRequires:  rust-toolset
BuildRequires:  systemd-devel systemd-rpm-macros
BuildRequires:  /usr/bin/make

%global _description %{expand:
This is a systemd unit generator that enables swap on zram.
(With zram, there is no physical swap device. Part of the avaialable RAM
is used to store compressed pages, essentially trading CPU cycles for memory.)}

%description %{_description}

%package        -n %{crate}
Summary:        %{summary}
License:        MIT
%description    -n %{crate} %{_description}

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
cp -a %{S:2} .
%cargo_prep -V 1

%build
export SYSTEMD_UTIL_DIR=%{_systemd_util_dir}
%cargo_build
make systemd_service SYSTEMD_SYSTEM_UNIT_DIR=%{_unitdir} SYSTEMD_SYSTEM_GENERATOR_DIR=%{_systemdgeneratordir}
cp -a %{S:3} %{S:4} man/

%install
export SYSTEMD_UTIL_DIR=%{_systemd_util_dir}
%cargo_install

mkdir -p %{buildroot}%{_systemdgeneratordir}
mv -v %{buildroot}%{_bindir}/zram-generator %{buildroot}%{_systemdgeneratordir}/
install -Dpm0644 -t %{buildroot}%{_unitdir} units/systemd-zram-setup@.service
install -Dpm0644 -t %{buildroot}%{_prefix}/lib/systemd %{SOURCE2}
install -Dpm0644 -t %{buildroot}%{_mandir}/man8 man/zram-generator.8
install -Dpm0644 -t %{buildroot}%{_mandir}/man5 man/zram-generator.conf.5

%files -n %{crate}
%license LICENSE
%doc zram-generator.conf.example
%doc README.md
%{_systemdgeneratordir}/zram-generator
%{_unitdir}/systemd-zram-setup@.service
%{_prefix}/lib/systemd/zram-generator.conf
%{_mandir}/man8/zram-generator.8*
%{_mandir}/man5/zram-generator.conf.5*

%changelog
* Thu Aug 12 2021  <msekleta@redhat.com> - 0.3.2-7
- Rebuild (#1990555)

* Thu Aug 05 2021  <msekleta@redhat.com> - 0.3.2-6
- Rename binary rpm to zram-generator (#1990555)

* Thu Jun 24 2021  <msekleta@redhat.com> - 0.3.2-5
- Adjust packaging to account for differences between Fedora and CentOS/RHEL rust packaging (#1930369)

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com>
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Mar 23 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.3.2-3
- Fix missing path to generator dir

* Fri Mar 19 2021 Vasiliy Glazov <vascom2@gmail.com> - 0.3.2-2
- Fix max-zram-size value to 8GB

* Wed Feb 24 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.3.2-1
- Downgrade logging levels (#1930869)

* Wed Jan 27 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.3.1-2
- Implement https://fedoraproject.org/wiki/Changes/Scale_ZRAM_to_full_memory_size (#1921084)

* Sat Jan 23 13:23:10 CET 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1

* Wed Jan 13 16:57:21 CET 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.3.0~rc.1-1
- Update to 0.3.0-rc.1

* Mon Dec 28 13:34:14 CET 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.2.0-6
- Rebuild

* Mon Nov 23 2020 Fabio Valentini <decathorpe@gmail.com> - 0.2.0-5
- Allow building against rust-ini 0.16.

* Sun Aug 16 15:02:03 GMT 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.2.0-4
- Rebuild

* Sat Aug  1 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.2.0-3
- Obsolete zram package from zram-generator-defaults

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 04 17:30:46 CEST 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Tue Jun 23 19:56:14 CEST 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.2.0~rc.1-1
- Update to 0.2.0-rc.1

* Thu Jun 18 11:30:43 CEST 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.2.0~beta.1-3
- Create a subpackage with default configuration

* Thu Jun 18 10:14:43 CEST 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.2.0~beta.1-2
- Install swap-create unit file

* Thu Jun 18 09:27:37 CEST 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.2.0~beta.1-1
- Update to 0.2.0-beta.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct  7 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.1.2-1
- Update to latest version

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 21:30:22 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.1-4
- Regenerate

* Sat Mar 09 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.1-3
- Adapt to new packaging

* Fri Mar  1 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.1.1-2
- Add crude patch to fix build (#1676154)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 16 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.1.1-1
- Initial package
