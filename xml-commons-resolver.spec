Name:           xml-commons-resolver
Version:        1.2
Release:        20
Summary:        Resolver subproject of xml-commons
Group:		Development/Java
License:        ASL 2.0
URL:            http://xerces.apache.org/xml-commons/components/resolver/
Source0:        http://www.apache.org/dist/xerces/xml-commons/%{name}-%{version}.tar.gz
Source5:        %{name}-pom.xml
Source6:        %{name}-resolver.1
Source7:        %{name}-xparse.1
Source8:        %{name}-xread.1
Patch0:         %{name}-1.2-crosslink.patch
Patch1:         %{name}-1.2-osgi.patch

BuildRequires:  java-11-openjdk
BuildRequires:	javapackages-local
BuildRequires:  ant
BuildArch:      noarch

%description
Resolver subproject of xml-commons.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
BuildRequires:  java-javadoc
Requires:       java-javadoc

%description javadoc
Javadoc for %{name}.

%prep
%autosetup -p1

# remove all binary libs and prebuilt javadocs
find . -name "*.jar" -exec rm -f {} \;
rm -rf docs
sed -i 's/\r//' KEYS LICENSE.resolver.txt NOTICE-resolver.txt

%build
ant -f resolver.xml jar javadocs

%install
# Jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 644 build/resolver.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{name}.jar $RPM_BUILD_ROOT%{_javadir}/xml-resolver.jar

# Javadocs
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/apidocs/resolver/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# Scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
%jpackage_script org.apache.xml.resolver.apps.resolver "" "" %{name} xml-resolver true
%jpackage_script org.apache.xml.resolver.apps.xread "" "" %{name} xml-xread true
%jpackage_script org.apache.xml.resolver.apps.xparse "" "" %{name} xml-xparse true

# Man pages
install -d -m 755 ${RPM_BUILD_ROOT}%{_mandir}/man1
install -p -m 644 %{SOURCE6} ${RPM_BUILD_ROOT}%{_mandir}/man1/xml-resolver.1
install -p -m 644 %{SOURCE7} ${RPM_BUILD_ROOT}%{_mandir}/man1/xml-xparse.1
install -p -m 644 %{SOURCE8} ${RPM_BUILD_ROOT}%{_mandir}/man1/xml-xread.1

# Pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -p -m 644 %{SOURCE5} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files -f .mfiles
%doc KEYS LICENSE.resolver.txt NOTICE-resolver.txt
%{_mandir}/man1/*
%{_bindir}/xml-*
%{_javadir}/*

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.resolver.txt NOTICE-resolver.txt
