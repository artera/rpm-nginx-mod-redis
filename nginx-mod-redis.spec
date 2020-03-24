Summary: Redis caching module for mainline nginx
Name: nginx-mod-redis
Version: 0.3.9
Release: 2%{?dist}
Vendor: Artera
URL: https://www.nginx.com/resources/wiki/modules/redis/

%define _modname            redis
%define _nginxver           1.16.1
%define nginx_config_dir    %{_sysconfdir}/nginx
%define nginx_build_dir     %{_builddir}/nginx-%{_nginxver}
%define mod_build_dir       %{_builddir}/%{_modname}-%{version}

Source0: https://nginx.org/download/nginx-%{_nginxver}.tar.gz
Source1: https://people.freebsd.org/~osa/ngx_http_redis-%{version}.tar.gz

Requires: nginx = 1:%{_nginxver}
BuildRequires: nginx
BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: zlib-devel
BuildRequires: perl-devel
BuildRequires: gd-devel
BuildRequires: GeoIP-devel
BuildRequires: libxslt-devel
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: gperftools-devel

License: BSD

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Redis caching module for mainline nginx.

%prep
%setup -q -n nginx-%{_nginxver}
%setup -T -D -b 1 -n ngx_http_redis-%{version}

%build
cd %{_builddir}/nginx-%{_nginxver}
./configure %(nginx -V 2>&1 | grep 'configure arguments' | sed -r 's@^[^:]+: @@') --add-dynamic-module=../ngx_http_redis-%{version}
make modules

%install
%{__rm} -rf %{buildroot}

%{__install} -Dm755 %{nginx_build_dir}/objs/ngx_http_redis_module.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ngx_http_redis_module.so

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/nginx/modules/*.so
