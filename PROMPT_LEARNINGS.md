# What I Learned About Prompt Engineering

**Date:** 2025-12-04
**Task:** Creating prompts for RAG system with Mixtral 8x7b

---

## The Problem I Was Solving

I needed to create prompts that combine user queries with retrieved document chunks to generate relevance explanations. The LLM needs to explain why each retrieved paper is (or isn't) relevant to the research question.

---

## Initial Attempt Issues

### Issue 1: Response Was Cut Off
**What happened:** The detailed explanation only completed 1 paper out of 3, then stopped mid-sentence.

**Why it happened:** I wasn't setting `num_predict` in the Ollama API call, so it used a very short default token limit.

**The fix:**
```python
"options": {
    "num_predict": 2000,  # Allow up to 2000 tokens in response
    "temperature": 0.7     # Some creativity but not too much
}
```

### Issue 2: Instructions Weren't Clear Enough
**What happened:** The model didn't seem motivated to complete all papers.

**Why it happened:** My prompt said "For each paper, provide..." but didn't emphasize that ALL papers needed analysis.

**The fix:**
- Changed to "TASK: Analyze ALL papers above..."
- Added at the end: "Make sure to analyze ALL papers provided above."
- Used emphasis (CAPS) to make requirements clear

---

## What Works Well

### System Prompt (Sets the AI's Role)
```
You are an expert research assistant specializing in academic literature.
Your task is to explain why retrieved papers are relevant to a research question.
Base your explanations ONLY on the provided text.
Be specific and cite paper sources.
Use clear, professional language.
```

**Why this works:**
- Establishes expert persona
- Sets clear boundaries (only use provided text)
- Emphasizes relevance over summarization

### User Prompt Structure
1. State the research question first
2. Show each document clearly separated
3. Include source filename and similarity score
4. Give explicit task instructions
5. Provide exact output format

### Two Modes I Created

**Detailed Mode:**
- Provides: Relevance level + Explanation + Key concepts
- Good for: Thorough analysis
- Takes: ~30-60 seconds

**Simple Mode:**
- Provides: One sentence per paper
- Good for: Quick overviews
- Takes: ~15-30 seconds

---

## Key Insights

1. **API parameters matter a lot**
   - `num_predict` controls how much text the model generates
   - `temperature` controls creativity (0.7 is good balance for academic work)

2. **Explicit > Implicit**
   - Don't assume the model knows to do everything
   - Say "ALL papers" not just "each paper"
   - Repeat important requirements

3. **Format matters**
   - Clear separators between documents (---)
   - Numbered papers (Paper 1, Paper 2, etc.)
   - Show exact output format you want

4. **Different prompts = Different perspectives**
   - Same paper got "Moderately Relevant" vs "Highly Relevant"
   - Both were valid interpretations
   - Depends on what aspect the prompt emphasizes

---

## Practical Tips for Future Adjustments

### If responses are too short:
- Increase `num_predict` value
- Add more explicit instructions about completeness

### If responses are too verbose:
- Decrease `num_predict` value
- Add length constraints to prompt ("2-3 sentences")

### If format is inconsistent:
- Show exact format example in prompt
- Use clear markers like [Paper X - filename]

### If accuracy is poor:
- Emphasize "ONLY use provided text"
- Lower temperature (closer to 0)
- Make system prompt more strict

---

## Testing Results

**Test Query:** "machine learning for document classification"

**Retrieved Papers:**
- Paper 1: Credential handling errors (similarity: 0.389)
- Paper 2: Query-document filtering with cross-encoders (similarity: 0.345)
- Paper 3: BERT/RoBERTa for document classification (similarity: 0.344)

**Results:**
- All 3 papers got complete assessments ✓
- Paper 3 correctly identified as most relevant ✓
- Explanations were based on actual content ✓
- Format was consistent and parseable ✓

---

## What I Still Want to Explore

- [ ] Test with more diverse queries
- [ ] Try different temperature values
- [ ] Experiment with very specific vs very broad queries
- [ ] See how it handles queries with no relevant papers
- [ ] Compare detailed vs simple mode quality systematically

---

## Code Location

File: `src/generation.py`
- `ExplanationGenerator.generate()` - Detailed explanations
- `ExplanationGenerator.generate_simple()` - Quick summaries
- `ExplanationGenerator.create_prompt()` - Prompt formatting logic
