# https://github.com/cri-o/cri-o
%global goipath         github.com/kubernetes-sigs/cri-tools
Version:                1.22.0

%if 0%{?rhel} && 0%{?rhel} <= 8
%define gobuild(o:) %{expand:
  # https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
  %global _dwz_low_mem_die_limit 0
  %ifnarch ppc64
  go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-}%{?currentgoldflags} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags %{?__golang_extldflags}' -compressdwarf=false" -a -v -x %{?**};
  %else
  go build                -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-}%{?currentgoldflags} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags %{?__golang_extldflags}' -compressdwarf=false" -a -v -x %{?**};
  %endif
}
%bcond_with check
%else
%gometa
%bcond_without check
%endif

%global built_tag v%{version}

Name: %{repo}
Release: 3%{?dist}
Summary: CLI and validation tools for Container Runtime Interface
License: ASL 2.0
URL:     https://%{goipath}
Source0: %url/archive/v%{version}/%{name}-%{version}.tar.gz
# no ppc64
ExclusiveArch: %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm} ppc64le s390x}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires: golang
BuildRequires: glibc-static
BuildRequires: git
BuildRequires: go-md2man
Provides: crictl = %{version}-%{release}

%description
%{summary}

%prep
%if 0%{?rhel} && 0%{?rhel} <= 8
%autosetup -p1 -n %{name}-%{version}
%else
%goprep -k
%endif

%build
%gobuild -o bin/crictl %{goipath}/cmd/crictl
go-md2man -in docs/crictl.md -out docs/crictl.1

%install
# install binaries
install -dp %{buildroot}%{_bindir}
install -p -m 755 ./bin/crictl %{buildroot}%{_bindir}

# install manpage
install -dp %{buildroot}%{_mandir}/man1
install -p -m 644 docs/crictl.1 %{buildroot}%{_mandir}/man1

%files
%license LICENSE
%doc CHANGELOG.md CONTRIBUTING.md OWNERS README.md RELEASE.md code-of-conduct.md
%doc docs/{benchmark.md,roadmap.md,validation.md}
%{_bindir}/crictl
%{_mandir}/man1/crictl*

%changelog
* Thu Nov 11 2021 Peter Hunt <pehunt@redhat.com> - 1.21.0-3
- bump to v1.21.0

* Wed Aug 18 2021 Peter Hunt <pehunt@redhat.com> - 1.20.0-2
- bump to v1.20.0

* Tue Nov 10 14:03:43 EST 2020 Peter Hunt <pehunt@redhat.com> - 1.19.0-1
- bump to v1.19.0

* Thu Jul 09 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.18.0-1
- bump to v1.18.0

* Tue Jan 14 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.17.0-1
- new version

* Tue Nov 05 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.16.1-2
- GO111MODULE=off

* Tue Oct 22 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.16.1-1
- bump to v1.16.1

* Sat Jul 20 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.15.0-1
- bump to v1.15.0

* Sat Jul 20 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.14.0-1
- bump to v1.14.0

* Thu Feb 21 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.13.0-1.gitc06001f
- bump to v1.13.0

* Thu Jan 31 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.12.0-2.gite392824
- built commit e392824

* Wed Oct 31 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.12.0-1.gite4dff19
- bump to v1.12.0

* Mon Sep 17 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.11.1-2.gitedabfb5
- buit commit edabfb5

* Mon Aug 27 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.11.1-1.git404b126
- bump to v1.11.1

* Mon Jul 02 2018 Lokesh Mandvekar <lsm5@redhat.com> - 1.0.0-6.rhaos3.11.git78ec590
- import spec from rhaos3.10
- built release-1.11 commit 78ec590

* Wed May 16 2018 Lokesh Mandvekar <lsm5@redhat.com> - 1.0.0-5.rhaos3.10.git2e22a75
- Resolves: #1572795 - build for all arches
- From: Yaakov Selkowitz <yselkowi@redhat.com>

* Tue May 15 2018 Lokesh Mandvekar <lsm5@redhat.com> - 1.0.0-4.rhaos3.10.git2e22a75
- built commit 2e22a75
- include rhaos version in release tag

* Sun Apr 22 2018 Lokesh Mandvekar <lsm5@redhat.com> - 1.0.0-3.gitf37a5a1
- built commit f37a5a1
- critest doesn't build, skipped for now

* Wed Feb 07 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-2.alpha.0.git653cc8c
- include critest binary

* Wed Feb 07 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-1.alpha.0.gitf1a58d6
- First package for Fedora
