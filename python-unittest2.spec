# Created by pyp2rpm-1.1.1
%global pypi_name unittest2
%global with_python3 1
%global bootstrap_traceback2 0

Name:           python-%{pypi_name}
Version:        1.1.0
Release:        15%{?dist}
Summary:        The new features in unittest backported to Python 2.4+

License:        BSD
URL:            http://pypi.python.org/pypi/unittest2
Source0:        https://pypi.python.org/packages/source/u/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# we don't need this in Fedora, since we have Python 2.7, which has argparse
Patch0:         unittest2-1.1.0-remove-argparse-from-requires.patch
# we only apply this if bootstrap_traceback2 == 1
Patch1:         unittest2-1.1.0-remove-traceback2-from-requires.patch
# this patch backports tests from Python 3.5, that weren't yet merged, thus the tests are failing
#  (the test is modified to also pass on Python < 3.5)
#  TODO: submit upstream
Patch2:         unittest2-1.1.0-backport-tests-from-py3.5.patch
BuildArch:      noarch


%description
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7 and onwards. It is tested to run on Python 2.6, 2.7,
3.2, 3.3, 3.4 and pypy.


%package -n     python2-%{pypi_name}
Summary:        The new features in unittest backported to Python 2.4+
%{?python_provide:%python_provide python2-%{pypi_name}}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-six
%if ! 0%{?bootstrap_traceback2}
BuildRequires:  python2-traceback2
Requires:       python2-traceback2
%endif
Requires:       python2-setuptools
Requires:       python2-six


%description -n python2-%{pypi_name}
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7 and onwards. It is tested to run on Python 2.6, 2.7,
3.2, 3.3, 3.4 and pypy.


%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        The new features in unittest backported to Python 2.4+
%{?python_provide:%python_provide python3-%{pypi_name}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
%if ! 0%{?bootstrap_traceback2}
BuildRequires:  python3-traceback2
%endif # bootstrap_traceback2
Requires:       python3-setuptools
Requires:       python3-six
%if ! 0%{?bootstrap_traceback2}
Requires:       python3-traceback2
%endif


%description -n python3-%{pypi_name}
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7 and onwards. It is tested to run on Python 2.6, 2.7,
3.2, 3.3, 3.4 and pypy.
%endif # with_python3


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%patch0 -p0
%patch2 -p0
%if 0%{?bootstrap_traceback2}
%patch1 -p0
%endif


%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
%py3_install
pushd %{buildroot}%{_bindir}
mv unit2 unit2-%{python3_version}
ln -s unit2-%{python3_version} unit2-3
# compatibility symlink
ln -s unit2-%{python3_version} python3-unit2
popd
%endif

%py2_install
pushd %{buildroot}%{_bindir}
mv unit2 unit2-%{python2_version}
ln -s unit2-%{python2_version} unit2-2
ln -s unit2-2 unit2
popd


%check
%if ! 0%{?bootstrap_traceback2}
%{__python2} -m unittest2

%if 0%{?with_python3}
%{__python3} -m unittest2
%endif # with_python3
%endif # bootstrap_traceback2


%files -n python2-%{pypi_name}
%doc README.txt
%{_bindir}/unit2
%{_bindir}/unit2-2
%{_bindir}/unit2-%{python2_version}
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info


%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.txt
%{_bindir}/unit2-3
%{_bindir}/unit2-%{python3_version}
%{_bindir}/python3-unit2
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with_python3


%changelog
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-14
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-13
- Bootstrap for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.1.0-11
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.1.0-8
- Disable bootstrap method

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.1.0-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu May 19 2016 Carl George <carl.george@rackspace.com> - 1.1.0-5
- Implement new Python packaging guidelines (python2 subpackage)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 15 2015 Slavek Kabrda <bkabrda@redhat.com> - 1.1.0-3
- Fix tests on Python 3.5

* Sat Nov 14 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 1.1.0-2
- traceback2 has been bootstrapped.  Remove the bootstrapping conditional

* Thu Nov 12 2015 bkabrda <bkabrda@redhat.com> - 1.1.0-1
- Update to 1.1.0
- Bootstrap dependency on traceback2

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 14 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.8.0-2
- Bump to avoid collision with previously blocked 0.8.0-1

* Mon Nov 10 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.8.0-1
- Unretire the package, create a fresh specfile
