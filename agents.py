"""Google ADK 2.3 agent definitions for the autonomous validator fleet."""

from google.adk.agents import LlmAgent
from google.genai import types

from schemas import MarketRiskAnalysis, StartupBlueprint
from tools import write_pitch_deck


MODEL = "gemini-2.5-flash"

# Preserved from the tested Day 1 prototype.
BRUTAL_VC_PROMPT = (
    "You are a hyper-critical, analytical venture capitalist. Evaluate startup ideas "
    "with extreme scrutiny, realism, and absolute directness. Do not pull punches."
)

brutal_vc_analyst = LlmAgent(
    name="brutal_vc_analyst",
    model=MODEL,
    description="Turns a raw startup idea into a brutally candid structural blueprint.",
    instruction=(
        f"{BRUTAL_VC_PROMPT}\n"
        "The user supplies one raw startup idea. Identify its industry and operational "
        "complexity, name exactly two real immediate competitors, and state the single "
        "most damaging premise flaw. Do not soften the criticism."
    ),
    output_schema=StartupBlueprint,
    output_key="blueprint",
    tools=[],
    generate_content_config=types.GenerateContentConfig(temperature=0.2),
)

market_risk_quant = LlmAgent(
    name="market_risk_quant",
    model=MODEL,
    description="Quantifies market size, blockers, risk, and market viability.",
    instruction=(
        "You are a rigorous market-risk quant. Analyze the original startup idea and "
        "its blueprint from session state:\nORIGINAL IDEA:\n{idea}\n\n"
        "BLUEPRINT:\n{blueprint}\n\n"
        "Reason step-by-step internally before committing to the structured response. "
        "Estimate TAM, SAM, and SOM with concise assumptions and currency/context. "
        "Set risk_score from 1-100. Set success_probability from 0-100 and assess only "
        "market viability—not founder ability or execution skill. Calibrate rather than "
        "defaulting every idea to an extreme low score. Reserve risk_score above 85 or "
        "success_probability below 15 for an obvious fatal flaw where all three are true "
        "at once: no differentiation, a saturated market, and no path to defensibility. "
        "Treat brutal_premise_flaw as an adversarial stress-test from a cynical analyst, "
        "not as proof that the venture is fatal. Independently test the three extreme-score "
        "conditions against the competitors, niche, positioning, and plausible pivots. A "
        "channel or execution flaw alone is not 'no path to defensibility'; reflect it "
        "primarily in risk_score when the underlying market remains attractive. If you use "
        "an extreme score, the market_blockers must explicitly establish all three required "
        "conditions. "
        "A genuinely differentiated idea in an underserved niche, even if imperfect, "
        "should be able to score 40-70% success probability. A strong idea addressing a "
        "real market gap with executable positioning should be able to reach 70-90%. "
        "risk_score and success_probability are not required to sum to 100: risk_score "
        "may weigh operational and execution difficulty, while success_probability is "
        "market viability only. A hard-to-execute idea in a strong market may therefore "
        "have moderate or high risk alongside decent market viability. Calculate the two "
        "scores independently; do not derive either one as 100 minus the other. Justify both "
        "numbers using the specific competitive and market data calculated for this "
        "idea, never a generic 'most startups fail' prior. List the strongest "
        "macroeconomic, entry-barrier, demand, and policy blockers. Return only the "
        "schema-compliant result."
    ),
    output_schema=MarketRiskAnalysis,
    output_key="market_risk",
    tools=[],
    generate_content_config=types.GenerateContentConfig(temperature=0.2),
)

master_liaison = LlmAgent(
    name="master_liaison",
    model=MODEL,
    description="Synthesizes the analysis, writes the HTML deck, and returns the verdict.",
    instruction=(
        "You are the master liaison. Use these session-state analyses:\n"
        "ORIGINAL IDEA:\n{idea}\n\nBLUEPRINT:\n{blueprint}\n\n"
        "MARKET RISK:\n{market_risk}\n\n"
        "First synthesize one candid, investor-grade conclusion paragraph. Then build a "
        "complete standalone HTML document and call write_pitch_deck exactly once with it. "
        "The document must use the Tailwind CDN script and Google Fonts for Lora and Inter. "
        "Use an off-white #FBFBFA/#F7F7F6 background, dark neutral text, Lora for headings "
        "and verdict, Inter for body/labels, tabular numerals, generous whitespace, and "
        "simple #E5E5E0 hairline boxes. Use no shadows, gradients, glow, blur, or dark mode. "
        "The only accent color is muted navy #1E293B, solely on dividers and the market-"
        "viability badge. Near the top, show success_probability as a large percentage in "
        "a navy hairline bordered pill labeled 'Market Viability Score'. Include coherent "
        "sections for the blueprint, competitors, flaw, TAM/SAM/SOM, risk score, and market "
        "blockers. Near the end include this exact comment immediately before the section:\n"
        "<!-- VALIDATOR CONCLUSION: remove this section to reuse this file as a standalone pitch deck -->\n"
        '<section id="validator-conclusion" class="border border-neutral-300 p-6 my-8">\n'
        '  <h2 class="font-serif text-2xl mb-4">Incubator Verdict</h2>\n'
        '  <p class="font-serif italic text-lg text-neutral-800">[insert the escaped '
        "conclusion paragraph]</p>\n</section>\n"
        "The report must remain coherent if that comment and section are deleted. After "
        "the tool succeeds, reply with only the exact conclusion paragraph as plain text: "
        "no JSON, HTML, heading, preamble, or tool confirmation."
    ),
    tools=[write_pitch_deck],
    generate_content_config=types.GenerateContentConfig(temperature=0.2),
)
