#!/usr/bin/env python3
"""
job-description-optimizer — job post → bias score, reading level,
must-have vs nice-to-have split, inclusivity improvements, rewritten version
"""
import anthropic, json, re, sys
from pathlib import Path

SYSTEM = """You are an expert in inclusive hiring, organizational psychology, and talent acquisition.
Analyze this job description for bias, clarity, and effectiveness.

Research shows biased JDs deter qualified candidates before they even apply.
Your job is to find every problem and fix it.

Return ONLY valid JSON — no markdown, no explanation.

{
  "role_title": "extracted role title",
  "overall_score": number_0_to_100,
  "grade": "A|B|C|D|F",
  "reading_level": "6th_grade|8th_grade|10th_grade|college|graduate",
  "estimated_reading_minutes": number,
  "bias_analysis": {
    "gender_bias_score": number_0_to_10,
    "gendered_words_found": ["rockstar","ninja","aggressive","nurturing","..."],
    "age_bias_signals": ["entry-level but requires 10 years","..."],
    "cultural_bias_signals": ["requires native English","specific cultural references","..."],
    "disability_bias_signals": ["must be able to lift","valid driver's license when not needed","..."]
  },
  "requirements_analysis": {
    "must_have": ["genuinely required skills/experience"],
    "nice_to_have": ["skills that would help but aren't blocking"],
    "questionable": [
      {
        "requirement": "original text",
        "issue": "why this may be unnecessary or biased",
        "suggestion": "rewrite or remove"
      }
    ],
    "years_experience_required": number_or_null,
    "years_experience_assessment": "appropriate|too_high|too_low",
    "degree_required": true_or_false,
    "degree_necessary": true_or_false
  },
  "clarity_issues": [
    {
      "phrase": "vague or jargon-heavy phrase",
      "issue": "why it's unclear",
      "suggestion": "clearer alternative"
    }
  ],
  "missing_elements": ["salary range","benefits","remote policy","team size","growth path","..."],
  "inclusion_improvements": [
    {
      "original": "original text",
      "improved": "more inclusive version",
      "why": "explanation"
    }
  ],
  "red_flags_for_candidates": ["things that deter good candidates"],
  "strengths": ["things the JD does well"],
  "rewritten_jd": {
    "title": "optimized title",
    "about_role": "2-3 sentences — what this role does and why it matters",
    "what_youll_do": ["bullet list of key responsibilities — action verbs, specific outcomes"],
    "what_we_need": ["true must-haves only — short, specific, no years unless truly needed"],
    "nice_to_have": ["genuine nice-to-haves"],
    "what_we_offer": ["compensation range","benefits","culture notes"],
    "about_us": "2 sentences — who you are and why someone should care",
    "inclusion_statement": "genuine inclusion statement (not boilerplate)"
  },
  "estimated_applicant_pool_change": "e.g. '+35% more diverse applicants with these changes'",
  "confidence": 0.0
}"""

def optimize(jd_text: str) -> dict:
    client = anthropic.Anthropic()
    if len(jd_text) > 20000: jd_text = jd_text[:20000]
    resp = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=4096, system=SYSTEM,
        messages=[{"role":"user","content":f"Analyze and optimize this job description:\n\n{jd_text}"}]
    )
    raw = re.sub(r'^```(?:json)?\s*','',resp.content[0].text.strip(),flags=re.MULTILINE)
    raw = re.sub(r'\s*```$','',raw,flags=re.MULTILINE)
    return json.loads(raw)

def optimize_file(path: str) -> dict:
    return optimize(Path(path).read_text(encoding="utf-8", errors="replace"))

GRADE_C = {"A":"\033[92m","B":"\033[92m","C":"\033[93m","D":"\033[91m","F":"\033[91m"}
R = "\033[0m"

def print_report(r: dict):
    g = r.get("grade","?")
    print(f"\n{'═'*60}")
    print(f"  JD OPTIMIZER — {r.get('role_title','?')}")
    print(f"  Score: {GRADE_C.get(g,'')}{g}{R} ({r.get('overall_score',0)}/100)")
    print(f"  Reading level: {r.get('reading_level','?')} | ~{r.get('estimated_reading_minutes',0)} min read")
    print(f"{'═'*60}")

    bias = r.get("bias_analysis",{})
    bias_score = bias.get("gender_bias_score",0)
    print(f"\n  Gender bias: {'█'*bias_score}{'░'*(10-bias_score)} {bias_score}/10")
    gendered = bias.get("gendered_words_found",[])
    if gendered: print(f"  Gendered words: {', '.join(gendered[:6])}")
    age_signals = bias.get("age_bias_signals",[])
    if age_signals:
        for s in age_signals[:2]: print(f"  ⚠ Age bias: {s}")

    req = r.get("requirements_analysis",{})
    questionable = req.get("questionable",[])
    if questionable:
        print(f"\n{'─'*60}\n  QUESTIONABLE REQUIREMENTS")
        for q in questionable[:5]:
            print(f"\n  ⚠ \"{q.get('requirement','')[:60]}\"")
            print(f"     Issue: {q.get('issue','')}")
            print(f"     Fix: {q.get('suggestion','')}")

    clarity = r.get("clarity_issues",[])
    if clarity:
        print(f"\n{'─'*60}\n  CLARITY ISSUES")
        for c in clarity[:4]:
            print(f"  \"{c.get('phrase','')}\" → \"{c.get('suggestion','')}\"")

    missing = r.get("missing_elements",[])
    if missing: print(f"\n  Missing: {', '.join(missing)}")

    inclusion = r.get("inclusion_improvements",[])
    if inclusion:
        print(f"\n{'─'*60}\n  INCLUSION IMPROVEMENTS")
        for i in inclusion[:3]:
            print(f"\n  Before: \"{i.get('original','')[:70]}\"")
            print(f"  After:  \"{i.get('improved','')[:70]}\"")
            print(f"  Why: {i.get('why','')}")

    rjd = r.get("rewritten_jd",{})
    if rjd:
        print(f"\n{'─'*60}\n  REWRITTEN JD — {rjd.get('title','')}")
        print(f"\n  {rjd.get('about_role','')}")
        must = rjd.get("what_we_need",[])
        if must:
            print(f"\n  What we need:")
            for m in must: print(f"  • {m}")
        nice = rjd.get("nice_to_have",[])
        if nice:
            print(f"\n  Nice to have:")
            for n in nice: print(f"  • {n}")

    if r.get("estimated_applicant_pool_change"):
        print(f"\n  Impact: {r['estimated_applicant_pool_change']}")
    print(f"\n  Confidence: {int(r.get('confidence',0)*100)}%")
    print(f"{'═'*60}\n")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args: print("Usage: python -m jd_optimizer <jd.txt> [--json]"); sys.exit(0)
    text = Path(args[0]).read_text(encoding="utf-8",errors="replace") if Path(args[0]).exists() else sys.stdin.read() if args[0]=="-" else args[0]
    r = optimize(text)
    if "--json" in args: print(json.dumps(r,indent=2,ensure_ascii=False))
    else: print_report(r)
