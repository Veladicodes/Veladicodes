<div align="center">

<img src="assets/banner.svg" alt="Adithya A, AI and ML engineer building real-time systems" width="100%" />

<br/>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-adithya--a--ml-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adithya-a-ml/)
[![Email](https://img.shields.io/badge/Email-10403adithya%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:10403adithya@gmail.com)

</div>

---

## 👋 About

I build machine-learning systems that run **live**, not just in notebooks: streaming pipelines, GPU inference, agent frameworks you can replay and audit, and dashboards that make the output usable. B.Tech student at VIT.

I report results the way they came out. The drone project below missed its own 0.88 mAP target, and the README says so.

## 🚀 Flagship projects

| | Project | What it is | Evidence |
|---|---|---|---|
| 🛡️ | [**RT-GIDS**](https://github.com/Veladicodes/Real-Time-GPU-Based-Intrusive-Detection-System) <br/> [![CI](https://github.com/Veladicodes/Real-Time-GPU-Based-Intrusive-Detection-System/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Veladicodes/Real-Time-GPU-Based-Intrusive-Detection-System/actions/workflows/ci.yml) [![release](https://img.shields.io/github/v/release/Veladicodes/Real-Time-GPU-Based-Intrusive-Detection-System)](https://github.com/Veladicodes/Real-Time-GPU-Based-Intrusive-Detection-System/releases) | Real-time network intrusion detection: XGBoost detector, FastAPI backend, Next.js dashboard with a 3D threat globe and SHAP explainability | 33 backend tests, TypeScript typecheck, production build and Docker build on every push |
| 🧭 | [**Deterministic Agent Orchestration**](https://github.com/Veladicodes/deterministic-agent-orchestration-mega-ai) <br/> [![Tests](https://github.com/Veladicodes/deterministic-agent-orchestration-mega-ai/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/Veladicodes/deterministic-agent-orchestration-mega-ai/actions/workflows/test.yml) [![release](https://img.shields.io/github/v/release/Veladicodes/deterministic-agent-orchestration-mega-ai)](https://github.com/Veladicodes/deterministic-agent-orchestration-mega-ai/releases) | Multi-agent pipeline (decomposer, retriever, critic, synthesizer) where every run produces a replayable trace and a SHA-256 execution hash | 123 tests; replay compare and validate endpoints; a React replay/diff view |
| 🔍 | [**Real-Time Fake Job Detector**](https://github.com/Veladicodes/Realtime-Fake-Job-Predictor) <br/> [![CI](https://github.com/Veladicodes/Realtime-Fake-Job-Predictor/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Veladicodes/Realtime-Fake-Job-Predictor/actions/workflows/ci.yml) [![release](https://img.shields.io/github/v/release/Veladicodes/Realtime-Fake-Job-Predictor)](https://github.com/Veladicodes/Realtime-Fake-Job-Predictor/releases) | Streaming pipeline that flags fraudulent job postings as they arrive: Kafka, Spark, PostgreSQL, FastAPI, Next.js | F1 **75.6%**, precision **82.3%**, recall **70.0%** on data with 4.8% fraud, with the threshold tuned on a validation split |
| 🔥 | [**Drone Fire Detection with RAG**](https://github.com/Veladicodes/cloud-rag-drone-fire-detection) <br/> [![CI](https://github.com/Veladicodes/cloud-rag-drone-fire-detection/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Veladicodes/cloud-rag-drone-fire-detection/actions/workflows/ci.yml) [![release](https://img.shields.io/github/v/release/Veladicodes/cloud-rag-drone-fire-detection)](https://github.com/Veladicodes/cloud-rag-drone-fire-detection/releases) | YOLO edge detection feeding a FAISS-backed RAG pipeline that drafts cited response plans for wildfire responders | mAP@0.5 **0.733** (the 0.88 target was not met), about 73 ms detect-to-plan with a mock LLM, about 198 messages/s across 10 simulated drones |

Also: [**RetailSense Lite**](https://github.com/Veladicodes/RetailSense_Lite), retail demand forecasting with a Prophet, XGBoost and LightGBM ensemble, anomaly detection and a Streamlit dashboard.

## 🧰 Tech stack

<div align="center">
  <img src="assets/stack.svg" alt="Python, TypeScript, React, Next.js, FastAPI, PyTorch, XGBoost, Kafka, Spark, Docker, PostgreSQL, Azure, Terraform" width="100%" />
</div>

## 🐍 Play snake with me

A real game, played by clicking. Each link opens a pre-filled issue: just press **Submit new issue**. A GitHub Actions workflow moves the snake one step, redraws the board and closes the issue, usually within a minute. Refresh this page to see your move. You need to be signed in to GitHub.

<div align="center">
  <img src="assets/snake-game.svg" alt="The current snake game board" width="640" />

| | | |
|:-:|:-:|:-:|
| | [⬆️ **Up**](https://github.com/Veladicodes/Veladicodes/issues/new?title=snake%7Cup&body=Just+click+%22Submit+new+issue%22.+You+do+not+need+to+change+anything.) | |
| [⬅️ **Left**](https://github.com/Veladicodes/Veladicodes/issues/new?title=snake%7Cleft&body=Just+click+%22Submit+new+issue%22.+You+do+not+need+to+change+anything.) | [⬇️ **Down**](https://github.com/Veladicodes/Veladicodes/issues/new?title=snake%7Cdown&body=Just+click+%22Submit+new+issue%22.+You+do+not+need+to+change+anything.) | [➡️ **Right**](https://github.com/Veladicodes/Veladicodes/issues/new?title=snake%7Cright&body=Just+click+%22Submit+new+issue%22.+You+do+not+need+to+change+anything.) |

[🔄 **New game**](https://github.com/Veladicodes/Veladicodes/issues/new?title=snake%7Cnew&body=Just+click+%22Submit+new+issue%22.+You+do+not+need+to+change+anything.)

</div>

<sub>One click is one step. Hitting a wall or yourself ends the game, and reversing straight back is ignored. The game logic lives in [`game/`](game/) and has its own tests.</sub>

## 📊 GitHub activity

<div align="center">

<img height="180" src="profile-summary-card-output/github_dark/3-stats.svg" alt="GitHub stats" />
<img height="180" src="profile-summary-card-output/github_dark/1-repos-per-language.svg" alt="Top languages by repo" />
<img height="180" src="profile-summary-card-output/github_dark/2-most-commit-language.svg" alt="Top languages by commit" />

<br/>

The autopilot version: a snake that eats my contribution graph.

<img src="https://raw.githubusercontent.com/Veladicodes/Veladicodes/output/github-snake-dark.svg" alt="Contribution snake" />

</div>

---

<div align="center">
  <sub>Open to ML / AI engineering internships and collaborations. Reach out on LinkedIn or by email.</sub>
</div>
