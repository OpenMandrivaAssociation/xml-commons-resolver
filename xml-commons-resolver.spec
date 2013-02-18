Summary:	Resolver subproject of xml-commons
Name:		xml-commons-resolver
Version:	1.2
Release:	10
License:	ASL 2.0
Group:		Development/Java
Url:		http://xml.apache.org/commons/
Source0:	http://www.apache.org/dist/xml/commons/xml-commons-resolver-%{version}.tar.gz
Source1:	xml-commons-resolver-resolver.sh
Source2:	xml-commons-resolver-xread.sh
Source3:	xml-commons-resolver-xparse.sh
Source4:	%{name}-MANIFEST.MF
Source5:	%{name}-pom.xml
BuildArch:	noarch

BuildRequires:	java-devel >= 0:1.6.0
BuildRequires:	ant
BuildRequires:	jpackage-utils
BuildRequires:	zip
Requires:	xml-commons-apis
Requires:	jpackage-utils
Requires(post,postun):   jpackage-utils

Provides:	xml-commons-resolver12 = %version-%release

%description
Resolver subproject of xml-commons.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java
Requires:	jpackage-utils

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
install -pD -T build/resolver.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/xml-resolver-%{version}.jar

# Jar versioning
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# Javadocs
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr build/apidocs/resolver/* %{buildroot}%{_javadocdir}/%{name}

# Scripts
mkdir -p %{buildroot}%{_bindir}
cp %{SOURCE1} %{buildroot}%{_bindir}/xml-resolver
cp %{SOURCE2} %{buildroot}%{_bindir}/xml-xread
cp %{SOURCE3} %{buildroot}%{_bindir}/xml-xparse

# Pom
install -pD -T -m 644 %{SOURCE5} %{buildroot}%{_mavenpomdir}/JPP-xml-resolver.pom
%add_to_maven_depmap xml-resolver xml-resolver %{version} JPP xml-resolver

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%doc KEYS LICENSE.resolver.txt
%{_mavendepmapfragdir}/*
%{_mavenpomdir}/*
%{_javadir}/*
%{_bindir}/*

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.resolver.txt

