# Final Technical Accuracy & Presentation Audit Report

**Repository:** [`tanmay-devx/tanmay-devx`](https://github.com/tanmay-devx/tanmay-devx)  
**Candidate:** Tanmay Agrawal  
**Audit Scope:** Final Accuracy, Presentation & Defensibility Audit  
**Date of Audit:** October 2026  

---

## 1. Itemized Correction & Verification Log

| # | Item / Check | Audit Finding & Action Taken | Verification Status |
| :--- | :--- | :--- | :--- |
| **1** | **Project Preview Assets** | Verified that all four referenced project preview images exist in `assets/projects/` and on the `main` branch: `coditorium-logo.png` (499KB), `nijisamvad-preview.png` (75KB), `dropx-preview.png` (487KB), and `planrova-preview.png` (148KB). | **Verified (HTTP 200 on main)** |
| **2** | **Stack Section Heading** | Replaced "Production & Implementation Stack" with **"Technologies Used in Projects"**, keeping it strictly separate from technologies currently being explored. | **Verified** |
| **3** | **RabbitMQ Delivery Mechanics** | Eliminated all "guaranteed delivery" language. Accurately described durable queue declarations (`{ durable: true }`), persistent message delivery (`{ persistent: true }`), and explicit manual consumer acknowledgments (`{ noAck: false }`) to mitigate message loss during worker interruptions. | **Verified in Codebase** |
| **4** | **Rootless Podman Framing** | Replaced absolute security claims with defensible risk-reduction framing: executing untrusted containers without root privileges to substantially reduce the host attack surface and mitigate root privilege escalation vectors. | **Verified** |
| **5** | **Removal of "Autonomous"** | Removed all occurrences of the word "Autonomous" from the Sanjeevni AI title, description, and limitations, repositioning it strictly as an **"AI-Assisted Patient Intake Kiosk"**. | **Verified (0 occurrences)** |
| **6** | **FastAPI Integration Boundary** | Removed `FastAPI` from Sanjeevni AI's own tech stack (`React 18`, `Three.js`, `Node.js Express`, `SQLite`, `Groq LLaMA 3.3`). Explicitly clarified that FastAPI powers the separate **Swasya AI** companion clinical command center. | **Verified** |
| **7** | **Planrova Offline Qualification** | Qualified that local timetable views, habit tracking, and Pomodoro focus timers function offline, while multi-device state synchronization (Cloud Firestore) and handwriting OCR (Groq Vision API) require an active internet connection. | **Verified** |
| **8** | **Android Alarm Constraints** | Corrected the Android alarm description to avoid implying that Doze restrictions and OEM battery policies can always be bypassed. Noted that exact alarms via `AlarmManager.setAlarmClock()` reduce timer suppression during idle states but remain bounded by OS-level `SCHEDULE_EXACT_ALARM` permissions and aggressive OEM power-saving policies. | **Verified** |
| **9** | **Resource-Management Principle** | Replaced generic "bounded streaming" language with accurate payload boundary and rate-limiting principles consistent with DropX's actual `express.raw()` 100MB ceiling. | **Verified** |
| **10** | **Competitive Programming & Cards** | Verified that all handles (LeetCode: `tanmay041`, Codeforces: `tanmay0412`, CodeChef: `tanmay041`, HackerRank: `tanmay041`) and live cards (`leetcard.jacoblin.cool`, `codeforces-readme-stats`) return HTTP 200 OK. | **Verified** |
| **11** | **Repository Metadata** | Documented exact About description, homepage, and topics for manual configuration on GitHub (since SSH keys lack administrative REST API permissions). | **Documented** |
| **12** | **Mermaid Diagram Syntax** | Validated both Diagram 1 (`flowchart TD`) and Diagram 2 (`sequenceDiagram`) against GitHub-flavored Markdown parsers with zero syntax warnings. | **Verified** |

---

## 2. Asset Resolution Audit

```
[Local Assets - assets/projects/]
✓ assets/projects/coditorium-logo.png   (499,082 bytes) -> HTTP 200 OK
✓ assets/projects/nijisamvad-preview.png (75,150 bytes)  -> HTTP 200 OK
✓ assets/projects/dropx-preview.png      (487,997 bytes) -> HTTP 200 OK
✓ assets/projects/planrova-preview.png   (148,150 bytes) -> HTTP 200 OK

[External Cards & SVG Badges]
✓ Typing SVG (readme-typing-svg.demolab.com)            -> HTTP 200 OK
✓ SkillIcons Grid (skillicons.dev)                      -> HTTP 200 OK
✓ GitHub Streak Card (streak-stats.demolab.com)         -> HTTP 200 OK
✓ GitHub Stats & Top Langs (github-readme-stats-eight)  -> HTTP 200 OK
✓ LeetCode Card (leetcard.jacoblin.cool)                -> HTTP 200 OK
✓ Codeforces Card (codeforces-readme-stats)             -> HTTP 200 OK
✓ Verified Credential Links (Certmetrics & Credly)      -> HTTP 200 OK
```

---

## 3. Explicit Remaining Limitations (Unverified / Staged Features)

To maintain absolute technical integrity, the following limitations are transparently documented in the profile:

1. **Coditorium:** Container cold-start invocation latency exists on each submission; warm container pre-forking or microVM virtualization (e.g. Firecracker) are identified future milestones.
2. **NijiSamvad:** Derives symmetric keys from a pre-shared room secret without an asymmetric Double Ratchet protocol (Signal Protocol); does not provide Perfect Forward Secrecy (PFS).
3. **DropX:** In-memory `express.raw()` buffering caps single-file uploads at 100MB rather than using backpressure-controlled streaming pipelines.
4. **Planrova:** Android alarms rely on `SCHEDULE_EXACT_ALARM` permissions and remain subject to aggressive OEM battery management overrides or user force-stops.
5. **Sanjeevni AI:** Speech recognition accuracy depends on clinic acoustic noise; designed strictly as a preliminary intake tool rather than a standalone diagnostic device.
6. **Terraform Multi-Env:** Deploys compute into default VPC subnets rather than provisioning custom multi-tier VPC topologies.
