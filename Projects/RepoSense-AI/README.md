# RepoSense AI

**Private, explainable machine-learning triage for GitHub issues.** Analyze an issue, inspect the evidence behind its prediction, find similar reports, and teach a model from your corrections.

## Features

- **Real local machine learning:** Multinomial Naive Bayes with add-one smoothing and a starter set of 48 hand-written example reports (12 per label).
- **Explainable predictions:** words ranked by how much they distinguish the suggested class from the runner-up.
- **Related issue search:** TF-IDF weighted cosine similarity against the labeled examples.
- **Human feedback loop:** label corrections immediately retrain the model and persist in your browser's local storage.
- **Batch analysis:** upload a CSV with title and description columns, then export predicted categories, model fit, review flags and suggested priorities.
- **No backend or API keys:** the issue text stays in your browser.

## Run locally

1. Download the project from GitHub.
2. Open the index.html file in Chrome, Edge or Firefox.
3. Try an example and press **Analyze issue**.

No Python installation, npm, terminal commands, accounts, or dependencies required.

## What is actually AI?

The issue category comes from a locally trained **Multinomial Naive Bayes** classifier implemented in plain JavaScript.

1. Split the issue title and description into tokens, removing common stop words.
2. Give title words double weight.
3. Learn how often each word appears in examples of Bug, Feature, Documentation, and Question.
4. Score an incoming issue against all four categories using smoothed log-likelihoods.
5. Show the winning class, an uncalibrated relative-fit measure, and its most distinctive learned terms.

Similar reports are ranked with **TF-IDF cosine similarity**. The P1/P2/P3 priority suggestion is a **separate keyword rule**, not part of the ML model.

## Batch CSV example

The first row must contain the headers: title,description

Example:

    title,description
    "Dashboard crashes","Importing an empty CSV causes an exception."
    "Add keyboard shortcuts","Support Ctrl+K for searching."

Up to 500 rows and 1 MB per uploaded file. CSV stays on the current device.

## Learning and privacy

Only issues that you explicitly save as feedback are persisted in browser storage. You can export those examples as JSON or reset them. If you clear your site's local storage, saved feedback is also deleted. Input issues are not sent to external services.

## Limitations

This is a **learning and portfolio prototype**, not a production incident-management product. Starter data is small, hand-written and English-only; accuracy is not benchmarked. Relative model fit is **not a calibrated probability**. Text similarity does not establish whether issues are duplicates. Priority rules can be incorrect or miss emergencies. A human should assess all consequential decisions, particularly security and incidents.

## Built with

HTML, CSS, vanilla JavaScript, Multinomial Naive Bayes, TF-IDF, LocalStorage, the Browser File API.

## Possible next improvements

- Evaluate with separate held-out test issues and show a confusion matrix.
- Enable optional imports of public GitHub issues with user permission.
- Add portable dataset import, multilingual tokenization, and model comparison.
- Improve low-confidence escalation with a measured validation dataset.

---

RepoSense AI is a local-first, explainable AI experiment designed for developer portfolios.