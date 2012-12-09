#!/bin/sh
# 
# xml-commons-resolver resolver script
# JPackage Project (http://www.jpackage.org/)
# $Id: xml-commons-resolver-resolver.sh,v 1.1 2004/09/09 14:51:13 cvsdist Exp $

# Source functions library
. /usr/share/java-utils/java-functions

# Configuration
MAIN_CLASS=org.apache.xml.resolver.apps.resolver
BASE_JARS="xml-commons-resolver.jar xml-commons-apis.jar jaxp_parser_impl.jar"

# Set parameters
set_jvm
set_classpath $BASE_JARS
set_flags $BASE_FLAGS
set_options $BASE_OPTIONS

# Let's start
run "$@"
