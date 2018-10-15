#!/usr/bin/env python
#
# Replace cvpadmin password with your own username string relevant to your installation.
# Add ay other user relevant prior to complete config provisoning from CVP.
# Replace ingest key in TerminAttr statement to match your installation.
# Replace IP in ingestgrpcurl to be relevant for your installation.
# Replace System MACs, MGMT IPs and default rouute relevant to you DC.
#

from string import Template
import subprocess

#
# Dictionary to describe DC devices
#

DC4 = {
		"5254.0033.81ba": "192.168.132.5",
		"5254.0049.b49e": "192.168.132.6",
		"5254.004a.d85b": "192.168.132.7",
		"5254.0032.f30f": "192.168.132.8",
		"defaultRoute": "192.168.132.1"
	}

#
# Fetch System MACs to index dictionary above
#

Response = subprocess.Popen(["/usr/bin/FastCli", "-c", "sho version"], stdout=subprocess.PIPE)
mac = "xx"
for Line in iter(Response.stdout.readline, ''):
 if Line.count("MAC", 0, 20):
  Fields = Line.split()
  mac = Fields[3]

IP = DC4[mac]

#
# Make ready Replacements for config Template
#

Replacements = {
				"ip": IP,
				"route": DC4["defaultRoute"]
				}

#
# Create a config template
# 

config = Template("""
!
username cvpadmin privilege 15 secret 5 $1$E6VAxeV9$rMrf9bnHXs0AkCM8RJ/kt0 
username df privilege 15 secret 5 $1$yorRLk72$Js0Z3mXVE0hydvFYGAQ0r. 
!
daemon TerminAttr
  exec /usr/bin/TerminAttr -ingestgrpcurl=192.168.130.3:9910 -taillogs -ingestauth=key,bluppfisk -smashexcludes=ale,flexCounter,hardware,kni,pulse,strata -ingestexclude=/Sysdb/cell/1/agent,/Sysdb/cell/2/agent
  no shutdown
! 
interface Management1
  ip address $ip/24
!
ip route 0.0.0.0/0 $route
!
management api http-commands
   no shutdown
!
""").safe_substiture(Replacements)

#
# Open, rewrite startup-config with the new config
#

ConfigFile = open('/mnt/flash/startup-config', 'w')
ConfigFile.write( config )
ConfigFile.close()