# job-description-optimizer

> **Any job post → bias score, inclusivity improvements, must-have vs nice-to-have split, rewritten version.** Expands your candidate pool by removing unconscious barriers.

[![PyPI](https://img.shields.io/pypi/v/job-description-optimizer?style=flat)](https://pypi.org/project/job-description-optimizer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Quickstart

```bash
pip install job-description-optimizer
python -m jd_optimizer job_post.txt
python -m jd_optimizer job_post.txt --json
```

## What it detects

- **Gender-coded words** — "rockstar", "ninja", "aggressive", "nurturing"
- **Age bias signals** — "entry-level but requires 10 years experience"
- **Unnecessary requirements** — degree required for roles that don't need it
- **Vague language** — "excellent communication skills", "self-starter"
- **Missing elements** — no salary range, no remote policy, no team size

## What it produces

A rewritten JD with must-haves separated from nice-to-haves, gendered language replaced,
vague requirements made specific, and a genuine inclusion statement.

## License
MIT © [Alper Nabil Gabra Zakher](https://github.com/AlperNab)
