# Evaluation Strategy for Text-to-SQL Agent

## Overview

When I started thinking about this task, the first question that came to my mind was — how do we actually know if a Text-to-SQL agent is doing a good job? Just because it generates some SQL doesn't mean it's correct. So for this part, I want to lay out a clear strategy for how we can evaluate whether the agent is actually working well or not.

The way I see it, there are three main things we need to check:

1. Does the SQL actually run without errors?
2. Does it return the correct result?
3. Is the agent smart enough to fix its own mistakes?

Let me go through each of these.

---

## 1. Execution Success Rate

The most basic thing to check is whether the generated SQL even runs. If the agent writes SQL with wrong column names, missing quotes, or broken joins, PostgreSQL will just throw an error and the query won't execute at all.

So the first metric I would track is simply:

**What percentage of the generated queries actually execute without any database errors?**

If this number is low, it means the agent doesn't have a solid understanding of the database schema. For example, in our Classic Models database, column names like `customerNumber` and `productLine` need to be wrapped in double quotes. If the agent forgets this, every query it writes will fail immediately.

---

## 2. Execution Accuracy (The Most Important One)

This is the metric that matters the most to me. Even if a query runs successfully, it might return completely wrong data. For example, the agent could write a query that runs fine but accidentally joins the wrong tables and returns customers from Spain instead of France.

The way to evaluate this properly is to compare the result rows that the agent's query returns against the result rows that our manually written ground truth query returns. If both return the exact same data, then the agent got it right.

I think this is a much better approach than doing a direct string comparison between the two SQL queries. The reason is that there are often multiple valid ways to write the same correct query. For example, someone might write `WHERE country = 'France'` and another person might write `WHERE UPPER(country) = 'UPPER'` — both can return the same result. So we should compare what comes out of the database, not just the SQL text itself.

**How to calculate it:**

```
Execution Accuracy = (Queries that return identical results to ground truth) / (Total Queries)
```

---

## 3. Structural Check Using AST Matching

Sometimes comparing results alone is not enough. I also want to know if the agent is selecting the right tables, using the right joins, and grouping or filtering correctly. For example, maybe the agent accidentally writes a query that returns correct-looking results but for completely wrong reasons.

To catch this, I would parse both the generated SQL and the ground truth SQL into an Abstract Syntax Tree (AST) using a tool like `sqlglot`. An AST basically breaks down the SQL into its logical parts — the SELECT columns, the FROM tables, the JOIN conditions, the WHERE filters, etc. By comparing the trees, we can check whether the agent understood the structure of the query correctly, even if the exact wording is slightly different.

This is especially useful when reviewing queries that involve complex joins or aggregations.

---

## 4. Self-Correction and Retry

Another thing I want to evaluate is how well the agent handles its own mistakes. In a real-world scenario, if the first query fails, the agent should be able to look at the error message from PostgreSQL, understand what went wrong, and try again with a corrected query.

So I would test this by intentionally running the agent on tricky questions and recording:

- Did the first query fail?
- Did the agent retry?
- Did the retry succeed?

A good agent should be able to self-correct at least some of the time. If it keeps failing even after retries, that's a sign the agent doesn't understand the schema well enough.

---

## 5. Response Latency

This one is more about user experience. If the agent takes 30 to 40 seconds to return an answer, it's not really practical to use in real life. I would track how long it takes from when the question is asked to when the final result is returned.

Ideally, for simple questions, this should be fast — under 5 seconds. For complex multi-join aggregation queries, a bit longer is acceptable, but anything over 15 seconds would be a problem.

---

## 6. Quality of the Natural Language Answer

Finally, a Text-to-SQL agent isn't just supposed to return raw data — it should explain the result in plain English. So the last thing I want to evaluate is whether the final answer actually makes sense as a human-readable response.

For example, instead of just returning a JSON table of customer names, the agent should say something like:

> "There are 13 customers from France in the database. Here are the top ones..."

I would evaluate this manually or by checking if the response is relevant to the original question.

---

## Summary Table

| Metric | What It Checks | Why It Matters |
| :--- | :--- | :--- |
| Execution Success Rate | Does the SQL run without errors? | Catches broken syntax and wrong column names |
| Execution Accuracy (EX) | Does it return the correct data? | The most important measure of correctness |
| AST Structural Match | Does the query use the right logic? | Catches wrong table/join usage even if results look similar |
| Self-Correction Rate | Can the agent fix its own mistakes? | Makes the agent more reliable in real use |
| Response Latency | How fast is it? | Practical usability |
| NL Answer Quality | Does it explain the result properly? | End-user experience |

---

## How I Will Use This in Task 3 and 4

When I build the Text-to-SQL agent in the upcoming tasks, I will use these metrics to test it against the benchmark questions from Task 1. For each question, I will compare the agent's output against my manually written ground truth SQL and score it using execution accuracy as the main measure. If the agent fails, I will check the error message and see if adding a retry loop improves the success rate.

This way, I will have a clear and honest picture of how well my agent is actually performing.
