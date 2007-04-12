%define modname perl
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A48_%{modname}.ini

Summary:	This extension embeds Perl Interpreter into PHP
Name:		php-%{modname}
Version:	1.0.0
Release:	%mkrel 8
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/perl
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tar.bz2
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	perl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
This extension embeds Perl Interpreter into PHP. It allows execute Perl files,
evaluate Perl code, access Perl variables and instantiate Perl objects.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%build

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc tests CREDITS EXPERIMENTAL README TODO package*.xml 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

