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

The chosen domain is **Student reviews of CS 6515: Graduate Algorithms (GA) in the OMSCS program at Georgia Institute of Technology**.

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

**Chunk size:** 1,200 characters (~300 tokens).

**Overlap:** 200 characters (~50 tokens).

**Why these choices fit your documents:** Most individual reviews are self-contained at a few hundred to ~1,200 characters, so a 1,200-character window keeps the majority of a single student's review (or a coherent paragraph of a long review) intact, preserving one person's perspective rather than blending opinions across students and semesters. The 200-character overlap is a safety net so a fact split near a boundary still appears whole in an adjacent chunk.

**Preprocessing**: Documents were cleaned manually during collection (stripping HTML, removing headers, etc.) 

**Final chunk count:** Two strategies were implemented.

### Fixed-size

The strategy slides a fixed 1,200/200 character window and produced **1,329 chunks** across all documents.

### Recursive

This strategy splits on a separator hierarchy (paragraph -> newline -> sentence -> word) with the overlap trimmed to the nearest word so chunks never start mid-word. It produced **1,820 chunks** across all documents.

## Sample Chunks

Five representative chunks from the recursive strategy, each labeled with its source document:

1. From `1.txt`:

> Spring 2026\n\nTL/DR: This course has a reputation of graduation gatekeeping, and while it can be difficult, it is very doable if you are diligent and detail oriented when following course expectations.\n\nPeople will be unkind this course, but I enjoyed it and have some thoughts. Keep in mind that OMSCS is a massive program and thus the acceptance rate is much higher than other masters programs. In my experience, there are a lot of students that think earning a masters is a simply a matter of paying for the courses. A masters degree is difficult and requires work outside of areas you are completely comfortable with. This was a somewhat frustrating course, but there are some interesting course lessons to learn along the way. Anyways, my thoughts:

2. From `2.txt`:

> practice homework problems, watch the office hours, and invest in an external webcam. (Shelling out $50 for a webcam is annoying, but it does make the exam proctoring less stressful) \n\n\n\nSummer 2020\n\nI spent the 7 prior semesters hearing horror stories about GA and I don't have an undergraduate CS degree (and thus have never taken an algorithms course), so I went in expecting a very painful semester.  I was pleasantly surprised to find the material challenging yet approachable, and the workload very manageable. The lectures are well-done and explain things very clearly, yet aren't overly long and bloated.  I rarely found myself having to do outside research to understand the lectures despite my limited algorithms background.  Overall, you'll learn a lot of useful and interesting material if you're willing to put in a reasonable amount of time/effort.

3. From `4.txt`:

> more from those than from professor office hours. I worked through his practice problems repeatedly, and that made a huge difference.\n\nI averaged about seventeen hours per week and earned a solid B.\n\nMy honest take is that around ten hours per week would probably not have been enough for me to pass. Around seventeen hours made a B achievable. Around twenty three or more hours might have made an A possible, but it would have been very difficult. I do not think I am particularly gifted at this material. The amount of time I put in correlated very directly with how well I did.\n\nTaking PTO is something I strongly recommend. There are three exams, and realistically the most useful study material, especially TA walkthroughs, only becomes available about a week before each exam. Before that it can be hard to even know how to study effectively.\n\nI took a three day weekend for each exam and a four day weekend for one of them. If I had not taken PTO, I think passing would have been much harder. If you are working full time, I would strongly recommend taking at least one PTO day per exam.

4. From `6.txt`:

> course material on my own before the semester starts. Even I understand I may not be able to get a seat in upcoming semester, this is eventually a course I have to take so I wouldn't delay.\n\nMy plan:\n\nI want to go over the course recording, some exercises from the textbook, and also student's notes (specific ga-notes) before the fall semester. If you have a similar plan, DM me. I will be happy to form a study group for those who want to study GA in advance.

5. From `9.txt`:

> **Class Deliverables:**\n\n-   3 Logistics Quizzes: 3%\n-   6 Quizzes: 7%\n-   8 Homeworks: 12%\n-   3 Coding Projects: 6%\n-   3 Exams (only 3 in Summer): 72%\n    \n\n**Review of Deliverables + Tips To Succeed**



---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers` as recommended

**Production tradeoff reflection:**

If cost wasn't a constraint, the following factors should be considered when choosing a different embedding model for production deployment:

* Context length limits

    `all-MiniLM-L6-v2` truncates input at ~256 tokens, so a longer-context model (e.g., `text-embedding-3-large`) could embed a whole long review as one vector.
    
* Domain accuracy

    A model that maps computer science and grading terminology more precisely would improve retrieval on jargon-heavy queries.
    
* Latency

    Larger embedding dimensions slow vector search, degrading the live query experience.
    
* Multilingual support

    Low marginal value here since the corpus is English.

## Retrieval Test Results

**Query 1: "How many exams does GA typically have in recent semesters?"**

* Chunk 1 (`1.txt` Distance 0.328)

    > 25% for each exam\nIn the Fall/Spring semesters, a final exam can replace your lowest exam score\n8 HW Assignments: 10%\n3 Coding Projects: 9%\n8 Quizzes (the exact number depends on the semester): 6%\n\nCriticisms of GA\nMy main gripe with GA is that we had a free response problem as one of our \"multiple choice\" questions for Exam 3. This is mostly on me for not preparing properly since we had a fill-in-the-blank question for the multiple choice section of Exam 2 as well. I lost 6/9 points for the free response problem on Exam 3 since I hadn't been expecting that I would have to provide my own answers hah. Yikes!

* Chunk 2 (`2.txt` Distance 0.380)

    > each exam  \nIn the Fall/Spring semesters, a final exam can replace your lowest exam score  \n8 HW Assignments: 10%  \n3 Coding Projects: 9%  \n8 Quizzes (the exact number depends on the semester): 6%  \n\n**Criticisms of GA**  \nMy main gripe with GA is that we had a free response problem as one of our \"\"multiple choice\"\" questions for Exam 3. This is mostly on me for not preparing properly since we had a fill-in-the-blank question for the multiple choice section of Exam 2 as well. I lost 6/9 points for the free response problem on Exam 3 since I hadn't been expecting that I would have to provide my own answers hah. Yikes!

* Chunk 3 (`8.txt` Distance 0.390)

    > GA is a polarizing course. Some say the course is easy, that they can get an A without a background in CS or math. Others were struggling despite having passed 9 courses before GA. Having taken the course myself in Fall 2024, I see no contradiction between the two. The content in GA is no harder than the average OMSCS course, but scoring can be hard. The key is your ability to synthesize course content into exam answers that can score points. I believe some students do better than the others in this regard. I also believe that anyone can develop this ability by having the correct study and exam techniques.\n\nMy approach to studying\n\nDuring the semester, I have developed a specific study routine that worked well with me.


**Why are these chunks relevant?**

The query is about exam structure, and the top two chunks are the explicit course grading breakdown. The low distances reflect a strong topical match.

---

**Query 2: "What's the cut score to earn a B in GA in recent semesters?"**

* Chunk 1 (`8.txt` Distance 0.454)

    > GA is a polarizing course. Some say the course is easy, that they can get an A without a background in CS or math. Others were struggling despite having passed 9 courses before GA. Having taken the course myself in Fall 2024, I see no contradiction between the two. The content in GA is no harder than the average OMSCS course, but scoring can be hard. The key is your ability to synthesize course content into exam answers that can score points. I believe some students do better than the others in this regard. I also believe that anyone can develop this ability by having the correct study and exam techniques.\n\nMy approach to studying\n\nDuring the semester, I have developed a specific study routine that worked well with me.

* Chunk 2 (`5.txt` Distance 0.459)

    > I'm in GA and we're currently preparing for exam 2, and I figured I'd share some information with future students. A few notes about myself, because I know you may be thinking \"here's another lazy whiner\". I have a 3.6 GPA, which is evidently not perfect. My undergrad was not in CS but in Computer Engineering. I took EOS, AOS, SICC and DC as electives because I knew they were intense courses but would be rewarding. This is my 9th class. I'm a SWE at a FAANG company.\n\nIf you don't know, this course requires a 70% to get a B [the curve] and a B is mandatory for most specializations for graduation. TAs say this may be adjusted at the end but who knows by how much? At the start of class, I joined a study group with [originally] 5 people. Of the 5 in the study group, 2 people have withdrawn - both taking this as their final course before graduation. 2 of the 3 remaining people received Fs on exam 1, including myself. Here are some exam 1 statistics:\n\n- Mean: 36.8/60 (61%)\n\n- Median: 37.4/60 (62%)

* Chunk 3 (`1.txt` Distance 0.464)

    > 25% for each exam\nIn the Fall/Spring semesters, a final exam can replace your lowest exam score\n8 HW Assignments: 10%\n3 Coding Projects: 9%\n8 Quizzes (the exact number depends on the semester): 6%\n\nCriticisms of GA\nMy main gripe with GA is that we had a free response problem as one of our \"multiple choice\" questions for Exam 3. This is mostly on me for not preparing properly since we had a fill-in-the-blank question for the multiple choice section of Exam 2 as well. I lost 6/9 points for the free response problem on Exam 3 since I hadn't been expecting that I would have to provide my own answers hah. Yikes!


**Why are these chunks relevant?**

The query is about course cut score. Chunk 2 contains the direct answer "this course requires a 70% to get a B".

---

**Query 3: "Is homework graded in recent semesters?"**

* Chunk 1 (`1.txt` Distance 0.447)

> taking final exam(optional)~~ Passed with a easy B; The minimum requirement to get A is to try your best for exams.\n\nThe grading feedback from Some TAs in the Fall 2021 semester are really horrible.\n\nI believe that there is some unspoken rules: (Homework weights are small(7 homework accounts for total 12% grading). Students are encouraged to discuss how to solve those problems without directly revealing answers.)\nBut even based on the above expectation, grading feedback from some TAs are still not professional.\nIf you have a hard time finishing homework or not confident you have nailed that homework, but you wish you can get positive grading feedback, you will end up with disappointment: because some of TAs contributed little effort to grade your homework (although there is nothing staying in your way of regrading.)\n\nSummer 2021

* Chunk 2 (`2.txt` Distance 0.456)

> Exam 1, Exam 2 with medium scores, ~~I really wish I can pass this course without taking final exam(optional)~~ Passed with a easy B; The minimum requirement to get A is to try your best for exams.\n\nThe grading feedback from **Some TAs** in the Fall 2021 semester are really horrible. \n- I believe that there is some unspoken rules: \n*(Homework weights are small(7 homework accounts for total 12% grading). Students are **encouraged** to discuss how to solve those problems without directly revealing answers.)*\n- But even based on the above expectation, grading feedback from some TAs are still not professional.\n- If you have a hard time finishing homework or not confident you have nailed that homework, but you wish you can get positive grading feedback, you will end up with disappointment: because some of TAs contributed little effort to grade your homework (although there is nothing staying in your way of regrading.) \n\n\nSummer 2021

* Chunk 3 (`2.txt` Distance 0.433)

> is another key part of the course. While not every problem is graded, it’s important to work through all of them and then review the evaluation threads where other students share their approaches. Seeing how others tackle problems can give you new perspectives and help solidify your understanding. If you think your homework or exam was graded unfairly, don’t hesitate to ask for a regrade. I found that as long as I articulated my reasoning clearly, my regrades were always justly awarded. The workload is heavy—it’s not uncommon to spend 15–20 hours a week on this course between homework, reviewing materials, and preparing for exams. But the effort is worth it because you come out with a much stronger grasp of algorithms and problem-solving skills. It’s definitely a challenging experience, but if you stay consistent and use all the resources available to you, it’s manageable and very rewarding in the end.

**Why are these chunks relevant?**

The query is about homework. These retrived chunks discuss homework grading/weighting.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

> You are a helpful assistant answering questions about Georgia Tech's CS 6515 Graduate Algorithms (GA) course using ONLY the numbered context below, which is excerpts from student reviews. Follow these rules strictly:
> 1. Use only information in the numbered context. Never use outside knowledge or fill in gaps from what you already know.
> 2. After each claim, cite the marker(s) it came from, e.g. 'Exams are 30% each [1].'
> 3. If the context does not contain enough information to answer, reply with exactly this sentence and nothing else: The retrieved sources don't contain enough information to answer that."
>
> Keep the answer concise (2-5 sentences).

In addition to the system prompt, each retrieved chunk is injected as numbered, source-labeled context along with a 0.2 temperature for factual stability.

**How source attribution is surfaced in the response:**

I used citation markers for source attribution. After generation, the script parse the `[n]` markers back out of the answer and map them to the exact chunks the model cited.

**Example 1 (Grounded Generation with Source Attribution)**

Query:

> Are there quizzes in the course?

Answer:

> Yes, there are quizzes in the course [1, 2]. The quizzes are almost every week, except exam weeks, and are 5-10 questions that relate directly to the lecture material [1]. They can be taken or retaken as many times as desired within the week [1]. Additionally, there are logistic quizzes which are considered free points [1, 2].

> [1] 9.txt — chunk 7 (distance 0.370)
> Logistic Quizzes: These are quizzes...

> [2] 1.txt — chunk 148 (distance 0.376)
> ... Quizzes The logistics quizzes are free points 2 attempts per quiz with some showing the answers (format) and some hiding the answer (content)...


**Example 2 (Gronded Generation with Source Attribution)**

Query:

> Is GA difficult?

Answer:

> GA is a difficult course [2]. Some students find it easy, but others struggle despite having a strong background [1]. The difficulty lies not only in the content, but also in scoring well on exams, which requires the ability to synthesize course content into exam answers [1]. However, it's suggested that with the correct study and exam techniques, anyone can develop this ability [1]. The course may still be stressful even with hard work [2].

> [2] 1.txt — chunk 625 (distance 0.377)
> ... this course is difficult....

> [1] 8.txt — chunk 0 (distance 0.329)
> GA is a polarizing course. Some say the course is easy, that they can get an A without a background in CS or math. Others were struggling despite having passed 9 courses before GA...



**Example 3 (Out-of-scope refusal)**

Query:

> What is the weather in GA today?

Answer:

> The retrieved sources don't contain enough information to answer that.

> No sources — the model declined to answer.

## Query Interface

A Gradio web app (`app.py`) at:
> http://localhost:7860

**Input:**
* **Question** (text box)
* **Chunking strategy** (radio button): `recursive` (default), `fixed_size`, or `compare both`.
* **Chunks to retrieve (top-K)** (slider): from 1 to 8, default 5.

**Output:**
- **Answer** with inline citation markers.
- **Sources cited**: the exact chunk(s) the model cited (source file, distance, and the chunk text).
- **Retrieved context** (collapsible): all top-K chunks supplied to the model.


**Sample interaction transcript:**
```
Question: How are exams weighted in GA?
Chunking strategy: recursive
Chunks to retrieve (top-K): 5

Answer:
  Exams are weighted 25% each in the GA course [1, 3]. However, in some semesters, such as Summer, the exam weighting may be different, with 3 exams accounting for 90% of the score [5].

Sources cited:
  [1] 1.txt — chunk 669 (distance 0.372)

  25% for each exam In the Fall/Spring semesters, a final exam...

  [3] 2.txt — chunk 229 (distance 0.427)

  each exam In the Fall/Spring semesters, a final exam can replace...

  [5] 2.txt — chunk 405 (distance 0.473)

  They do not help with office hours and they barely answer any question...
```

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->


| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Is GA a core course for all OMSCS specializations? | No. | GA is considered a core course for most OMSCS specializations, with some students stating it's a must-take course for the program [3, 4]. However, the context does not explicitly state that it is required for all specializations. Some reviews imply that passing GA with a good grade is necessary for graduation in many specializations [6]. The retrieved sources don't contain enough information to definitively answer if GA is a core course for all OMSCS specializations. | Relevant | Partially accurate |
| 2 | Which OMSCS specializations do not require GA? | HCI (Human-Computer Interaction) and AI (Artificial Intelligence). | The retrieved sources don't contain enough information to answer that. | Partially relevant | Inaccurate |
| 3 | How many exams does GA typically have in recent semesters? | 3 exams. | GA typically has 3 exams in recent semesters [1, 2, 6]. The final exam can also replace the lowest exam score in Fall/Spring semesters [1, 2]. | Relevant | Accurate |
| 4 | What's the cut score to earn a B in GA in recent semesters? | 70%. | The cut score to earn a B in GA is 70% [2]. The curve may be adjusted at the end of the semester, but the exact adjustment is uncertain [2]. | Relevant | Accurate |
| 5 | Is homework graded in recent semesters? | Yes. TAs grade the homework and provide feedback, but it does not contribute to the final course grade. | Homework is graded, but the weights are small, with 7 homework assignments accounting for a total of 12% of the grading [3, 5]. However, doing homework is still important for understanding the course material and performing well in exams [6]. The retrieved sources don't provide information on whether homework grading has changed in recent semesters, but it is mentioned that the grading on homework can be inconsistent and sometimes unprofessional [3, 5, 8]. | Relevant | Inaccurate |

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

> Which OMSCS specializations do not require GA?

**What the system returned:**

> The retrieved sources don't contain enough information to answer that.

**Root cause (tied to a specific pipeline stage):**

This is a **chunking failure**. The fact does exist in `1.txt`:

> ... it's insane the this course needs to be a core course in almost every OMSCS specialization except for HCI and II.

* Note that in the **Expected Answer**, *AI (Artificial Intelligence)* was mentioned instead of *II*. The *AI* specialization was previously known as *II (Interactive Intelligence)*.

For the query *"Which OMSCS specializations do not require GA?"*, the chunk containing the answer does not even appear in the **top 50** results. The chunk has a cosine distance of ~0.64. The top hit, in comparison, has a distance of ~0.31.

In this case, the root cause appears to be the semantic dilution from a too-coarse chunk. Embedding the same sentence in isolation and measuring cosine distance to the query results in ~0.42 which would likely land in the top-K retrival.

**What you would change to fix it:**

I would try a semantic chunker that starts a new chunk when the topic shifts, which would place *"except for HCI and II"* in a coherent unit instead of averaging it with an unrelated rant. This attacks the root cause directly.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

Writing the chunk size, overlap, embedding model, and the 5 evaluation questions in `planning.md` before implementation meant each milestone had a concrete target.

**One way your implementation diverged from the spec, and why:**

The original spec committed to a single **fixed-size** chunking strategy. During retrieval testing I found that fixed-size's chunks were being silently truncated by `all-MiniLM-L6-v2`'s 256-token limit, weakening retrieval. So I added a second **recursive** chunker, while keeping fixed-size as a comparison baseline.

I didn't anticipate the limitation in the spec, and it highlighted how chunking interacts with the embedding model.

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

- *What I gave the AI:* my chunking strategy plus the lecture demo; I asked it to implement an equivalent recursive chunker for my documents.
- *What it produced:* a working `RecursiveChunker`, carrying overlap between chunks.
- *What I changed or overrode:* I inspected the output and noticed many chunks started mid-word. I directed a fix to trim the overlap to the nearest word boundary, then re-ran and confirmed the chunks read cleanly.

**Instance 2**

- *What I gave the AI:* the plan to support two chunking strategies.
- *What it produced:* an initial design putting all chunks in one ChromaDB.
- *What I changed or overrode:* I required the strategies to live in separate ChromaDB instances so chunks from different strategies can never mix or be cross-retrieved.


## Chunking Strategy Comparison

Both chunking strategies were indexed in separate ChromaDB stores and compared on the evaluation queries (raw cosine distance of the best retrieved chunk; lower = better):

| Query | Fixed-size best distance | Recursive best distance | Winner |
|-------|--------------------------|--------------------------|--------|
| Is GA core for all specializations? | 0.399 | **0.341** | Recursive |
| Which specializations don't require GA? | 0.513 (weak) | **0.309** | Recursive |
| How many exams does GA have? | 0.382 | **0.328** | Recursive |

The recursive chunking strategy performed better on every query. One likely cause is the embedding model's 256-token limit, truncating tails silently at embed time, so part of each chunk never contributes to its vector. Recursive's boundary-aware chunks average ~895 characters (~220 tokens), mostly under the cap, so they embed in full and match more precisely.
