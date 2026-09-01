# Ernest Baker<br>DevSecOps Engineer | U.S. Army Veteran

<div align="center">


[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ernest%20Baker-blue?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ernest-baker/)
[![GitHub followers](https://img.shields.io/github/followers/crow50?label=Follow%20Me%20on%20GitHub&style=social)](https://github.com/crow50)

</div>

---

<div align="center">

| DevSecOps | Automation | CI/CD |
|:-----------:|:------------:|:-------:|
| [![Gitleaks Scan](https://github.com/crow50/ernest-portfolio/actions/workflows/gitleaks-scanning.yml/badge.svg)](https://github.com/crow50/ernest-portfolio/actions/workflows/gitleaks-scanning.yml) | [![Dependabot Updates](https://github.com/crow50/ernest-portfolio/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/crow50/ernest-portfolio/actions/workflows/dependabot/dependabot-updates) | [![Cloudflare Pages](https://img.shields.io/badge/Cloudflare-Pages-F38020?logo=cloudflare&logoColor=white)](https://ernestbaker.me) |
| [![Trivy Container Scan](https://github.com/crow50/ernest-portfolio/actions/workflows/trivy-scanning.yaml/badge.svg)](https://github.com/crow50/ernest-portfolio/actions/workflows/trivy-scanning.yaml) | [![Bundle Audit](https://github.com/crow50/ernest-portfolio/actions/workflows/bundle-audit.yml/badge.svg)](https://github.com/crow50/ernest-portfolio/actions/workflows/bundle-audit.yml) | [![Docker Build](https://img.shields.io/github/actions/workflow/status/crow50/ernest-portfolio/build-and-push-container.yml?label=Docker%20Build&logo=docker)](https://github.com/crow50/ernest-portfolio/actions/workflows/build-and-push-container.yml) |

</div>

---

## 👋 [Welcome to my Portfolio](https://ernestbaker.me)

I'm Ernest, a **Senior Systems Analyst** transitioning into **DevSecOps Engineering** with 10+ years in systems analysis, administration, and automation. I build automated infrastructure and CI/CD pipelines with security built in from the start: secrets scanning, container hardening, and software supply-chain analysis. This repo powers my portfolio site and showcases projects demonstrating **automation, CI/CD workflows, and system reliability**.

---

## 🛠️ Skills & Tools

* **DevSecOps & CI/CD:** Git, GitHub, GitHub Actions, GitHub Advanced Security, Gitleaks, Trivy, Syft, Grype, Pre-commit, SBOM Generation, CVE/CVSS Vulnerability Analysis, Applied ML for Security Scoring
* **Systems Engineering & Governance:** IT Governance, Infrastructure & Network Design, Project Management, Requirements Gathering, UAT, Digital Transformation
* **Automation & Programming:** Python, Bash, C++, Java, SQL, YAML, Markdown, HTML
* **Platforms, Virtualization & Cloud:** Windows Server, Linux, VMware, Proxmox, Docker, Kubernetes (k3s), Digital Ocean, nginx, vsftpd
* **Networking & Security Tools:** VLANs, Subnetting, VPNs, Load Balancing, Multi-Gigabit Networking, iSCSI, Ethernet, Cellular, TCP/IP, nmap, Wireshark, Hardware MFA (YubiKey)
* **Infrastructure Automation:** Traefik, n8n, Pi-hole
* **Database Management:** SQL Server, Oracle, MySQL, PostgreSQL
* **Tools & Applications:** Itron FDM, Fixed Network 100, OpenWay, SSMS, Oracle Billing & MDM, Cherwell

---

## 🏗️ Projects

### **Container Vulnerability Scanning with Trivy**

* **Objective:** Scan container images for OS package, dependency, and secrets vulnerabilities.
* **What:** Used Trivy to scan a container image and automated the scan in a GitHub Actions pipeline, documenting the full workflow from a vulnerable base image through scan results and remediation.
* **Repo:** [trivy-container-security](https://github.com/crow50/trivy-container-security)

### **Supply Chain Security with SBOM**

* **Objective:** Demonstrate end-to-end software supply-chain vulnerability management.
* **What:** Generated an SBOM with Syft, scanned it with Grype, triaged 47 initial findings down to the one with an available fix, remediated it, and rebuilt/rescanned to confirm.
* **Repo:** [supply-chain-security-with-sbom](https://github.com/crow50/supply-chain-security-with-sbom)

### **Predicting CVSS Vulnerability Severity with Machine Learning**

* **Objective:** Predict CVSS base severity from attack characteristics and real-world exploit signals, for a Big Data Mining and Analytics course.
* **What:** Trained a Random Forest Regression model on ~156,000 NVD vulnerability records (CVE, CISA KEV, EPSS data). Achieved an R² of 0.986, identified integrity impact and network attack vectors as the strongest predictors, and caught/corrected a data-leakage bug in an earlier iteration.
* **Course:** Big Data Mining and Analytics (CINF 401/8756), Stetson University

### **Capture-the-Flag Infrastructure Setup (NJ3CT)**

* **Objective:** Build and harden infrastructure for a team CTF exercise.
* **What:** Provisioned a DigitalOcean VM, hardened SSH, stood up nginx and vsftpd, and built deliberately vulnerable services (anonymous FTP, path-traversal targets) for teammates to practice enumeration and exploitation against.

### **Secrets Scanning in Git Repositories**

* **Objective:** Demonstrate detection and prevention of secrets leakage using local and CI/CD tools.
* **What:** Integrated Gitleaks into GitHub Actions to scan commits and PRs, added pre-commit hooks for local protection, and showcased GitHub Advanced Security push protection. Originated as an in-class CI/CD security demo for Introduction to Cybersecurity. Demo includes fake secrets, pipeline failure, remediation, and history cleanup with git-filter-repo.
* **Repo:** [Gitleaks Secret Scanning](https://github.com/crow50/Gitleaks-Secret-Scanning)

### **Portfolio CI/CD Pipeline**

* **Objective:** Build a personal portfolio site with automated deployments using GitHub Actions + Cloudflare.
* **What:** GitOps workflow basics, static site hosting, version control, and deployment automation.
* **Repo:** [Portfolio Source](https://github.com/crow50/ernest-portfolio)

### **DOE Grant Data Extraction Script**

* **Objective:** Execute and maintain Python scripts to generate datasets for DOE Grid Modernization grant reporting.
* **What:** Scripting fundamentals, data extraction, and operational support for compliance workflows.
* **Repo:** [DOE Script](https://github.com/crow50/ernest-portfolio/blob/main/previous-experience/duquesne-light-company/odms_data_extraction.py)

### **Open Source Guestbook Contribution**

* **Objective:** Open-source collaboration learning GitHub forking, branching, and PR submission workflow.
* **What:** Basic open-source contribution practices, collaborative version control skills.
* **Merged PR:** [Guestbook PR](https://github.com/OpenSource-Communities/guestbook/pull/705)

### **CloudRF API Clients - Python 3 Migration**

* **Objective:** Add compatibility for CloudRF API clients using Python 3 while preserving Python 2 usage.
* **What:** Refactored syntax/imports, split 2.x/3.x paths for compatibility; PR merged upstream.
* **Merged PR:** [CloudRF #2 - Python changes](https://github.com/Cloud-RF/CloudRF-API-clients/pull/2)

---

## 🌟 Professional Background

* **Duquesne Light Company - Software & Systems Analyst III**

  * Maintained Python scripts delivering DOE reporting datasets for \$19.7M grant compliance.
  * Converted legacy manual processes to Python-based workflows, reducing recurring work hours.

* **City of Cleveland - Systems Analyst**

  * Automated manual workflows saving 5+ hours per week in operational tasks.
  * Supported network infrastructure for Automated Meter Reading systems, maintaining 98% uptime.

* **Itron - Field Engineer & QA**

  * Performed field testing and QA for utility data collection systems.
  * Ensured operational reliability for deployed hardware/software systems.

---

## 🎓 Education & Training

* **Stetson University:** B.S. Cybersecurity (in progress)
* **Relevant Coursework:** Applied Cryptography, Big Data Mining & Analytics, Introduction to Cybersecurity
* **Certifications & Courses:** Service Planning & Architecture, Project Risk Management, Python Programming

---
