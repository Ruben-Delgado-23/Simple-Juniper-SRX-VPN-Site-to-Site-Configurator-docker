def generate_vpn_config(data):
    zone1_name = data.get("zone1_name", "trust")
    zone1_interface = data.get("zone1_interface", "ge-0/0/0")
    zone1_ip = data.get("zone1_ip", "192.168.1.1/24")
    zone1_network = data.get("zone1_network", "192.168.1.0/24")

    zone2_name = data.get("zone2_name", "untrust")
    zone2_interface = data.get("zone2_interface", "ge-0/0/1")
    zone2_ip = data.get("zone2_ip", "1.1.1.1/30")
    zone2_network = data.get("zone2_network", "172.16.1.0/24")

    ike_secret = data.get("ike_secret", "secretkey123")

    config = []
    config.append("## Security Zones and Address Book Configuration ##\n")
    config.append(f"set security zones security-zone {zone1_name} interfaces {zone1_interface}")
    config.append(f"set interfaces {zone1_interface} unit 0 family inet address {zone1_ip}")
    config.append(f"set security address-book global address LOCAL_NETWORK {zone1_network}")
    config.append(f"set security zones security-zone {zone1_name} address-book address LOCAL_NETWORK {zone1_network}\n")

    config.append(f"set security zones security-zone {zone2_name} interfaces {zone2_interface}")
    config.append(f"set interfaces {zone2_interface} unit 0 family inet address {zone2_ip}")
    config.append(f"set security address-book global address REMOTE_NETWORK {zone2_network}")
    config.append(f"set security zones security-zone {zone2_name} address-book address REMOTE_NETWORK {zone2_network}\n")

    config.append("## Security Policies Configuration ##\n")
    config.append(f"set security policies from-zone {zone1_name} to-zone {zone2_name} policy Allow-Communication match source-address LOCAL_NETWORK")
    config.append(f"set security policies from-zone {zone1_name} to-zone {zone2_name} policy Allow-Communication match destination-address REMOTE_NETWORK")
    config.append(f"set security policies from-zone {zone1_name} to-zone {zone2_name} policy Allow-Communication match application any")
    config.append(f"set security policies from-zone {zone1_name} to-zone {zone2_name} policy Allow-Communication then permit\n")

    config.append(f"set security policies from-zone {zone2_name} to-zone {zone1_name} policy Allow-Communication match source-address REMOTE_NETWORK")
    config.append(f"set security policies from-zone {zone2_name} to-zone {zone1_name} policy Allow-Communication match destination-address LOCAL_NETWORK")
    config.append(f"set security policies from-zone {zone2_name} to-zone {zone1_name} policy Allow-Communication match application any")
    config.append(f"set security policies from-zone {zone2_name} to-zone {zone1_name} policy Allow-Communication then permit\n")

    config.append("## NAT Policy Configuration ##\n")
    config.append(f"set security nat source rule-set No-NAT from zone {zone1_name}")
    config.append(f"set security nat source rule-set No-NAT to zone {zone2_name}")
    config.append(f"set security nat source rule-set No-NAT rule No-NAT-Rule match source-address {zone1_network}")
    config.append(f"set security nat source rule-set No-NAT rule No-NAT-Rule match destination-address {zone2_network}")
    config.append(f"set security nat source rule-set No-NAT rule No-NAT-Rule then source-nat off\n")

    config.append("## Tunnel Interface and Routing ##\n")
    config.append("set interfaces st0 unit 0 family inet")
    config.append(f"set routing-options static route {zone2_network} next-hop st0.0\n")

    config.append("## IKE Proposal IKE Policy IKE Gateway ##\n")
    config.append("set security ike proposal IKE-Proposal-Standard authentication-method pre-shared-keys")
    config.append("set security ike proposal IKE-Proposal-Standard dh-group group14")
    config.append("set security ike proposal IKE-Proposal-Standard authentication-algorithm sha-256")
    config.append("set security ike proposal IKE-Proposal-Standard encryption-algorithm aes-256-cbc")
    config.append("set security ike proposal IKE-Proposal-Standard lifetime-seconds 28800\n")

    config.append("set security ike policy IKE-Policy proposals IKE-Proposal-Standard")
    config.append(f"set security ike policy IKE-Policy pre-shared-key ascii-text {ike_secret}\n")

    config.append("set security ike gateway IKE-GW ike-policy IKE-Policy")
    config.append(f"set security ike gateway IKE-GW address {zone2_ip}")
    config.append(f"set security ike gateway IKE-GW external-interface {zone2_interface}")
    config.append("set security ike gateway IKE-GW general-ikeid\n")

    config.append("## IPSEC Proposal IPSEC Policy Ipsec VPN ##\n")
    config.append("set security ipsec proposal IPSEC-Proposal-Standard-Standard protocol esp")
    config.append("set security ipsec proposal IPSEC-Proposal-Standard encryption-algorithm aes-256-cbc")
    config.append("set security ipsec proposal IPSEC-Proposal-Standard authentication-algorithm hmac-sha-256-128")
    config.append("set security ipsec proposal IPSEC-Proposal-Standard lifetime-seconds 3600\n")

    config.append("set security ipsec policy IPSEC-Policy perfect-forward-secrecy keys group5")
    config.append("set security ipsec policy IPSEC-Policy proposals IPSEC-Proposal-Standard\n")

    config.append("set security ipsec vpn VPN-TUNNEL bind-interface st0.0")
    config.append("set security ipsec vpn VPN-TUNNEL ike gateway IKE-GW")
    config.append("set security ipsec vpn VPN-TUNNEL ike ipsec-policy IPSEC-Policy")
    config.append("set security ipsec vpn VPN-TUNNEL establish-tunnels immediately\n")

    config.append("## Add st0.0 to zone, permit Ike service ##\n")
    config.append(f"set security zones security-zone {zone2_name} interfaces st0.0")
    config.append(f"set security zones security-zone {zone2_name} host-inbound-traffic system-services ike\n")

    return "\n".join(config)