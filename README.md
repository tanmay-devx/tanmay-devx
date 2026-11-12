<!-- =========================================================
     TANMAY AGRAWAL | GITHUB PROFILE README
     Software Engineer | Backend · Full-Stack · Cloud
     Developer Brand: TanmayDevX
     Repository: tanmay-devx/tanmay-devx
========================================================== -->

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=venom&height=200&text=Tanmay%20Agrawal&fontSize=48&fontColor=58A6FF&stroke=58A6FF&strokeWidth=1&animation=fadeIn&desc=Backend%20Systems%20%7C%20Distributed%20Architecture%20%7C%20Cloud%20Infrastructure&descSize=15&descAlignY=68&color=0:0D1117,100:161B22" width="100%" alt="Tanmay Agrawal Banner"/>

### Software Engineer | Backend · Full-Stack · Cloud
*Engineering scalable backend systems, distributed architectures, and reliable software products.*

<p align="center">
  <a href="https://tanmaydev.in" target="_blank">
    <img src="https://img.shields.io/badge/Portfolio-tanmaydev.in-58A6FF?style=flat-square&logo=vercel&logoColor=white" alt="Portfolio"/>
  </a>
  &nbsp;
  <a href="https://www.linkedin.com/in/tanmayagrawaldev" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-tanmayagrawaldev-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>
  &nbsp;
  <a href="mailto:tanmayagrawal.dev@gmail.com">
    <img src="https://img.shields.io/badge/Email-tanmayagrawal.dev%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"/>
  </a>
  &nbsp;
  <a href="https://leetcode.com/u/tanmay041/" target="_blank">
    <img src="https://img.shields.io/badge/LeetCode-tanmay041-FFA116?style=flat-square&logo=leetcode&logoColor=black" alt="LeetCode"/>
  </a>
  &nbsp;
  <a href="https://github.com/tanmay-devx">
    <img src="https://img.shields.io/badge/GitHub-tanmay--devx-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"/>
  </a>
</p>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=15&duration=2800&pause=1000&color=58A6FF&center=true&vCenter=true&width=700&lines=Building+asynchronous+execution+pipelines+with+RabbitMQ.;Sandboxing+untrusted+code+with+Rootless+Podman.;Architecting+defensive%2C+fault-tolerant+backend+services.;Building+cloud-native+applications+with+AWS+and+Terraform." alt="Typing SVG"/>

</div>

---

<div align="center">
  <img src="./assets/executive-summary.svg" width="100%" alt="01 Executive Summary"/>
</div>

---

<div align="center">
  <img src="./assets/header-projects.svg" width="100%" alt="02 Key Engineering Projects"/>
</div>

<table>
<tr>
<td width="50%" valign="top">

### 01. [CodVidya — Distributed Code Judge](https://github.com/tanmay-devx/Coditorium)
*Asynchronous execution engine and isolated grading platform.*

- Decoupled **RabbitMQ** judge queue handling concurrent submissions with manual ACKs.
- Sandboxed compilation and execution inside **Rootless Podman** containers with cgroup limits.
- **Turborepo** monorepo unifying API gateway, worker service, and shared Prisma schemas.

<details>
<summary>⚡ Architecture &amp; Pipeline Flow</summary>

`Client → NestJS API → RabbitMQ Queue → Rootless Podman Worker → PostgreSQL`

</details>

`NestJS` `TypeScript` `RabbitMQ` `Podman` `PostgreSQL` `Prisma`

<p>
  <a href="https://github.com/tanmay-devx/Coditorium" target="_blank">
    <img src="https://img.shields.io/badge/GitHub_Repo-181717?style=flat-square&logo=github&logoColor=white" alt="CodVidya GitHub Repo"/>
  </a>
</p>

</td>
<td width="50%" valign="top">

### 02. [NijiSamvad — Encrypted Real-Time Mesh](https://github.com/tanmay-devx/NijiSamvad)
*Zero-knowledge communication and peer-to-peer WebRTC platform.*

- Client-side **AES-256-GCM** encryption with **PBKDF2 (100k iterations)** key derivation.
- Stateless **Socket.IO** signaling server guaranteeing zero plaintext server exposure.
- Direct peer-to-peer audio/video streaming over resilient **WebRTC** mesh topology.

<details>
<summary>⚡ Architecture &amp; Pipeline Flow</summary>

`Web Crypto (AES-GCM) → Stateless Socket.IO Signaling ↔ P2P WebRTC Mesh`

</details>

`React` `Node.js` `Socket.IO` `WebRTC` `Web Crypto API`

<p>
  <a href="https://niji-samvad.vercel.app/" target="_blank">
    <img src="https://img.shields.io/badge/Live_Demo-238636?style=flat-square&logo=vercel&logoColor=white" alt="NijiSamvad Live Demo"/>
  </a>
  &nbsp;
  <a href="https://github.com/tanmay-devx/NijiSamvad" target="_blank">
    <img src="https://img.shields.io/badge/GitHub_Repo-181717?style=flat-square&logo=github&logoColor=white" alt="NijiSamvad GitHub Repo"/>
  </a>
</p>

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 03. [DropX — Ephemeral Data Exchange](https://github.com/tanmay-devx/dropx)
*Accountless temporary cross-device file sharing platform.*

- Automated **Redis** TTL session lifecycle and ephemeral room cleanup.
- Raw Express buffer streaming with enforced **100MB** bounded memory ceilings.
- End-to-end client-side payload encryption prior to local transit.

<details>
<summary>⚡ Architecture &amp; Pipeline Flow</summary>

`Encrypted Buffer → Express 100MB Stream → Socket.IO Room + Redis TTL`

</details>

`Node.js` `Express.js` `Redis` `Socket.IO` `React`

<p>
  <a href="https://dropxio.vercel.app/" target="_blank">
    <img src="https://img.shields.io/badge/Live_Demo-238636?style=flat-square&logo=vercel&logoColor=white" alt="DropX Live Demo"/>
  </a>
  &nbsp;
  <a href="https://github.com/tanmay-devx/dropx" target="_blank">
    <img src="https://img.shields.io/badge/GitHub_Repo-181717?style=flat-square&logo=github&logoColor=white" alt="DropX GitHub Repo"/>
  </a>
</p>

</td>
<td width="50%" valign="top">

### 04. [Planrova — Local-First Study System](https://github.com/tanmay-devx/planrova)
*Offline-capable academic productivity ecosystem.*

- Native Android Kotlin **AlarmManager** (`setAlarmClock()`) bridge bypassing OS Doze limits.
- Local-first offline persistence paired with selective **Cloud Firestore** sync.
- Multimodal **Groq Vision OCR** pipeline converting handwritten notes into structured tasks.

<details>
<summary>⚡ Architecture &amp; Pipeline Flow</summary>

`Local Store ⇄ Firestore Sync · Kotlin AlarmManager · Groq Vision OCR`

</details>

`React Native` `Expo` `Kotlin` `Firestore` `Groq API`

<p>
  <a href="https://planrova.vercel.app/" target="_blank">
    <img src="https://img.shields.io/badge/Live_Demo-238636?style=flat-square&logo=vercel&logoColor=white" alt="Planrova Live Demo"/>
  </a>
  &nbsp;
  <a href="https://github.com/tanmay-devx/planrova" target="_blank">
    <img src="https://img.shields.io/badge/GitHub_Repo-181717?style=flat-square&logo=github&logoColor=white" alt="Planrova GitHub Repo"/>
  </a>
</p>

</td>
</tr>
<tr>
<td colspan="2" valign="top">

### 05. [Sanjeevni AI — Multimodal Intake Kiosk](https://github.com/tanmay-devx/Sanjeevni-AI)
*AI-assisted clinic intake kiosk with 3D interaction and localized edge storage.*

- Edge-deployed **SQLite (`better-sqlite3`)** persisting patient intake logs during network dropouts.
- Interactive **Three.js** 3D anatomical avatar and 2D pain coordinate mapping.
- Multilingual voice intake (**Hindi / Hinglish / English**) synthesized via **Groq LLaMA** clinical summaries.

<details>
<summary>⚡ Architecture &amp; Pipeline Flow</summary>

`Voice + 3D Anatomy UI → Node.js Edge API → SQLite Offline Store + Groq LLaMA Triage`

</details>

`React 18` `Three.js` `Node.js` `SQLite` `Groq LLaMA`

<p>
  <a href="https://sanjeevniai.vercel.app/" target="_blank">
    <img src="https://img.shields.io/badge/Live_Demo-238636?style=flat-square&logo=vercel&logoColor=white" alt="Sanjeevni AI Live Demo"/>
  </a>
  &nbsp;
  <a href="https://github.com/tanmay-devx/Sanjeevni-AI" target="_blank">
    <img src="https://img.shields.io/badge/GitHub_Repo-181717?style=flat-square&logo=github&logoColor=white" alt="Sanjeevni AI GitHub Repo"/>
  </a>
</p>

</td>
</tr>
</table>

---

<div align="center">
  <img src="./assets/header-credentials.svg" width="100%" alt="03 Verified Credentials and Honors"/>
</div>

<table width="100%">
<tr>
  <td width="50%" valign="top">
    <a href="https://cp.certmetrics.com/amazon/en/public/verify/credential/fac9701f985443a3a5cad85982cc6520" target="_blank">
      <img src="./assets/cred-aws-cloud.svg" width="100%" alt="AWS Certified Cloud Practitioner"/>
    </a>
  </td>
  <td width="50%" valign="top">
    <a href="https://cp.certmetrics.com/amazon/en/public/verify/credential/4ad652a9eeee41e39af0dfabae4fcc8a" target="_blank">
      <img src="./assets/cred-aws-ai.svg" width="100%" alt="AWS Certified AI Practitioner"/>
    </a>
  </td>
</tr>
<tr>
  <td width="50%" valign="top">
    <img src="./assets/cred-innotech.svg" width="100%" alt="Innotech Hackathon — 1st Place Winner"/>
  </td>
  <td width="50%" valign="top">
    <img src="./assets/cred-nit.svg" width="100%" alt="NIT Jalandhar Hackathon — Top 10 Finalist"/>
  </td>
</tr>
<tr>
  <td colspan="2" valign="top">
    <a href="https://www.credly.com/earner/earned/badge/ff32dd8b-470b-4dd4-b7da-536382d97959" target="_blank">
      <img src="./assets/cred-aws-genai.svg" width="100%" alt="AWS Academy Graduate — Generative AI Foundations"/>
    </a>
  </td>
</tr>
</table>

---

## 🛠️ One Engineer, Every Layer of a Distributed System

<div align="center">
  <img src="./assets/distributed-system-layers.svg" width="100%" alt="One engineer, every layer of a distributed system"/>
</div>

---

## 🧮 Problem Solving & Engineering Activity

<div align="center">

<p align="center">
  <a href="https://leetcode.com/u/tanmay041/" target="_blank">
    <img src="https://img.shields.io/badge/LeetCode-tanmay041-FFA116?style=flat-square&logo=leetcode&logoColor=black" alt="LeetCode"/>
  </a>
  &nbsp;
  <a href="https://codeforces.com/profile/tanmay0412" target="_blank">
    <img src="https://img.shields.io/badge/Codeforces-tanmay0412-1F8ACB?style=flat-square&logo=codeforces&logoColor=white" alt="Codeforces"/>
  </a>
  &nbsp;
  <a href="https://www.codechef.com/users/tanmay041" target="_blank">
    <img src="https://img.shields.io/badge/CodeChef-tanmay041-5B4638?style=flat-square&logo=codechef&logoColor=white" alt="CodeChef"/>
  </a>
  &nbsp;
  <a href="https://www.hackerrank.com/tanmay041" target="_blank">
    <img src="https://img.shields.io/badge/HackerRank-tanmay041-2EC866?style=flat-square&logo=hackerrank&logoColor=white" alt="HackerRank"/>
  </a>
</p>

<table width="100%">
<tr>
  <td width="50%" align="center">
    <a href="https://leetcode.com/u/tanmay041/">
      <img src="https://raw.githubusercontent.com/tanmay-devx/tanmay-devx/stats-output/assets/card-leetcode.svg" width="100%" alt="LeetCode Stats"/>
    </a>
  </td>
  <td width="50%" align="center">
    <a href="https://codeforces.com/profile/tanmay0412">
      <img src="https://raw.githubusercontent.com/tanmay-devx/tanmay-devx/stats-output/assets/card-codeforces.svg" width="100%" alt="Codeforces Stats"/>
    </a>
  </td>
</tr>
<tr>
  <td width="50%" align="center">
    <a href="https://github.com/tanmay-devx">
      <img src="https://raw.githubusercontent.com/tanmay-devx/tanmay-devx/stats-output/assets/card-streak.svg" width="100%" alt="GitHub Streak"/>
    </a>
  </td>
  <td width="50%" align="center">
    <a href="https://github.com/tanmay-devx">
      <img src="https://raw.githubusercontent.com/tanmay-devx/tanmay-devx/stats-output/assets/card-github.svg" width="100%" alt="GitHub Stats"/>
    </a>
  </td>
</tr>
</table>

<div style="margin-top: 25px;">
  <img src="https://raw.githubusercontent.com/tanmay-devx/tanmay-devx/stats-output/assets/activity.svg" width="100%" alt="GitHub 3D Contribution Activity"/>
</div>

</div>

---

<div align="center">

<p align="center">
  <a href="https://tanmaydev.in"><b>Portfolio</b></a> &bull;
  <a href="https://www.linkedin.com/in/tanmayagrawaldev"><b>LinkedIn</b></a> &bull;
  <a href="mailto:tanmayagrawal.dev@gmail.com"><b>tanmayagrawal.dev@gmail.com</b></a> &bull;
  <a href="https://github.com/tanmay-devx"><b>GitHub</b></a>
</p>

```
$ echo "Good software engineering is understanding the trade-offs behind why it works."
```

</div>
