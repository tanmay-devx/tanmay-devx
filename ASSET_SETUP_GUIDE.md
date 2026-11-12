# Asset & External Services Setup Guide

This guide provides technical specifications, operational status, and deployment instructions for all external visual services, animated badges, and GitHub Actions workflows integrated into Tanmay Agrawal's GitHub profile (`tanmay-devx`).

---

## 1. Inventory of External Visual & SVG Services

| Service / Tool | Purpose in Profile | Source URL & Endpoint | Availability & Resilience Status |
| :--- | :--- | :--- | :--- |
| **Readme Typing SVG** | Dynamic animated header typing title | `https://readme-typing-svg.demolab.com` | Verified 200 OK. Hosted on high-availability demolab edge. |
| **SkillIcons.dev** | High-definition dark-mode tech stack icons | `https://skillicons.dev/icons?i=...` | Verified 200 OK. Cached globally via Cloudflare CDN. |
| **GitHub Readme Streak Stats** | Live streak and contribution consistency tracker | `https://streak-stats.demolab.com/?user=tanmay-devx` | Verified 200 OK. Official demolab production deployment. |
| **GitHub Readme Stats & Top Langs** | Aggregated repository stars, commits, and language ratios | `https://github-readme-stats-eight-theta.vercel.app/api?username=tanmay-devx` | Verified 200 OK. Configured with `#0D1117` GitHub dark theme matching. |
| **LeetCode Card (JacobLin)** | Real-time LeetCode problem solving metrics | `https://leetcard.jacoblin.cool/tanmay041?theme=dark` | Verified 200 OK. Dark theme with problem distribution. |
| **Codeforces Stats Card** | Live contest rating and rank visualization | `https://codeforces-readme-stats.vercel.app/api/card?username=tanmay0412` | Verified 200 OK. Tokyonight theme with dark background. |
| **Shields.io** | Clean action buttons and contact links | `https://img.shields.io/badge/...` | High-reliability global badge CDN. |
| **Platane/snk** | Dynamic contribution grid snake eating commit tiles | Automated GitHub Action committing to `output` branch | Self-hosted inside repository; zero external API dependency. |

---

## 2. GitHub Contribution Snake Animation Setup

The contribution snake animation is powered by [`Platane/snk`](https://github.com/Platane/snk), generating animated SVGs based on your real GitHub contribution graph.

### Step 1: Workflow Configuration
The workflow configuration is committed at:
```
.github/workflows/snake.yml
```

### Step 2: Enable Workflow Write Permissions
GitHub Actions needs permission to push the generated SVGs to your repository's `output` branch.

1. Navigate to your repository on GitHub: `https://github.com/tanmay-devx/tanmay-devx`
2. Click **Settings** (top navigation bar of the repository).
3. On the left sidebar, click **Actions** ➔ **General**.
4. Scroll down to **Workflow permissions**.
5. Select **"Read and write permissions"**.
6. Check **"Allow GitHub Actions to create and approve pull requests"**.
7. Click **Save**.

### Step 3: Trigger the First Run Manually
1. Navigate to the **Actions** tab on `tanmay-devx/tanmay-devx`.
2. In the left sidebar, click **"Generate Contribution Snake Animation"**.
3. Click the **Run workflow** dropdown on the right side and click the green **Run workflow** button.
4. Once completed (typically ~30 seconds), a new orphan branch named `output` will be created automatically containing:
   - `github-contribution-grid-snake.svg`
   - `github-contribution-grid-snake-dark.svg`
5. Your profile README is already pre-configured with `<picture>` tags to render these SVGs automatically with light/dark mode adaptation.

---

## 3. GitHub Readme Stats Resilience & Fallback

### Why Rate-Limiting Occurs on Upstream Instances
The upstream public URL `https://github-readme-stats.vercel.app` handles millions of global requests daily and periodically encounters GitHub API rate limits (returning `HTTP Error 503: Service Unavailable`).

### Active Mirror Configuration (Default)
Your profile is configured to use an active edge mirror (`github-readme-stats-eight-theta.vercel.app`) styled with the cohesive `#0D1117` GitHub dark theme.

### Optional: Deploy Your Own 1-Click Vercel Instance (100% Uptime Guarantee)
To run your own private instance with your personal GitHub rate limit:
1. Fork the official repository: [anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats).
2. Create a free account at [Vercel](https://vercel.com) and click **"Add New Project"**.
3. Select your forked `github-readme-stats` repository.
4. Generate a classic GitHub Personal Access Token (PAT) with `repo` scope at `github.com/settings/tokens`.
5. In Vercel environment variables, set:
   `PAT_1 = <YOUR_GITHUB_TOKEN>`
6. Click **Deploy**.
7. Replace `github-readme-stats-eight-theta.vercel.app` in `README.md` with your Vercel URL.

---

## 4. GitHub Profile Metadata Recommendation

To maximize recruiter discoverability on GitHub, configure the repository metadata on [github.com/tanmay-devx/tanmay-devx](https://github.com/tanmay-devx/tanmay-devx):

- **About Description:**
  `Full-Stack Developer & Software Engineer | Backend Engineering, Distributed Systems & Cloud Infrastructure`
- **Website URL:**
  `https://github.com/tanmay-devx/portfolio`
- **Topics (Tags):**
  `full-stack`, `backend`, `distributed-systems`, `system-design`, `nestjs`, `rabbitmq`, `podman`, `webrtc`, `cryptography`, `terraform`, `aws`
