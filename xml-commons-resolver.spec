Summary:	Resolver subproject of xml-commons
Name:		xml-commons-resolver
Epoch:		1
Version:	1.2
Release:	11
License:	ASL 2.0
Group:		Development/Java
Url:		http://xerces.apache.org/xml-commons/
# Packaged directly from svn instead of downloading the tarball because the
# official tarball is missing which.xml and friends (see below)
# svn export http://svn.apache.org/repos/asf/xerces/xml-commons/tags/xml-commons-resolver-1_2/ xml-commons-resolver-1.2
# tar cJf xml-commons-resolver-1.2.tar.xz xml-commons-resolver-1.2
Source0:	http://www.apache.org/dist/xml/commons/xml-commons-resolver-%{version}.tar.xz
Source1:	xml-commons-resolver-resolver.sh
Source2:	xml-commons-resolver-xread.sh
Source3:	xml-commons-resolver-xparse.sh
Source4:	xml-commons-resolver-which.sh
Source5:	%{name}-MANIFEST.MF
Source6:	%{name}-pom.xml
BuildArch:	noarch

BuildRequires:	java-devel >= 0:1.6.0
BuildRequires:	ant
BuildRequires:	jpackage-utils
BuildRequires:	zip
Requires:	xml-commons-apis
Requires:	jpackage-utils
Requires(post,postun):   jpackage-utils

Provides:	xml-commons-resolver12 = %EVRD
Obsoletes:	xml-commons-resolver12 < %EVRD
Provides:	xml-commons-which12 = %EVRD
Obsoletes:	xml-commons-which12 < %EVRD
Provides:	xml-commons-which = %EVRD
Obsoletes:	xml-commons-which < %EVRD

# There's probably no need to keep the legacy versions around since (unlike
# xml-commons-apis or the likes) there don't seem to be any incompatible
# API changes.
# To be on the safe side, let's obsolete the old versions without providing
# them so we can just reintroduce the legacy packages at some point in the future
# if needed.
Obsoletes:	xml-commons-resolver11 < 1:1.1-0
Obsoletes:	xml-commons-resolver10 < 1:1.0-0
Obsoletes:	xml-commons-which11 < 1:1.1-0
Obsoletes:	xml-commons-which10 < 1:1.0-0

%track
prog %name = {
	url = http://xerces.apache.org/mirrors.cgi
	regex = "XML Commons Resolver Version (__VER__) - tar.gz"
	version = %version
}

%description
Resolver subproject of xml-commons.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java
Requires:	jpackage-utils
Provides:	xml-commons-resolver12-javadoc = %EVRD
Obsoletes:	xml-commons-resolver12-javadoc < %EVRD
Provides:	xml-commons-which-javadoc = %EVRD
Obsoletes:	xml-commons-which-javadoc < %EVRD
Provides:	xml-commons-which12-javadoc = %EVRD
Obsoletes:	xml-commons-which12-javadoc < %EVRD
Obsoletes:	xml-commons-resolver11-javadoc < 1:1.1-0
Obsoletes:	xml-commons-resolver10-javadoc < 1:1.0-0
Obsoletes:	xml-commons-which11-javadoc < 1:1.1-0
Obsoletes:	xml-commons-which10-javadoc < 1:1.0-0

%description javadoc
Javadoc for %{name}.

%prep
%setup -q

# remove all binary libs and prebuilt javadocs
find . -name "*.jar" -exec rm -f {} \;
rm -rf docs
sed -i 's/\r//' KEYS LICENSE

%build
sed -i -e 's|call Resolver|call resolver|g' java/resolver.xml
sed -i -e 's|classname="org.apache.xml.resolver.Catalog"|fork="yes" classname="org.apache.xml.resolver.apps.resolver"|g' java/resolver.xml
sed -i -e 's|org.apache.xml.resolver.Catalog|org.apache.xml.resolver.apps.resolver|g' java/src/manifest.resolver

ant jars javadocs

%install
# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE5} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u java/build/resolver.jar META-INF/MANIFEST.MF

# Jars
install -pD -T java/build/resolver.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/xml-resolver-%{version}.jar

# Jar versioning
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# Javadocs
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr java/build/apidocs/resolver java/build/apidocs/which %{buildroot}%{_javadocdir}/%{name}

# Scripts
mkdir -p %{buildroot}%{_bindir}
cp %{SOURCE1} %{buildroot}%{_bindir}/xml-resolver
cp %{SOURCE2} %{buildroot}%{_bindir}/xml-xread
cp %{SOURCE3} %{buildroot}%{_bindir}/xml-xparse
cp %{SOURCE4} %{buildroot}%{_bindir}/xml-which

# Pom
install -pD -T -m 644 %{SOURCE6} %{buildroot}%{_mavenpomdir}/JPP-xml-resolver.pom
%add_to_maven_depmap xml-resolver xml-resolver %{version} JPP xml-resolver

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%doc KEYS LICENSE
%{_mavendepmapfragdir}/*
%{_mavenpomdir}/*
%{_javadir}/*
%{_bindir}/*

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE

