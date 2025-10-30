# Multi-Country Camera Scanner - Combined Tool

<div align="center">

![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FW8SOJIB%2FW8CameraHackV2&label=Visitors&countColor=%23263759&style=flat)
![GitHub Views](https://komarev.com/ghpvc/?username=W8SOJIB&label=Profile%20Views&color=0e75b6&style=flat)
[![GitHub Stars](https://img.shields.io/github/stars/W8SOJIB/W8CameraHackV2?style=social)](https://github.com/W8SOJIB/W8CameraHackV2)
[![GitHub Forks](https://img.shields.io/github/forks/W8SOJIB/W8CameraHackV2?style=social)](https://github.com/W8SOJIB/W8CameraHackV2)

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue?style=flat&logo=python)
![Termux Support](https://img.shields.io/badge/Termux-Compatible-green?style=flat&logo=android)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20Android-lightgrey?style=flat)
![License](https://img.shields.io/badge/license-MIT-green?style=flat)
![Countries](https://img.shields.io/badge/countries-44-brightgreen?style=flat)
![One Click](https://img.shields.io/badge/operation-one--click-orange?style=flat)

### 🎯 Real-Time Visitor Counter - See Who's Visiting! 👆

</div>

A powerful tool that combines IP range collection and camera scanning functionality for **44 countries** in the Asia-Pacific region (APNIC).

## 🆕 What's New in V2?

Upgrading from [V1](https://github.com/W8SOJIB/W8CameraHackV1)? Here's what's new:

- ✅ **44 Countries Support** (V1: Bangladesh only)
- ✅ **One-Click Operation** (V1: Manual 4-step process)
- ✅ **Automatic IP Range Download** (V1: Separate step)
- ✅ **Auto-Scan After Download** (V1: Manual scan)
- ✅ **Simplified Menu** (2 options vs 5)
- ✅ **Country-Specific Output Files** (Better organization)
- ✅ **Enhanced User Interface** (Better country selection)

## Features

- 🌍 **44 Countries Supported** - Select from Afghanistan, Australia, Bangladesh, Brunei, Bhutan, Cambodia, China, Fiji, Hong Kong, India, Indonesia, Japan, South Korea, Laos, Malaysia, Myanmar, Nepal, New Zealand, Pakistan, Philippines, Singapore, Sri Lanka, Taiwan, Thailand, Vietnam, and more!
- 🌐 Fetch IPv4 ranges for any selected country from APNIC database
- 📹 Scan for IP cameras and web services
- 🔍 Detect multiple camera brands:
  - **Anjhua-Dahua Technology Cameras**
  - **HIK Vision Cameras**
- 💾 Live save - Results saved instantly as they're found
- 💻 Termux compatible (Android)
- 🎨 Colorful terminal interface
- 🚀 Multi-threaded scanning (100 threads)
- 📊 Detailed camera information (IP, Port, URL, Timestamp)
- 🗂️ Organized output - Separate files for each country

## Download Camera Live View App

https://w8team.top/W8SOJIB//index.php?user/publicLink&fid=eeb7f4Fmgo5rHTKhT4KOm61nzgob0933QBWTguLs9XTdkVbmCloYXbIU6Ey6Y8rO6LgHsh1bZXTzhDGz9ZE3w3i5Snp2e5VopypU6G5jzwXw1W8bsms3uQ&file_name=/DMSS_1_99_623_222.apk

Altanitive.. https://gofile.io/d/fr8rOB


## Installation

### Quick Install (Recommended)

#### For Termux (Android)

```bash
# Clone the repository
git clone https://github.com/W8SOJIB/W8CameraHackV2
cd W8CameraHackV2

# Run automatic installer
bash install.sh
```

#### For Desktop (Windows/Linux/Mac)

```bash
# Clone the repository
git clone https://github.com/W8SOJIB/W8CameraHackV2
cd W8CameraHackV2

# Install dependencies
pip install requests aiohttp pyfiglet colorama
```

### Manual Installation

#### For Termux (Android)

```bash
# Update packages
pkg update && pkg upgrade

# Install required packages
pkg install python git

# Clone repository
git clone https://github.com/W8SOJIB/W8CameraHackV2
cd W8CameraHackV2

# Install Python dependencies
pip install requests aiohttp pyfiglet

# Optional: For colors (if colorama install fails, the script works without it)
pip install colorama
```

#### For Desktop (Windows/Linux/Mac)

```bash
# Clone repository
git clone https://github.com/W8SOJIB/W8CameraHackV2
cd W8CameraHackV2

# Install Python dependencies
pip install requests aiohttp pyfiglet colorama
```

## Usage

Run the script:
```bash
python W8CameraHackV2.py
```

### Menu Options

1. **Select Country & Scan** - Choose from 44 supported countries and automatically fetch IP ranges + scan for cameras
2. **Exit** - Quit the program

**Simple Workflow:** Select a country → Script automatically downloads IP ranges → Scans for cameras → Done!

### 🌍 Supported Countries (44 Total)

Afghanistan, Australia, Bangladesh, Brunei, Bhutan, Cambodia, China, Cook Islands, Fiji, Micronesia, Guam, Hong Kong, India, Indonesia, Japan, Kiribati, South Korea, Sri Lanka, Laos, Myanmar, Mongolia, Macau, Maldives, Malaysia, New Caledonia, Nepal, Nauru, New Zealand, French Polynesia, Papua New Guinea, Philippines, Pakistan, North Korea, Palau, Solomon Islands, Singapore, Thailand, Timor-Leste, Tonga, Taiwan, Vanuatu, Vietnam, Samoa, and United States (APNIC region)

### 🎮 Scan Controls

During scanning, you can use:
- **Ctrl+C** - ⛔ Stop scan immediately (instant exit)
- **Ctrl+Z** - ⏸️ Pause/Resume scan (toggle on Linux/Mac/Termux)

## Output Files

- `[COUNTRY_CODE]_IP.txt` - Contains IP ranges for selected country in CIDR notation (e.g., `BD_IP.txt`, `IN_IP.txt`, `PK_IP.txt`)
- `[COUNTRY_CODE]_CCTV_Found.txt` - All detected cameras with details for that country (Live Save)
  - **Anjhua-Dahua Technology Cameras** (WEB SERVICE detection)
  - **HIK Vision Cameras** (login.asp detection)

### Output Format

Each detected camera is saved with:
- Camera Type (Brand/Model)
- IP Address
- Port Number
- Full URL
- Detection Timestamp
- Live saving (results appear immediately!)

**Example Output:**
```
============================================================
Camera Type: Anjhua-Dahua Technology Camera
IP Address: 192.168.1.100
Port: 80
URL: http://192.168.1.100
Detection Time: 2025-10-01 14:30:45
============================================================
```

See `SAMPLE_OUTPUT.txt` for more examples.

## How It Works

1. **Country Selection**: Choose from 44 countries in the Asia-Pacific region (APNIC)
2. **Automatic IP Range Collection**: Automatically fetches IPv4 ranges for the selected country from APNIC's delegation database
3. **CIDR Parsing**: Converts custom CIDR notation (IP/count) to individual IP addresses
4. **Auto-Scan**: Immediately starts scanning after IP range download
5. **Multi-threaded Scanning**: Uses 100 threads to scan ports 80 and 8080 simultaneously
6. **Detection**: Identifies cameras by looking for specific HTML titles and patterns
7. **Country-Specific Output**: Saves results to separate files for each country

**One-Click Operation:** Select country → Everything happens automatically! 🚀

## Ports Scanned

- Port 80 (HTTP)
- Port 8080 (HTTP Alternative)

## Notes

- The scanner uses a 0.25 second timeout per connection
- Results are saved in real-time to output files (Live Save with `file.flush()`)
- **Instant Stop**: Press Ctrl+C to stop scanning immediately (no delay!)
- **Pause/Resume**: Press Ctrl+Z to pause and resume (Linux/Mac/Termux only)
- The tool is optimized for Termux with fallback color codes if colorama is not available
- All worker threads properly handle stop signals for clean shutdown

## Legal Disclaimer

This tool is for educational and authorized security testing purposes only. Always obtain proper authorization before scanning networks you don't own.

## Credits

<div align="center">

### 👨‍💻 Developed by: W8Team/W8SOJIB

[![GitHub](https://img.shields.io/badge/GitHub-W8SOJIB-181717?style=for-the-badge&logo=github)](https://github.com/W8SOJIB)
[![Profile Views](https://komarev.com/ghpvc/?username=W8SOJIB&label=Profile%20Views&color=blueviolet&style=for-the-badge)](https://github.com/W8SOJIB)

**Team:** W8Team  
**Contact:** [GitHub Profile](https://github.com/W8SOJIB)

</div>

### 📊 Repository Stats

![Repo Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FW8SOJIB%2FW8CameraHackV2&labelColor=%23697689&countColor=%23ff8a65&style=plastic&labelStyle=upper)
![GitHub code size](https://img.shields.io/github/languages/code-size/W8SOJIB/W8CameraHackV2?style=plastic)
![GitHub repo size](https://img.shields.io/github/repo-size/W8SOJIB/W8CameraHackV2?style=plastic)

### Version History
- 🆕 **V2** - Multi-Country Scanner (44 Countries, One-Click Operation)
- 📌 **[V1](https://github.com/W8SOJIB/W8CameraHackV1)** - Bangladesh Only Scanner (Legacy)

### Original Components
- 📡 All ASN Collector (IP Range Fetcher)
- 📹 W8IPCameraHK V4 (Camera Scanner)
- 🔧 Combined & Optimized by W8SOJIB for Termux Support
- 🌍 Enhanced V2: Multi-Country Support + Auto-Scan

---

<div align="center">

**⭐ If you like this project, please give it a star! ⭐**

Made with ❤️ by [W8Team/W8SOJIB](https://github.com/W8SOJIB)

</div>


