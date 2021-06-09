#!/usr/bin/python

from string import Template
import subprocess

fastcli = '/usr/bin/FastCli -p 15'
reloadcmd="""
reload
"""

Config = """
! Default ZTP-created config
!
transceiver qsfp default-mode 4x10G
!
hostname salem-core1
!
clock timezone CET
!
ntp server vrf MGT 162.159.200.1 prefer version 4
!
hardware tcam
   system profile vxlan-routing
!
spanning-tree mode mstp
!
no spanning-tree vlan-id 4094
!
vlan 4094
 name MLAG
 trunk group mlagpeer
!
!
vlan 1
	name switchar
!
vlan 2
	name Externt
!
vlan 10
	name Vlan10
!
vlan 12
	name E-skogsang
!
vlan 30
	name SALEM-CGI
!
vlan 50
	name Tele
!
vlan 100
	name Salem
!
vlan 109
	name E-GY
!
vlan 110
	name E-GY
!
vlan 161
	name ADM_Wireless
!
vlan 164
	name ADM-Ronninge
!
vlan 165
	name ADM-Gymnasie
!
vlan 166
	name ADM-Skyttorp
!
vlan 167
	name ADM-Driften
!
vlan 169
	name ADM-Sabyhemm
!
vlan 174
	name Ronninge
!
vlan 176
	name Gymnasiet
!
vlan 178
	name Edu-Resource
!
vlan 181
	name D-DMZ
!
vlan 200
	name Elev
!
vlan 220
	name TAC-MSB
!
vlan 222
	name MGMT_222
!
vlan 250
	name Tele2-VoIP
!
vlan 255
	name L3-Link-Adm
!
vlan 810
	name iSCSI-A
!
vlan 812
	name M-MGMT
!
vlan 1029
	name Tele2Upplink
!
vlan 1073
	name SkogsangenIPAD
!
vlan 1074
	name SabyIPAD
!
vlan 1501
	name NEW_INTRANET
!
vlan 1520
	name NEW_SERVER_VLAN
!
vlan 1521
	name NEW_INTRA
!
vlan 1522
	name Clients-VPN
!
vlan 1523
	name NetworkAdmin
!
vlan 1610
	name ADM-Syslagar
!
vlan 1611
	name A-Nytorp
!
vlan 1612
	name ADM-Prastgar
!
vlan 1614
	name A-Hus01
!
vlan 1615
	name ADM-Skogsang
!
vlan 1616
	name ADM-SabyMusi
!
vlan 1617
	name YttreEnheter
!
vlan 1618
	name HQ-Pers-It
!
vlan 1619
	name A-Staben
!
vlan 1620
	name A-Service
!
vlan 1622
	name A-Bibl
!
vlan 1623
	name A-Social
!
vlan 1628
	name Larm_Passage
!
vlan 1629
	name A-Bou
!
vlan 1630
	name A-Fritidsgarden
!
vlan 1633
	name ADM-MSB
!
vlan 1641
	name Solglantan
!
vlan 1642
	name ServsBo1
!
vlan 1643
	name korsbarsgarden
!
vlan 1644
	name sjostugan
!
vlan 1647
	name jagergarden
!
vlan 1680
	name MAG2600
!
vlan 1691
	name Sabytorgsvagen8c
!
vlan 1699
	name T-LABB
!
vlan 1710
	name Nytorp
!
vlan 1714
	name E-Hus01
!
vlan 1748
	name E-AteaVaxjo
!
vlan 1900
	name SalemNET
!
vlan 2030
	name Gastnat
!
vlan 2031
	name RADIONAT
!
vlan 2032
	name L3-Salembase-Edu
!
vlan 2033
	name Radio-MGMT
!
vlan 2034
	name escription
!
vlan 2040
	name GUESTNET-ADM
!
vlan 2050
	name Guest-Telia
!
vlan 2143
	name NAME-ME
!
vlan 2144
	name Telia
!
vlan 2145
	name LarmsystemTelia
!
vlan 2146
	name Telenor
!
vlan 2220
	name NAME-NE
!
vlan 3900
	name Unify-SabSko
!
vlan 3901
	name Unifi-SkySko
!
vlan 3902
	name Unifi-RonSko
!
vlan 3903
	name Unifi-RonGym
!
vlan 3904
	name Unifi-NytSko
!
vlan 3905
	name Unifi-SkoSko
!
vlan 3906
	name Unifi-Huset
!
vlan 3907
	name Unifi-
!
vlan 4000
	name PtP-Familjecentralen
!
vlan 4001
	name PTP-SKyttorp
!
vlan 4002
	name PTP-servicebonde
!
no aaa root
!
username cvpadmin privilege 15 secret 5 $1$E6VAxeV9$rMrf9bnHXs0AkCM8RJ/kt0
username df privilege 15 secret 5 $1$yorRLk72$Js0Z3mXVE0hydvFYGAQ0r.
!
vrf instance MGMT
!
vrf instance Adm
!
vrf instance Edu
!
ip routing vrf MGMT
!
ip routing vrf Adm
!
ip routing vrf Edu
!
interface port-Channel 2000
   description MLAG
   switchport mode trunk
   switchport trunk group mlagpeer
!
interface vlan 4094
   description MLAG
   mtu 9100
   ip address 10.0.0.0/31
!
interface Ethernet47
   channel-group 2000 mode active
!
interface Ethernet48
   channel-group 2000 mode active
!
interface Management1
 ip address 172.31.250.1/24
!
ip virtual-router mac-address 00:11:22:33:44:55
!
ip route vrf MGMT 0.0.0.0/0 172.31.250.254
!
ip routing
!
router bgp 65000
   neighbor MLAG peer group
   neighbor MLAG remote-as 65000
   neighbor MLAG send-community
   neighbor 10.0.0.1 peer group MLAG
!
management api http-commands
 protocol http
 no shutdown 
 vrf MGMT
   no shutdown
!
mlag
 local-interface vlan 4094
 peer-address 10.0.0.1
 peer-link port-channel 2000
 domain-id MLAG
!
end
"""
  
ConfigFile = open('/mnt/flash/startup-config', 'w')
ConfigFile.write( Config )
ConfigFile.close()
returnCode = subprocess.call("echo \"" + reloadcmd + "\" | " + fastcli, shell=True)
