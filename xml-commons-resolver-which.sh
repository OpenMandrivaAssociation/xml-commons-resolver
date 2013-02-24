#!/bin/sh
# 
# xml-commons which script
# JPackage Project <http://www.jpackage.org/>
# $Id: xml-commons.which.script,v 1.2 2002/11/14 20:08:56 jpackage Exp $

# Source functions library
if [ -f /usr/share/java-utils/java-functions ] ; then 
  . /usr/share/java-utils/java-functions
else
  echo "Can't find functions library, aborting"
  exit 1
fi

# Configuration
MAIN_CLASS=org.apache.env.Which
BASE_JARS=xml-commons-which12.jar
CLASSPATH="$CLASSPATH:$(build-classpath ant ant-launcher xerces-j2 crimson xalan-j2 xalan-j1  xml-commons-jaxp-1.3-apis 2>/dev/null)" || :

# Set parameters
set_jvm
set_classpath $BASE_JARS
set_flags $BASE_FLAGS
set_options $BASE_OPTIONS

# Let's start
run "$@"
