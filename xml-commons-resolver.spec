%{?_javapackages_macros:%_javapackages_macros}
Name:           xml-commons-resolver
Version:        1.2
Release:        14.1%{?dist}
%if 0%{?fedora}
Epoch:          0
%else
# FIXME epoch in mandriva...
Epoch:          1
%endif
Summary:        Resolver subproject of xml-commons
License:        ASL 2.0
URL:            http://xml.apache.org/commons/
Source0:        http://www.apache.org/dist/xml/commons/xml-commons-resolver-%{version}.tar.gz
Source1:        xml-commons-resolver-resolver.sh
Source2:        xml-commons-resolver-xread.sh
Source3:        xml-commons-resolver-xparse.sh
Source4:        %{name}-MANIFEST.MF
Source5:        %{name}-pom.xml
Source6:        %{name}-resolver.1
Source7:        %{name}-xparse.1
Source8:        %{name}-xread.1

Requires:       xml-commons-apis
Requires:       jpackage-utils
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  ant
BuildRequires:  jpackage-utils
BuildRequires:  zip

BuildArch:      noarch

%description
Resolver subproject of xml-commons.

%package javadoc
Summary:        Javadoc for %{name}

Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q

# remove all binary libs and prebuilt javadocs
find . -name "*.jar" -exec rm -f {} \;
rm -rf docs
sed -i 's/\r//' KEYS LICENSE.resolver.txt

%build
sed -i -e 's|call Resolver|call resolver|g' resolver.xml
sed -i -e 's|classname="org.apache.xml.resolver.Catalog"|fork="yes" classname="org.apache.xml.resolver.apps.resolver"|g' resolver.xml
sed -i -e 's|org.apache.xml.resolver.Catalog|org.apache.xml.resolver.apps.resolver|g' src/manifest.resolver

ant -f resolver.xml jar javadocs

%install
# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE4} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/resolver.jar META-INF/MANIFEST.MF

# Jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 644 build/resolver.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{name}.jar $RPM_BUILD_ROOT%{_javadir}/xml-resolver.jar

# Javadocs
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/apidocs/resolver/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# Scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/xml-resolver
cp %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/xml-xread
cp %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/xml-xparse

# Man pages
install -d -m 755 ${RPM_BUILD_ROOT}%{_mandir}/man1
install -p -m 644 %{SOURCE6} ${RPM_BUILD_ROOT}%{_mandir}/man1/xml-resolver.1
install -p -m 644 %{SOURCE7} ${RPM_BUILD_ROOT}%{_mandir}/man1/xml-xparse.1
install -p -m 644 %{SOURCE8} ${RPM_BUILD_ROOT}%{_mandir}/man1/xml-xread.1

# Pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -p -m 644 %{SOURCE5} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%doc KEYS LICENSE.resolver.txt
%{_mavendepmapfragdir}/*
%{_mavenpomdir}/*
%{_javadir}/*
%{_mandir}/man1/*
%attr(0755,root,root) %{_bindir}/*

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.resolver.txt

%changelog
* Thu Aug 15 2013 Mat Booth <fedora@matbooth.co.uk> - 0:1.2-14
- Fix FTBFS rhbz #993143

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 11 2013 Michal Srb <msrb@redhat.com> - 0:1.2-12
- Add man pages (Resolves: rhbz#949424)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 17 2012 Andy Grimm <agrimm@gmail.com> - 0:1.2-10
- Remove osgi(system.bundle) requirement

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 3 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.2-6
- Fix merge review comments (bug#226564).

* Wed Nov 3 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.2-5
- Add missing zip BR.
- Remove perl and dos2unix usage.
- Fix license - ASL 2.0 now.

* Fri Sep 24 2010 Mat Booth <fedora@matbooth.co.uk> 0:1.2-4
- Forgot to actually install a jar with a name that maven users expect.

* Sun Sep 19 2010 Mat Booth <fedora@matbooth.co.uk> 0:1.2-3
- Install a maven pom and depmap.

* Wed Apr 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.2-2
- No need to require jaxp_parser_impl now that we require java 1.5 or newer.

* Fri Mar 5 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.2-1
- Update to 1.2.
- Drop gcj_support.

* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0:1.1-4.17
- Fix Group tags
- Remove '.' at end of Summary
- Add dos2unix BR and fix line endings
- Use upstream tarball

* Sat Aug  8 2009 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1-4.16
- Fix specfile UTF-8 encoding.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-4.15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-3.15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-2.15
- Install osgi manifest for eclipse-dtp

* Fri Sep 05 2008 Deepak Bhole <dbhole@redhat.com> 1.1-2.14
- Build with IcedTea to escape sinjdoc issues

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.1-2.13
- drop repotag
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.1-2jpp.12
- Autorebuild for GCC 4.3

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> 1.1-1jpp.12
- Added missing dependencies.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.1-1jpp_11fc
- Rebuilt

* Fri Jul 21 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.1-1jpp_10fc
- Added conditional native compilation.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:1.1-1jpp_9fc
- rebuild

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:1.1-1jpp_8fc
- stop scriptlet spew

* Wed Dec 21 2005 Jesse Keating <jkeating@redhat.com> 0:1.1-1jpp_7fc
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 0:1.1-1jpp_6fc
- rebuilt

* Tue Jun 28 2005 Gary Benson <gbenson@redhat.com> 0:1.1-1jpp_5fc
- Remove jarfile from the tarball.

* Thu Nov  4 2004 Gary Benson <gbenson@redhat.com> 0:1.1-1jpp_4fc
- Build into Fedora.

* Thu Oct 28 2004 Gary Benson <gbenson@redhat.com> 0:1.1-1jpp_3fc
- Bootstrap into Fedora.

* Thu Mar  4 2004 Frank Ch. Eigler <fche@redhat.com> 0:1.1-1jpp_2rh
- RH vacuuming part II

* Wed Mar  3 2004 Frank Ch. Eigler <fche@redhat.com> 0:1.1-1jpp_1rh
- RH vacuuming

* Wed Jan 21 2004 David Walluck <david@anti-microsoft.org> 0:1.1-1jpp
- 1.1
- use perl instead of patch
- don't build docs (build fails)

* Tue May 06 2003 David Walluck <david@anti-microsoft.org> 0:1.0-2jpp
- update for JPackage 1.5

* Wed Nov 13 2002 Ville Skyttä <ville.skytta at iki.fi> - 1.0-1jpp
- Follow upstream changes, split out of xml-commons.
