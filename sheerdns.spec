Summary:	SheerDNS - simple replacement master DNS
Summary(pl):	SheerDNS - prosty "zastêpca" DNS-a nadrzêdnego
Name:		sheerdns
Version:	1.0.1
Release:	1
License:	GPL v2
Vendor:		Paul Sheer <psheer@icon.co.za>
Group:		Networking/Daemons
Source0:	http://threading.2038bug.com/sheerdns/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-dir.patch
URL:		http://threading.2038bug.com/sheerdns/
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Provides:       nameserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SheerDNS was written to be a simple replacement master DNS server that
can be used where atomic updates are required. Because it stores each
record in a small file, updating records does not require the sheerdns
process to be notified or restarted.

%description -l pl
SheerDNS zosta³ napisany jako prosty zastêpca DNS-a nadrzêdnego, który
mo¿e byæ u¿ywany do automatycznych aktualizacji. Ka¿dy rekord
przechowywany jest w ma³ym pliku, dlatego te¿ aktualizacja rekordu nie
wymaga restartu procesu sheerdns.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%{__make} \
	CFLAGS="%{rpmcflags} -Wall -ansi -pedantic"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d \
	   $RPM_BUILD_ROOT%{_sbindir} \
	   $RPM_BUILD_ROOT%{_var}/lib/%{name} \
	   $RPM_BUILD_ROOT%{_mandir}/man8 

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install sheerdns $RPM_BUILD_ROOT%{_sbindir}
install sheerdnshash $RPM_BUILD_ROOT%{_sbindir}
install sheerdns.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
        /etc/rc.d/init.d/%{name} restart 1>&2
else
        echo "Type \"/etc/rc.d/init.d/%{name} start\" to start %{name}." 1>&2
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/%{name} ]; then
                /etc/rc.d/init.d/%{name} stop 1>&2
        fi
        /sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc sheerdns.html sheerdns.ps
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man8/%{name}.8*
%{_var}/lib/%{name}
