# Security Operations Center 2

---

## 1. SOC Operations
- [ ] **1.1** Respond to a suspicious login alert by managing the incident using a basic case-recording method (e.g., shared spreadsheet or TheHive).  
- [ ] **1.2** Document investigator details: who investigated the alert.  
- [ ] **1.3** Record actions taken during investigation.  
- [ ] **1.4** Document the final outcome of the investigation.  
- [ ] **1.5** Submit a brief incident report including:  
  - [ ] **1.5a** Screenshot of the alert  
  - [ ] **1.5b** Timeline of events  
  - [ ] **1.5c** Resolution notes  

---

## 2. SIEM Setup & Alerts
- [ ] **2.1** Configure a free SIEM (e.g., Wazuh or Elastic Stack – open-source tier) to ingest logs from a system.  
- [ ] **2.2** Enable a rule that detects repeated failed logins.  
- [ ] **2.3** Provide screenshot evidence of the alert triggered in the SIEM dashboard.  
- [ ] **2.4** Document the following in your report:  
  - [ ] **2.4a** Setup process  
  - [ ] **2.4b** Rule configuration  
  - [ ] **2.4c** Evidence of triggered alert  

---

## 3. Threat Hunting & Intelligence
- [ ] **3.1** Perform a simple search in collected logs for unusual activity (e.g., odd IP address, suspicious command).  
- [ ] **3.2** If a suspicious indicator is found, verify it using a free threat intelligence site (e.g., VirusTotal).  
- [ ] **3.3** Document the following in your incident report:  
  - [ ] **3.3a** Search queries used  
  - [ ] **3.3b** Indicator discovered  
  - [ ] **3.3c** Screenshot or summary of verification  

---

## 4. Automation & Orchestration
- [ ] **4.1** Implement a basic automated response using a Python script or a free workflow tool (e.g., Shuffle).  
- [ ] **4.2** Automate at least one of the following tasks:  
  - [ ] **4.2a** Sending an email upon alert trigger  
  - [ ] **4.2b** Adding a note to the incident record  
- [ ] **4.3** Provide evidence of automation in action (e.g., screenshot, log output).  
- [ ] **4.4** Document your workflow clearly in your report.  
