Name:           xml-commons-resolver
Version:        1.2
Release:        7
Summary:        Resolver subproject of xml-commons
License:        ASL 2.0
URL:            http://xml.apache.org/commons/
Source0:        http://www.apache.org/dist/xml/commons/xml-commons-resolver-%{version}.tar.gz
Source1:        xml-commons-resolver-resolver.sh
Source2:        xml-commons-resolver-xread.sh
Source3:        xml-commons-resolver-xparse.sh
Source4:        %{name}-MANIFEST.MF
Source5:        %{name}-pom.xml

Requires:       xml-commons-apis
Requires:       jpackage-utils
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  ant
BuildRequires:  jpackage-utils
BuildRequires:  zip
Group:          Development/Java
BuildArch:      noarch

%description
Resolver subproject of xml-commons.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
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
rm -rf $RPM_BUILD_ROOT

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE4} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/resolver.jar META-INF/MANIFEST.MF

# Jars
install -pD -T build/resolver.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/xml-resolver-%{version}.jar

# Jar versioning
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# Javadocs
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/apidocs/resolver/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# Scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/xml-resolver
cp %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/xml-xread
cp %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/xml-xparse

# Pom
install -pD -T -m 644 %{SOURCE5} %{buildroot}%{_mavenpomdir}/JPP-xml-resolver.pom
%add_to_maven_depmap xml-resolver xml-resolver %{version} JPP xml-resolver

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc KEYS LICENSE.resolver.txt
%{_mavendepmapfragdir}/*
%{_mavenpomdir}/*
%{_javadir}/*
%attr(0755,root,root) %{_bindir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}
%doc LICENSE.resolver.txt

