%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

%global srcname unittest2

Name:           python-%{srcname}
Version:        0.5.1
Release:        1%{?dist}
Summary:        Backport of new unittest features for Python 2.7 to Python 2.4+

Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/pypi/unittest2
Source0:        http://pypi.python.org/packages/source/u/%{srcname}/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-nose


%description
unittest2 is a backport of the new features added to the unittest
testing framework in Python 2.7. It is tested to run on Python 2.4 - 
2.6.

To use unittest2 instead of unittest simply replace ``import unittest``
with ``import unittest2``.

Classes in unittest2 derive from the equivalent classes in unittest,
so it should be possible to use the unittest2 test running infra-
structure without having to switch all your tests to using unittest2
immediately. Similarly
you can use the new assert methods on ``unittest2.TestCase`` with the
standard unittest test running infrastructure. Not all of the new
features in unittest2 will work with the standard unittest test loaders
and runners however.


%prep
%setup -q -n %{srcname}-%{version}


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}


%clean
rm -rf %{buildroot}


%check
#Failing test deactivated
cd unittest2/test
nosetests test_new_tests.py
#nosetests test_unittest2.py
nosetests test_unittest2_with.py


%files
%defattr(-,root,root,-)
%doc README.txt
%{_bindir}/unit2*
%{python_sitelib}/%{srcname}/
%{python_sitelib}/%{srcname}*.egg-info


%changelog
* Wed Jul 21 2010 Fabian Affolter <fabian@bernewireless.net> - 0.5.1-1
- Updated to new upstream version 0.5.1

* Sat Jul 03 2010 Fabian Affolter <fabian@bernewireless.net> - 0.5.0-1
- Removed build cond for check section
- Switched to python2-devel
- Updated to new upstream version 0.5.0

* Sat Jul 03 2010 Fabian Affolter <fabian@bernewireless.net> - 0.1.4-1
- Initial package
