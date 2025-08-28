Notes:

DAE-05 ParrotOS - 192.168.1.30
DAE-08 Win11VM - 192.168.1.1

Set up my two Virtual Machines two seperate laptops

DAE-05, my main laptop is using ParrotOS, which will be designated as the attacker

DAE-08, my secondary laptop is using Windows 11, which will be designated as the defender.

Simulated Attacks so far 

[x] Login Phishing using ParrotOS Social Engineering Toolkit (ParrotOS Social Engineering Toolkit)

[] Brute force using Hydra from Attacker and will guess my password setup on my Windows 11 VM

# 🖥️ FTP Server Setup on Windows 11 (For Lab Use Only)

> ⚠️ This setup is intended for educational use in a controlled lab environment.

---

## ✅ Step 1: Enable FTP Server in Windows Features

1. Press `Win + S` and search for **"Windows Features"**
2. Open **"Turn Windows features on or off"**
3. Check the following boxes:
   - ✅ Internet Information Services
     - ✅ FTP Server
       - ✅ FTP Service
     - ✅ Web Management Tools
4. Click **OK** to install the required features

---

## ⚙️ Step 2: Configure FTP Site Using IIS

1. Press `Win + S`, search for **"IIS"**, and open **Internet Information Services (IIS) Manager**
2. In the left panel, right-click **Sites** > **Add FTP Site**
3. Name: `FTPTest`
4. Physical path: e.g., `C:\FTPTest`
5. Click **Next**

### Binding and SSL:
- IP Address: Select your system’s IP or leave as `All Unassigned`
- Port: `21`
- SSL: `No SSL`
- Click **Next**

### Authentication and Authorization:
- Authentication: ✅ Basic
- Authorization:
  - Select: **Specified users**
  - Enter: `ftpuser` (or your Windows username)
  - Permissions: ✅ Read and ✅ Write
- Click **Finish**

---

## 👤 Step 3: Create a Local FTP User

1. Open **PowerShell (as Administrator)**
2. Run the following command:

```powershell
net user ftpuser 123456 /add
