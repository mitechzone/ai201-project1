# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

The chosen domain is **Student reviews of CS 6515: Graduate Algorithms (GA) in the OMSCS program at Georgia Intitute of Technology**.

OMSCS is a leading online M.S. in Computer Science program with a large and diverse student and alumni community. CS 6515: Graduate Algorithms (GA) is a foundational graduate-level algorithms course and a core requirement for multiple OMSCS specializations. It is also one of the most challenging courses in the program, requiring students to develop strong algorithmic problem-solving skills and perform well on rigorous assessments. As a result, many students carefully research the course before enrolling to understand its difficulty, workload, study strategies, and common pitfalls.

This information is difficult to obtain through official channels because Georgia Tech does not maintain a centralized platform of student course reviews. Instead, relevant information is scattered across community-driven sources such as OMSHub (omshub.org), OMS Reviews (omscentral.com), and discussions on the r/OMSCS subreddit, making it challenging to discover, aggregate, and analyze systematically.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | OMS Reviews | Student reviews on OMS Reviews | https://www.omscentral.com/courses/introduction-to-graduate-algorithms/reviews |
| 2 | OMSHub | Student reviews on OMSHub | https://www.omshub.org/course/CS-6515 |
| 3 | Subreddit r/OMSCS | Passed CS6515 GA with A 97% Score, My Experience and Tips | https://www.reddit.com/r/OMSCS/comments/1pj9xen/passed_cs6515_ga_with_a_97_score_my_experience/ |
| 4 | Subreddit r/OMSCS | How to Pass Graduate Algorithms CS6515 | https://www.reddit.com/r/OMSCS/comments/1q0s8gw/how_to_pass_graduate_algorithms_cs6515/ |
| 5 | Subreddit r/OMSCS | CS6515 (Graduate Algorithms) - its true what they say... | https://www.reddit.com/r/OMSCS/comments/vleq4h/cs6515_graduate_algorithms_its_true_what_they_say/ |
| 6 | Subreddit r/OMSCS | Preparing for CS6515 Introduction to Graduate Algorithms in advance | https://www.reddit.com/r/OMSCS/comments/1k9jta5/preparing_for_cs6515_introduction_to_graduate/ |
| 7 | Subreddit r/OMSCS | Some notes for future GA students | https://www.reddit.com/r/OMSCS/comments/1hg51fx/some_notes_for_future_ga_students/ |
| 8 | Subreddit r/OMSCS | Study technique for CS6515 GA - My personal experience | https://www.reddit.com/r/OMSCS/comments/1idfnfi/study_technique_for_cs6515_ga_my_personal/ |
| 9 | Subreddit r/OMSCS | Graduate Algorithms (GA) Summer 2023 Final Review | https://www.reddit.com/r/OMSCS/comments/15ev3vm/graduate_algorithms_ga_summer_2023_final_review/ |
| 10 | Subreddit r/OMSCS | OSI False Accusation Survivor with Advice | https://www.reddit.com/r/OMSCS/comments/1h21nsz/osi_false_accusation_survivor_with_advice/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
