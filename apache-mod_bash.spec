#Module-Specific definitions
%define mod_name mod_bash
%define mod_conf B45_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module which embeds bash
Name:		apache-%{mod_name}
Version:	0.1.1
Release: 	8
Group:		System/Servers
License:	Apache License
URL:		https://www.autistici.org/bakunin/mod_bash/
Source0:	http://www.autistici.org/bakunin/mod_bash/src/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Patch0:		mod_bash-build_fix.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	glib2-devel
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_bash on is an Apache module that embeds the bash interpreter within the
server.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0

cp %{SOURCE1} %{mod_conf}

%build
export PATH="/sbin:/usr/sbin:/bin:/usr/bin"
export CPPFLAGS="`apr-1-config --cppflags`"
autoreconf -fis

%configure2_5x

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 src/.libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc examples/*.bash README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-7mdv2012.0
+ Revision: 772596
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-6
+ Revision: 678282
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-5mdv2011.0
+ Revision: 587940
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-4mdv2010.1
+ Revision: 516068
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-3mdv2010.0
+ Revision: 406552
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-2mdv2009.1
+ Revision: 325639
- rebuild

* Fri Aug 29 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-1mdv2009.0
+ Revision: 277328
- fix build (again...)
- fix build
- import apache-mod_bash


* Fri Aug 29 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-1mdv2009.0
- initial Mandriva package
