# Rule Sets

### FTP Server Checks

``` xml
<group name="ftp,windows,">
  <rule id="100120" level="10">
    <match>530 Login incorrect</match>
    <description>FTP login failed on Windows (FileZilla)</description>
  </rule>

  <rule id="100121" level="5">
    <match>230 Login successful</match>
    <description>FTP login successful on Windows (FileZilla)</description>
  </rule>
</group>

```

This rule set checks for FTP server requests wether logins are successful or failed. This ruleset is great for testing brute force techniques which are being applied on a server and will log each brute force attempt as failed or successful.

Make sure that the FileZilla server log is being properly accessed by specifiying in the wazuh agent configuration file `C:\Program Files (x86)\ossec-agent\ossec.conf`

Place the <localfile> tag inbetween the <ossec_config> tag and add the <log_format> and <location> of the filezilla server log in xml format.

```xml

<ossec_config>

...

<!-- Log analysis -->

  <localfile>
    <log_format>syslog</log_format>
    <location>C:\Program Files\FileZilla Server\Logs\filezilla-server.log</location>    
  </localfile>

...

</ossec_config>
```

Note: You might need to add full control permissions to `ossec.conf` and `filezilla-server.log` as in windows they cannot be read or accessed by default. Right click and add the permission in the file properties security tab.

### Ransomeware

``` xml

<group name="windows,sysmon,ransomware,">

  <!-- T1490 Inhibit System Recovery: vssadmin/shadow copy tampering -->
  <rule id="110201" level="12">
    <if_group>sysmon_event1</if_group> <!-- Process Create -->
    <field name="win.eventdata.Image">(?i)\\vssadmin\.exe$</field>
    <field name="win.eventdata.CommandLine">(?i)\b(delete\s+shadows|shadowstorage)\b</field>
    <description>Potential ransomware: vssadmin used to delete/modify shadow copies</description>
    <mitre><id>T1490</id><tactic>Impact</tactic></mitre>
  </rule>

  <rule id="110202" level="12">
    <if_group>sysmon_event1</if_group>
    <field name="win.eventdata.Image">(?i)\\wbadmin\.exe$</field>
    <field name="win.eventdata.CommandLine">(?i)\bdelete\s+(systemstatebackup|catalog)\b</field>
    <description>Potential ransomware: wbadmin deleting backups/catalog</description>
    <mitre><id>T1490</id><tactic>Impact</tactic></mitre>
  </rule>

  <rule id="110203" level="10">
    <if_group>sysmon_event1</if_group>
    <field name="win.eventdata.Image">(?i)\\bcdedit\.exe$</field>
    <field name="win.eventdata.CommandLine">(?i)\b(recoveryenabled\s+No|bootstatuspolicy\s+ignoreallfailures)\b</field>
    <description>Potential ransomware: bcdedit changes that hinder recovery</description>
    <mitre><id>T1490</id><tactic>Impact</tactic></mitre>
  </rule>

  <rule id="110204" level="12">
    <if_group>sysmon_event1</if_group>
    <field name="win.eventdata.Image">(?i)\\wmic\.exe$</field>
    <field name="win.eventdata.CommandLine">(?i)\bshadowcopy\s+delete\b</field>
    <description>Potential ransomware: WMI used to delete shadow copies</description>
    <mitre><id>T1490</id><tactic>Impact</tactic></mitre>
  </rule>

  <!-- T1486 Data Encrypted for Impact: suspicious “encrypted” suffixes -->
  <!-- Single suspicious rename/create to an encryption-like extension -->
  <rule id="110210" level="6">
    <if_group>sysmon_event11</if_group> <!-- File Create -->
    <!-- target filename ends in common ransom suffixes -->
    <field name="win.eventdata.TargetFilename">(?i)\.(encrypted|enc|locked|crypt)$</field>
    <description>Suspicious file creation/rename: potential encryption suffix</description>
    <mitre><id>T1486</id><tactic>Impact</tactic></mitre>
  </rule>

  <!-- Burst: many such events in a short window (tune thresholds) -->
  <rule id="110211" level="12" frequency="30" timeframe="60">
    <if_matched_sid>110210</if_matched_sid>
    <same_source/>
    <description>Ransomware-like behavior: ≥30 suspicious renames/creates in 60s</description>
    <mitre><id>T1486</id><tactic>Impact</tactic></mitre>
  </rule>

  <!-- Ransom note creation -->
  <rule id="110220" level="10">
    <if_group>sysmon_event11</if_group> <!-- File Create -->
    <field name="win.eventdata.TargetFilename">(?i)(README|HOW_TO_DECRYPT|RECOVER_FILES).*\.(txt|html)$</field>
    <description>Potential ransomware: ransom note file created</description>
    <mitre><id>T1486</id><tactic>Impact</tactic></mitre>
  </rule>

</group>

```

General Applicability of the Rules

1. Shadow Copy or Backup Tampering (Inhibit System Recovery)

Rules like detecting:

- vssadmin.exe delete shadows
- wbadmin.exe delete catalog
- bcdedit.exe recoveryenabled No
- wmic shadowcopy delete

Note: These are well know ransomware techniques aimed at disabling Window's recovery features.


2. Mass File Renames with Encryption-Like Extensions

Rules for detecting bursts of filenames ending with .encrypted, .enc, .locked, etc., are also not specific to the dummy script. They catch a generic ransomware pattern: mass renaming/encrypting files with new extensions—all under sysmon file-create events


3. Ransom Note Creation

The detection for files like README_TO_DECRYPT.txt, HOW_TO_DECRYPT_FILES.txt, etc., is again a broader pattern. Many ransomware variants drop ransom notes with recognizable names—even if the file names differ slightly. You can adapt the regex to catch variants like README.HAes.txt

Summary: General vs. Script-Specific

| Component                | Script-Specific | General Ransomware Detection |
| ------------------------ | --------------- | ---------------------------- |
| Shadow copy tampering    | No              | Yes (common across threats)  |
| Burst rename detection   | No              | Yes (generic behavior)       |
| Ransom note detection    | No              | Yes (common files/drops)     |
| Script names/path checks | Yes (if added)  | No (optional tuning)         |
