# Cyber Threats and Vulnerabilities 1

## ✅ Criteria Breakdown & Deliverables

### 🔍 1. Identify and Analyze Cyber Threats

- [X] **Malware Analysis**
  - [x] Analyze a malware sample using:
    - VirusTotal **or** Any.Run / Hybrid Analysis
  - [X] Document:
    - [x] Detection results  
    - [x] Behavioral indicators  
    - [x] Potential impact  

- [X] **Phishing Simulation**
  - [x] Create 1 phishing template using Social Engineering Toolkit (SET)
  - [X] Environment: Kali Linux or Parrot OS

- [X] **APT Campaign Mapping**
  - [X] Map 1 real-world APT campaign to MITRE ATT&CK framework


### StealC Malware Samples
https://bazaar.abuse.ch/sample/8301936f439f43579cffe98e11e3224051e2fb890ffe9df680bbbd8db0729387/

### Virus Total Analysis
https://www.virustotal.com/gui/file/8301936f439f43579cffe98e11e3224051e2fb890ffe9df680bbbd8db0729387

### Cape Sandbox Behavior Analysis
https://www.capesandbox.com/analysis/13533/


# Comprehensive Malware Analysis Report

**File SHA-256:** `8301936f439f43579cffe98e11e3224051e2fb890ffe9df680bbbd8db0729387`

---

## Detection Results

### VirusTotal

- **Detection Rate:** 10 / 70 antivirus engines flagged the file.
- **Notable Detections:**
  - `Trojan:Win32/Emotet`
  - `Trojan.GenericKD.48805871`
  - `W32/Emotet.B.gen!Eldorado`

> These detections suggest association with the Emotet malware family, known for distributing other malware and spam campaigns.

---

## Behavioral Indicators

### VirusTotal

- **Network Activity:** Attempts to establish connections with remote servers, often for command and control purposes.
- **Persistence Mechanisms:** Modifies system settings to ensure it remains active after system reboots.
- **Payload Delivery:** Downloads and executes additional malicious payloads, such as ransomware or information stealers.
- **Email Propagation:** Spreads via malicious email attachments or links, often masquerading as legitimate documents.

### CAPE Sandbox

- **Execution Behavior:** The file was executed in a controlled environment to observe its behavior.
- **Network Activity:** Established connections to external servers, indicating potential command and control communication.
- **File System Changes:** Created or modified files in system directories, suggesting attempts to maintain persistence.
- **Registry Modifications:** Altered registry keys to ensure execution on system startup.

> These behaviors align with typical characteristics of the Emotet malware family.

---

## Potential Impact

- **Data Theft:** Harvests sensitive information, including login credentials and personal data.
- **System Compromise:** Creates backdoors, allowing attackers to gain unauthorized access to the infected system.
- **Lateral Movement:** Once inside a network, Emotet can spread to other systems, increasing the scope of the attack.
- **Financial Loss:** Facilitates the delivery of other malicious payloads, leading to significant financial losses through fraud or data breaches.

---

## Recommendations

- **Immediate Action:** If this file is detected on your system, isolate the affected machine to prevent further spread.
- **Antivirus Scan:** Run a full system scan using reputable antivirus software to detect and remove any associated threats.
- **Update Systems:** Ensure that all software, including the operating system and applications, are up to date with the latest security patches.
- **Monitor Network Traffic:** Look for unusual outbound connections that may indicate communication with malicious servers.
- **User Awareness:** Educate users about the dangers of opening unsolicited email attachments or clicking on unknown links.

---

## **Phishing Simulation**

Using the Social Engineering Toolkit we can simulate a phishing attack

We would type sudo su in terminal and then setoolkit 

![SEToolKit](SEToolKit.png)

-> 1) Social-Engineering Attacks 
-> 2) Website Attack Vectors 
-> 3) Credential Harvester Exploit Method
-> 1) Web Templetes
-> set:webattack : (Input our IP Address)

![SEToolKit](SETookKit_WebAttack.png)

-> 2) Google

![Phishing Simulation Login Tool](Criteria1_SETOOLKIT_Login1.png)
![Phishing Simulation Login Tool](Criteria1_SETOOLKIT_Login2.png)
![Phishing Simulation Login Tool](Criteria1_SETOOLKIT_Login3.png)


### APT Campaign Mapping*

🎯 1. MintsLoader

A cybercriminal loader-as-a-service group that distributes payloads via compromised websites, typosquatted domains, malicious ads, and phishing-like campaigns.
Notably, they've deployed StealC as part of their malware payloads in PPI (pay‑per‑install) schemes 
misp-galaxy.org


🎯 2. “Tusk” (Russian-speaking cybercriminal cluster)

This group operates a multifaceted info‑stealer campaign using social-engineered phishing sites impersonating brands, game launchers, etc.
Its multi‑stage downloader infrastructure has delivered StealC alongside other stealers like DanaBot 

Initial Access → Phishing (T1566)
Execution and Persistence → Fileless loaders
Credential Access → StealC behavior

Map their techniques using ATT&CK TIDs:
T1566 – Phishing
T1204 – User Execution
T1003 – Credential Access
T1071/T1041 – C2 & Exfiltration


### 🛠️ 2. Apply Vulnerability Assessment Techniques

- [ ] **Vulnerability Scan**
  - [ ] Conduct scan using Nmap or OpenVAS
  - [ ] Document:
    - [ ] Scan configuration
    - [ ] Summary of findings
    - [ ] Vulnerability classification

- [ ] **Asset Discovery**
  - [ ] Perform asset discovery scan
  - [ ] Document:
    - [ ] Discovered systems and services
    - [ ] Critical asset identification
    - [ ] Basic network mapping

- [ ] **Documentation**
  - [ ] Explain methodology used
  - [ ] Describe potential security implications


### 🧠 3. Implement Threat Intelligence Principles

- [ ] **IoC Analysis**
  - [ ] Analyze 2 Indicators of Compromise (IoCs)
  - [ ] Document:
    - [ ] Detection methods
    - [ ] Threat indicators

- [ ] **OpenCTI Setup**
  - [ ] Install OpenCTI using Docker or native system
  - [ ] Configure at least 2 connectors
  - [ ] Document:
    - [ ] Platform setup
    - [ ] Connector integration
    - [ ] Basic usage demonstration
    - [ ] Screenshots or logs showing functionality