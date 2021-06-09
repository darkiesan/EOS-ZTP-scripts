#!/usr/bin/python

from string import Template
import subprocess

fastcli = '/usr/bin/FastCli -p 15'
reloadcmd="""
reload
"""

DC = [ 
	{ 'name':'dc1', 'links':'192.168.127.', 'management':'192.168.126.', 'loopbacks':'192.168.128.', 'vxlan':'192.168.129.', 'CVX':'192.168.128.0', 'defroute':'192.168.126.1' },
	{ 'name':'dc3', 'links':'192.168.123.', 'management':'192.168.122.', 'loopbacks':'192.168.124.', 'vxlan':'192.168.125.','CVX':'192.168.124.0', 'defroute':'192.168.122.1' }
]

Switches = [ 
	{ 	'hostname': 'dc1-spine1',
		'MAC':'5254.0048.28d5',
		'Number':'2',
		'DC':'dc1',
		'POD':'pod1',
		'role':'spine',
		'interfaces': {
				'Management1': { 'name': 'Management1', 'type': 'management' },
				'Ethernet1': { 'name': 'Ethernet1', 'type': 'uplink' },
				'Ethernet2': { 'name': 'Ethernet2', 'type': 'uplink' },
				'Ethernet3': { 'name': 'Ethernet3', 'type': 'unused' },
				'Loopback0': { 'name': 'Loopback0', 'type': 'loopback' }
			}
	},

	{ 	'hostname': 'dc1-spine2', 
		'MAC':'5254.002f.ca24',
		'Number':'3',
		'DC':'dc1',
		'POD':'pod1',
		'role':'spine',
		'interfaces': {
				'Management1': { 'name': 'Management1', 'type': 'management' },
				'Ethernet1': { 'name': 'Ethernet1', 'type': 'uplink' },
				'Ethernet2': { 'name': 'Ethernet2', 'type': 'uplink' },
				'Ethernet3': { 'name': 'Ethernet3', 'type': 'unused' },
				'Loopback0': { 'name': 'Loopback0', 'type': 'loopback' }
			}
	},

	{ 	'hostname': 'dc1-leaf1', 
		'MAC':'5254.0026.3c07',
		'Number':'4',
		'DC':'dc1',
		'POD':'pod1',
		'role':'spine',
		'interfaces': {
				'Management1': { 'name': 'Management1', 'type': 'management' },
				'Ethernet1': { 'name': 'Ethernet1', 'type': 'uplink' },
				'Ethernet2': { 'name': 'Ethernet2', 'type': 'uplink' },
				'Ethernet3': { 'name': 'Ethernet3', 'type': 'unused' },
				'Loopback0': { 'name': 'Loopback0', 'type': 'loopback' },
				'Loopback1': { 'name': 'Loopback1', 'type': 'vxlan' }
			}
	},

	{ 	'hostname': 'dc1-leaf2', 
		'MAC':'5254.0046.0e58',
		'Number':'5',
		'DC':'dc1',
		'POD':'pod1',
		'role':'leaf',
		'interfaces': {
				'Management1': { 'name': 'Management1', 'type': 'management' },
				'Ethernet1': { 'name': 'Ethernet1', 'type': 'uplink' },
				'Ethernet2': { 'name': 'Ethernet2', 'type': 'uplink' },
				'Ethernet3': { 'name': 'Ethernet3', 'type': 'unused' },
				'Loopback0': { 'name': 'Loopback0', 'type': 'loopback' },
				'Loopback1': { 'name': 'Loopback1', 'type': 'vxlan' }
			}
	},

	{ 	'hostname': 'dc3-spine1', 
		'MAC': '5254.0024.e852',
		'Number':'2',
		'DC':'dc3',
		'POD':'pod1',
		'role':'leaf',
		'interfaces': {
				'Management1': { 'name': 'Management1', 'type': 'management' },
				'Ethernet1': { 'name': 'Ethernet1', 'type': 'uplink' },
				'Ethernet2': { 'name': 'Ethernet2', 'type': 'uplink' },
				'Ethernet3': { 'name': 'Ethernet3', 'type': 'unused' },
				'Loopback0': { 'name': 'Loopback0', 'type': 'loopback' }
			}
	},

	{ 	'hostname': 'dc3-spine2', 
		'MAC': '5254.0059.dbab',
		'Number':'3',
		'DC':'dc3',
		'POD':'pod1',
		'role':'spine',
		'interfaces': {
				'Management1': { 'name': 'Management1', 'type': 'management' },
				'Ethernet1': { 'name': 'Ethernet1', 'type': 'uplink' },
				'Ethernet2': { 'name': 'Ethernet2', 'type': 'uplink' },
				'Ethernet3': { 'name': 'Ethernet3', 'type': 'unused' },
				'Loopback0': { 'name': 'Loopback0', 'type': 'loopback' }
			}
	},

	{ 	'hostname': 'dc3-leaf1', 
		'MAC': '5254.0027.1564',
		'Number':'4',
		'DC':'dc3',
		'POD':'pod1',
		'role':'leaf',
		'interfaces': {
				'Management1': { 'name': 'Management1', 'type': 'management' },
				'Ethernet1': { 'name': 'Ethernet1', 'type': 'uplink' },
				'Ethernet2': { 'name': 'Ethernet2', 'type': 'uplink' },
				'Ethernet3': { 'name': 'Ethernet3', 'type': 'unused' },
				'Loopback0': { 'name': 'Loopback0', 'type': 'loopback' },
				'Loopback1': { 'name': 'Loopback1', 'type': 'vxlan' }
			}
	},

	{ 	'hostname': 'dc3-leaf2', 
		'MAC': '5254.006d.2958',
		'Number':'5',
		'DC':'dc3',
		'POD':'pod1',
		'role':'leaf',
		'interfaces': {
				'Management1': { 'name': 'Management1', 'type': 'management' },
				'Ethernet1': { 'name': 'Ethernet1', 'type': 'uplink' },
				'Ethernet2': { 'name': 'Ethernet2', 'type': 'uplink' },
				'Ethernet3': { 'name': 'Ethernet3', 'type': 'unused' },
				'Loopback0': { 'name': 'Loopback0', 'type': 'loopback' },
				'Loopback1': { 'name': 'Loopback1', 'type': 'vxlan' }
			}
	}
]


Response = subprocess.Popen(["/usr/bin/FastCli", "-c", "sho version"], stdout=subprocess.PIPE)

mac = "xx"

for Line in iter(Response.stdout.readline, ''):
 if Line.count("MAC", 0, 20):
  Fields = Line.split()
  mac = Fields[3]

n=0
ListLen = len(Switches)

while n < ListLen:
 if Switches[n]['MAC'] == mac:
  myHostname = Switches[n]['hostname']
  Systemid = Switches[n]['Number']

  myDC = Switches[n]['DC']
  i = 0
  iListLen = len(DC)
  while i < iListLen:
   if DC[i]['name'] == myDC:
    CVXServer = DC[i]['CVX']
    myRoute = DC[i]['defroute']
    myMgmtIP = DC[i]['management'] + Systemid
    myLoopbackIP = DC[i]['loopbacks'] + Systemid
    myVXLANIP = DC[i]['vxlan'] + Systemid
   i=i+1

 n=n+1

Replacements = { "Number": Systemid, 
                 "myHostname": myHostname,
		 "CVXServer": CVXServer,
		 "myRoute": myRoute,
		 "myMgmtIP": myMgmtIP,
		 "myLoopbackIP": myLoopbackIP,
		 "myVXLANIP": myVXLANIP
		}

Config = Template("""
! Default ZTP-created config
!
transceiver qsfp default-mode 4x10G
!
hostname $myHostname
!
snmp-server community private rw
snmp-server community public ro
!
spanning-tree mode mstp
!
no aaa root
!
username becs privilege 15 secret 5 $1$edXmdxfz$lwH8NTWgA/q3DC8a456JN0
username cvpadmin privilege 15 secret 5 $1$E6VAxeV9$rMrf9bnHXs0AkCM8RJ/kt0
username df privilege 15 secret 5 $1$yorRLk72$Js0Z3mXVE0hydvFYGAQ0r.
!
interface Loopback0
 ip address $myLoopbackIP/32
!
interface Loopback1
 ip address $myVXLANIP/32
!
interface Management1
 ip address $myMgmtIP/24
!
interface Vxlan1
   vxlan source-interface Loopback1
   vxlan controller-client
   vxlan udp-port 4789
!
ip virtual-router mac-address 00:11:22:33:44:55
!
ip route 0.0.0.0/0 $myRoute
!
ip routing
!
management cvx
 no shutdown
 server host $CVXServer
!
management api http-commands
 protocol http
 cors allowed-origin all
 no shutdown 
!
end
""").safe_substitute(Replacements)
  
ConfigFile = open('/mnt/flash/startup-config', 'w')
ConfigFile.write( Config )
ConfigFile.close()
returnCode = subprocess.call("echo \"" + reloadcmd + "\" | " + fastcli, shell=True)
