Implement and Explain Advanced Cybersecurity Defense Strategies

The project must demonstrate the application of Zero Trust Architecture by showing how access controls were enforced across at least 2 security layers. An explanation of Defense in Depth must be included, with at least 3 layers of defense clearly described and applied to a system architecture. Supply Chain Security must be demonstrated through documentation of 1 example where supply chain risks were identified and mitigated. The project must also describe 1 advanced security model, such as the Bell-LaPadula model or Clark-Wilson model, with an explanation of how it was applied to secure a system.

Implement Incident Response and Handling

The project must include an Incident Response Plan (IRP) that outlines a structured 5-step IR framework: preparation, identification, containment, eradication, and recovery. Digital forensics basics must be demonstrated by documenting the use of at least 1 forensic tool for data collection. Evidence collection and documentation must be supported by at least 2 forms of evidence (e.g., log files, screenshots) with proper chain of custody documentation. Incident triage and prioritization must be shown by categorizing 3 types of incidents based on severity and business impact. Post-incident analysis must be included, summarizing the incident outcome and describing at least 2 lessons learned.

Demonstrate SOC (Security Operations Center) Fundamentals

The project must explain SOC functions and operations by identifying at least 3 primary SOC roles and their responsibilities. Monitoring fundamentals must be demonstrated by configuring 1 monitoring tool and showcasing at least 2 types of network activity being monitored. Alert management must be shown with evidence of how 2 different security alerts were generated, investigated, and resolved. Basic threat detection must be demonstrated with an analysis of at least 1 identified threat and how it was detected using SOC tools.

Develop and Implement Security Policies and Governance

The project must include a policy development framework by providing a written security policy document covering at least 3 areas: access control, data protection, and system use policies. Governance structure must be demonstrated by outlining roles and responsibilities for enforcing the policy. Compliance requirements must be addressed with references to at least 1 security standard (e.g., ISO 27001, NIST CSF). Policy implementation must be demonstrated with evidence of how the security policies were communicated and enforced in a system.

Produce Effective Security Documentation

The project must include technical writing with a clearly written cybersecurity procedure document covering at least 1 security control implementation. Process documentation must be demonstrated with a documented step-by-step guide for at least 1 security task such as patch management or incident reporting. Security playbooks must be included, outlining at least 2 incident response scenarios with steps to follow. Knowledge base management must be demonstrated with a structured document repository containing at least 3 categorized resources for cybersecurity reference.

# Cybersecurity Basics 2

---

### 1. Implement and Explain Advanced Cybersecurity Defense Strategies  
- [ ] **1.1** Demonstrate **Zero Trust Architecture** by enforcing access controls across at least 2 security layers  
- [ ] **1.2** Explain and apply **Defense in Depth** with at least 3 layers of defense in a system architecture  
- [ ] **1.3** Demonstrate **Supply Chain Security** by documenting 1 example of risk identification and mitigation  
- [ ] **1.4** Describe and apply 1 **advanced security model**:  
  - [ ] **1.4a** Bell-LaPadula model  
  - [ ] **1.4b** Clark-Wilson model  
  - [ ] **1.4c** Other advanced security model (explanation + application to a system)  

---

### 1. Implement and Explain Advanced Cybersecurity Defense Strategies  

#### 1.1 Zero Trust Architecture (ZTA)  
- **Definition:** A security framework that requires continuous verification of users, devices, and applications, regardless of location within or outside the network perimeter.  
- **Implementation Example:**  
  1. **Identity Layer:** Enforce Multi-Factor Authentication (MFA) for all VPN logins.  
  2. **Network Layer:** Require device posture validation (up-to-date patches, endpoint protection enabled) before granting access to internal resources.  
- **Result:** Access is not granted based on network location alone, but on verified trust at multiple layers.  


```mermaid
flowchart TD
    A[User Requests Access] --> B{Multi-Factor Authentication}
    B -->|Success| C[Device Posture Validation]
    B -->|Failure| X[Access Denied]
    C --> D{Device Compliant?}
    D -->|Yes| E[Identity Verification]
    D -->|No| Y[Remediate Device]
    Y --> C
    E --> F{Policy Check}
    F -->|Authorized| G[Grant Limited Access]
    F -->|Unauthorized| Z[Access Denied]
    G --> H[Continuous Monitoring]
    H --> I{Anomaly Detected?}
    I -->|No| J[Maintain Access]
    I -->|Yes| K[Re-authenticate/Restrict]
    K --> B
    J --> H

    style A fill:#e1f5fe
    style G fill:#c8e6c9
    style X fill:#ffcdd2
    style Y fill:#fff3e0
    style Z fill:#ffcdd2
```

---

#### 1.2 Defense in Depth (DiD)  
- **Definition:** A layered security approach where multiple security controls are implemented across the IT environment to reduce risk.  
- **Example System Architecture with 3 Layers:**  
  1. **Perimeter Layer:** Firewall + Intrusion Detection System (IDS).  
  2. **Host Layer:** Endpoint Detection & Response (EDR) with real-time monitoring.  
  3. **Application/Data Layer:** Database encryption and role-based access control (RBAC).  
- **Result:** Even if one defense fails (e.g., firewall bypass), additional layers continue to protect assets. 

---

```mermaid
flowchart TB
    subgraph "Perimeter Layer"
        A[Firewall] 
        B[Intrusion Detection System]
        C[VPN Gateway]
    end
    
    subgraph "Network Layer"
        D[Network Segmentation]
        E[Load Balancer]
        F[WAF - Web Application Firewall]
    end
    
    subgraph "Host Layer"
        G[Endpoint Detection & Response]
        H[Anti-malware]
        I[Host-based Firewall]
    end
    
    subgraph "Application Layer"
        J[Input Validation]
        K[Authentication & Authorization]
        L[Session Management]
    end
    
    subgraph "Data Layer"
        M[Database Encryption]
        N[Role-Based Access Control]
        O[Data Loss Prevention]
    end
    
    P[External Threat] --> A
    A --> D
    D --> G
    G --> J
    J --> M
    
    style P fill:#ffcdd2
    style M fill:#c8e6c9
    style A fill:#fff3e0
    style D fill:#fff3e0
    style G fill:#fff3e0
    style J fill:#fff3e0
```

---

#### 1.3 Supply Chain Security  
- **Definition:** Protecting systems from vulnerabilities or compromises introduced via third-party vendors, software, or hardware.  
- **Example of Risk Identification and Mitigation:**  
  - **Risk:** Open-source library used in a web app contains a known vulnerability (e.g., Log4j exploit).  
  - **Mitigation:**  
    - Perform regular dependency scanning (e.g., with OWASP Dependency-Check, GitHub Dependabot).  
    - Apply vendor patches and update vulnerable components immediately.  
    - Implement Software Bill of Materials (SBOM) tracking.  
- **Result:** Ensures that third-party risks are detected early and mitigated before exploitation.  

---

```mermaid
flowchart TD
    A[Third-Party Component] --> B{Vulnerability Scanning}
    B -->|Clean| C[Integration Approved]
    B -->|Vulnerable| D[Risk Assessment]
    
    D --> E{Risk Level}
    E -->|Low| F[Accept with Monitoring]
    E -->|Medium| G[Apply Patches/Updates]
    E -->|High| H[Block/Replace Component]
    
    C --> I[Software Bill of Materials]
    F --> I
    G --> I
    
    I --> J[Continuous Monitoring]
    J --> K{New Vulnerability?}
    K -->|No| L[Maintain Operation]
    K -->|Yes| M[Alert & Reassess]
    
    M --> D
    L --> J
    
    subgraph "Tools & Processes"
        N[OWASP Dependency-Check]
        O[GitHub Dependabot]
        P[SBOM Tracking]
        Q[CVE Database]
    end
    
    B -.-> N
    B -.-> O
    I -.-> P
    K -.-> Q
    
    style A fill:#e1f5fe
    style H fill:#ffcdd2
    style C fill:#c8e6c9
    style I fill:#fff3e0
```

---

#### 1.4 Advanced Security Models  

##### 1.4a Bell-LaPadula Model (Confidentiality-Focused)  
- **Definition:** Enforces data confidentiality using security clearance levels.  
- **Application:** Used in military systems where users with "Secret" clearance cannot access "Top Secret" data, but can write upwards.  
- **Rule:** *"No Read Up, No Write Down"*.  

---
```mermaid
graph TB
    subgraph "Bell-LaPadula Model (Confidentiality)"
        A1[Top Secret] 
        A2[Secret]
        A3[Confidential]
        A4[Unclassified]
        
        A1 -.->|No Read Down| A2
        A2 -.->|No Read Down| A3
        A3 -.->|No Read Down| A4
        
        A4 -->|Can Write Up| A3
        A3 -->|Can Write Up| A2
        A2 -->|Can Write Up| A1
    end
    
    style A1 fill:#ffcdd2
    style A4 fill:#c8e6c9
```
---

##### 1.4b Clark-Wilson Model (Integrity-Focused)  
- **Definition:** Ensures system integrity by enforcing separation of duties and well-formed transactions.  
- **Application:** Banking system enforces dual control — one employee enters a transaction, another must approve it.  
- **Rule:** Prevents unauthorized modifications and enforces integrity constraints.  

---
```mermaid
graph TB
    subgraph "Clark-Wilson Model (Integrity)"
    
        B1[User] --> B2[Transformation Procedure]
        B2 --> B3[Constrained Data Item]
        B4[Integrity Verification] --> B3
        B5[Separation of Duties] --> B2
        B6[Well-Formed Transaction] --> B2
    end

    style B3 fill:#e8f5e8
    style B6 fill:#e8f5e8
```

---

##### 1.4c Other Advanced Security Model – Brewer-Nash (Chinese Wall Model)  
- **Definition:** Prevents conflicts of interest by restricting access to data once a user accesses competing company data.  
- **Application:** In a consulting firm, an analyst working on "Company A" cannot access "Company B" financial data.  
- **Rule:** Protects against insider conflict-of-interest breaches.  

---

```mermaid
graph TB
    subgraph "Brewer-Nash Model (Chinese Wall)"
        C1[Analyst] --> C2{Access Request}
        C2 -->|Company A Data| C3[Grant Access]
        C2 -->|Company B Data| C4{Conflict Check}
        C4 -->|No Conflict| C5[Grant Access]
        C4 -->|Conflict Detected| C6[Deny Access]
        C3 --> C7[Wall Created]
        C7 -.->|Blocks| C6
    end

    style C6 fill:#ffcdd2
    style C7 fill:#fff3e0    
```
---

### 2. Implement Incident Response and Handling  
- [ ] **2.1** Create an **Incident Response Plan (IRP)** covering the 5-step framework:  
  - [ ] **2.1a** Preparation  
  - [ ] **2.1b** Identification  
  - [ ] **2.1c** Containment  
  - [ ] **2.1d** Eradication  
  - [ ] **2.1e** Recovery  
- [ ] **2.2** Demonstrate **digital forensics basics** with at least 1 forensic tool for data collection  
- [ ] **2.3** Collect and document evidence using at least 2 forms of evidence:  
  - [ ] **2.3a** Log files  
  - [ ] **2.3b** Screenshots  
  - [ ] **2.3c** Other evidence type  
- [ ] **2.4** Maintain proper **chain of custody documentation**  
- [ ] **2.5** Demonstrate **incident triage and prioritization** by categorizing 3 types of incidents based on severity and business impact  
- [ ] **2.6** Perform **post-incident analysis**:  
  - [ ] **2.6a** Summarize incident outcome  
  - [ ] **2.6b** Describe at least 2 lessons learned  

---

### 3. Demonstrate SOC (Security Operations Center) Fundamentals  
- [ ] **3.1** Explain **SOC functions and operations** by identifying at least 3 primary SOC roles and responsibilities  
- [ ] **3.2** Demonstrate **monitoring fundamentals**:  
  - [ ] **3.2a** Configure 1 monitoring tool  
  - [ ] **3.2b** Showcase at least 2 types of network activity being monitored  
- [ ] **3.3** Show **alert management** with evidence of how 2 different alerts were:  
  - [ ] **3.3a** Generated  
  - [ ] **3.3b** Investigated  
  - [ ] **3.3c** Resolved  
- [ ] **3.4** Demonstrate **basic threat detection** by analyzing at least 1 identified threat and showing how it was detected using SOC tools  

---

### 4. Develop and Implement Security Policies and Governance  
- [ ] **4.1** Provide a written **security policy document** covering at least 3 areas:  
  - [ ] **4.1a** Access control  
  - [ ] **4.1b** Data protection  
  - [ ] **4.1c** System use policies  
- [ ] **4.2** Demonstrate **governance structure** by outlining roles and responsibilities for enforcing the policy  
- [ ] **4.3** Address **compliance requirements** with references to at least 1 security standard (ISO 27001, NIST CSF, etc.)  
- [ ] **4.4** Demonstrate **policy implementation** with evidence of how policies were communicated and enforced in a system  

---

### 5. Produce Effective Security Documentation  
- [ ] **5.1** Create a **cybersecurity procedure document** covering at least 1 security control implementation  
- [ ] **5.2** Demonstrate **process documentation** with a step-by-step guide for at least 1 security task:  
  - [ ] **5.2a** Patch management  
  - [ ] **5.2b** Incident reporting  
  - [ ] **5.2c** Other task  
- [ ] **5.3** Include **security playbooks** outlining at least 2 incident response scenarios with steps to follow  
- [ ] **5.4** Demonstrate **knowledge base management** with a structured repository containing at least 3 categorized cybersecurity resources  
