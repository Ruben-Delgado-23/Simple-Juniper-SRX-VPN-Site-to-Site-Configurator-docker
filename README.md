# 🛡️ Juniper SRX VPN Site-to-Site Configurator

This is a web-based tool designed to help network engineers and security professionals quickly generate a simple configuration commands for establishing **Site-to-Site VPNs on Juniper SRX firewalls**.

## 🔧 What it does

This tool allows you to input a few key VPN parameters using a guided web form and instantly generates the necessary Junos configuration commands for:

- ✅ Security zones and address-book entries
- ✅ Standard IKE proposals and policies
- ✅ IKE gateway setup
- ✅ Standard IPSec proposals and policies
- ✅ VPN tunnel configuration
- ✅ Tunnel interface and static routing
- ✅ No nat policy if required

## 💻 Technologies Used

- Python 3
- Flask
- HTML/CSS/JavaScript
- Docker (optional)

## 🚀 How to Run (Locally)

```bash
git clone https://github.com/Ruben-Delgado-23/Simple-Juniper-SRX-VPN-Site-to-Site-Configurator
cd vpn-configurator
pip install -r requirements.txt
python app.py
```

Then visit: [http://localhost:5000](http://localhost:5000)

## 🐳 Run with Docker

```bash
docker build -t vpn-configurator .
docker run -p 5000:5000 vpn-configurator
```

## 📷 Screenshot
![image](https://github.com/user-attachments/assets/918a3b4f-4abb-4323-a5e0-b8c3a3861f41)

![image](https://github.com/user-attachments/assets/138b3594-7f20-444b-a769-4be1b2445114)

## 🙌 Author

Created by **Ruben Delgado** – Network & Security Engineer
