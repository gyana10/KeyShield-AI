# KeyShield AI
Problem Statement
Traditional authentication only checks:

Username
Password

If someone knows your password,

they can login.

Our project asks

"Does the person typing behave like the real owner?"

That's the entire project.

Simple.

Clear.

Industry relevant.
## Enterprise Behavioral Authentication & Analytics Platform
Problem 1: The dataset isn't an authentication dataset

The DSL-StrongPassword dataset is not labeled as Genuine vs Suspicious.

It contains genuine typing samples from 51 users.

So we cannot simply train:

Features → Genuine / Suspicious

because those labels don't exist.

Our solution

We'll generate authentication scenarios.

Genuine Authentication

Claimed User = Actual User

Example:

Claimed User	Typing Sample	Label
User_05	User_05 Sample 132	Genuine
Suspicious Authentication

Claimed User ≠ Actual User

Example:

Claimed User	Typing Sample	Label
User_05	User_18 Sample 42	Suspicious

This is how we'll create a balanced authentication dataset.

Problem 2: Typing changes over time

This is an even bigger issue.

A person never types exactly the same way twice.

Typing changes because of:

Fatigue
Mood
Keyboard
Laptop
Sitting position
Speed
Practice
Time of day

If our model expects identical typing, it'll reject the real user.

That's bad authentication.

So what should we do?

We build a Behavioral Profile, not a fixed pattern.

Instead of learning:

Hold Time = 94 ms

the model learns something like:

Hold Time

Mean = 94 ms

Normal Range = 88–100 ms

Now if the user types:

92 ms

Still genuine.

97 ms

Still genuine.

95 ms

Still genuine.

But:

145 ms

Probably suspicious.

This is much closer to how real behavioral biometric systems work.

Enrollment becomes very important

Instead of asking the user to type one paragraph, we'll ask them to type five different paragraphs.

Example:

Paragraph 1

↓

Paragraph 2

↓

Paragraph 3

↓

Paragraph 4

↓

Paragraph 5

Now we capture natural variation.

That becomes the user's behavioral profile.

Authentication

Later,

the user types one new random paragraph.

The model asks:

Does this typing behavior fall within the user's normal behavioral range?

If yes:

✅ Genuine

If not:

⚠ Suspicious

We also need paragraph diversity

If the user always types the same sentence:

The quick brown fox...

the model may partially learn the text instead of the behavior.

Instead, we'll maintain a library of many paragraphs.

Example:

Paragraph A

Paragraph B

Paragraph C

Paragraph D

...

Enrollment uses multiple paragraphs.

Authentication uses a different random paragraph.

This makes the model focus on typing rhythm, not memorized text.

Dataset Generation Strategy

I think we should build the dataset like this:

Stage 1 — Original Data
20,400 genuine typing samples

↓

Stage 2 — Enrollment

For each user:

Select a portion of their sessions to build the behavioral profile.

↓

Stage 3 — Authentication

Use the remaining genuine sessions as genuine login attempts.

↓

Stage 4 — Impostor Attempts

Use samples from other users while pretending they belong to the enrolled user.

↓

Stage 5 — Final Dataset
Enrollment Data

+

Genuine Authentication

+

Suspicious Authentication

Balanced.

Realistic.

Interview-worthy.

One thing I DON'T want to do

I do not want to create fake feature values using random numbers.

That would weaken the credibility of the project.

Instead, we'll use real human typing data to generate authentication events.

The realism comes from combining genuine user samples and impostor samples—not inventing arbitrary keystroke timings.

💡 I have one more idea

This could become the best part of the entire project.

Instead of training the model on individual typing samples, we'll train it on similarity to the enrolled profile.

Imagine this:

Enrollment Profile:

Average Hold Time
Average Flight Time
Average Typing Speed
Average Error Rate
...

New Authentication:

Current Hold Time
Current Flight Time
Current Typing Speed
...

Then we create comparison features such as:

Difference in average hold time
Difference in flight time
Difference in typing speed
Difference in pause duration

The ML model learns:

"How close is this typing session to the enrolled user's normal behavior?"

This is much closer to how real behavioral authentication systems work than simply classifying raw feature vectors.

⭐ I think this should become the heart of KeyShield AI.

Instead of saying:

"I trained a model on a keystroke dataset."

You'll be able to say:

"I designed a behavioral profile–based authentication system. Each user is enrolled through multiple typing sessions to establish a statistical typing profile. Authentication attempts are evaluated by comparing new typing behavior against this profile, and the machine learning model classifies whether the observed behavior is consistent with the enrolled user's historical typing patterns."

---

# Project Vision

KeyShield AI is an enterprise-grade behavioral biometric authentication platform that verifies a user's identity based on their unique typing behavior. Unlike traditional authentication systems that rely solely on passwords, KeyShield AI continuously analyzes keystroke dynamics to determine whether the current user matches their enrolled behavioral profile.

The platform combines Data Engineering, Machine Learning, Explainable AI (XAI), and Full-Stack Development to deliver a secure, intelligent, and explainable authentication experience.

---

# Problem Statement

Traditional password-based authentication is vulnerable to several security risks:

- Password theft
- Credential sharing
- Brute-force attacks
- Social engineering
- Password reuse

Even if an attacker knows the correct password, they cannot easily replicate the legitimate user's typing behavior.

KeyShield AI introduces behavioral biometrics as an additional authentication layer by analyzing how a user types rather than only what they type.

---

# Proposed Solution

The system authenticates users through a Behavioral Verification Challenge.

During enrollment, users complete multiple typing sessions to create a personalized behavioral profile.

During authentication, users type a randomly selected paragraph while the system captures raw keyboard events such as key press time, key release time, typing speed, and typing rhythm.

The captured data is processed through an ensemble machine learning model that determines whether the typing behavior belongs to the enrolled user.

The prediction is accompanied by Explainable AI (XAI), allowing users and administrators to understand why a decision was made.

All authentication events are stored inside a PostgreSQL Data Warehouse for reporting and analytics.

---

# Objectives

- Build an enterprise-grade behavioral authentication platform.
- Capture raw keystroke events from users in real time.
- Generate behavioral features using feature engineering.
- Authenticate users using an ensemble machine learning model.
- Provide Explainable AI (XAI) for every authentication decision.
- Design and implement an ETL pipeline.
- Build a PostgreSQL Data Warehouse with Raw, Staging, and Analytics layers.
- Develop a modern React dashboard for monitoring authentication activities.
- Deploy the complete application using free cloud platforms.

---

# Key Features

## User Management

- User Registration
- User Login
- Behavioral Enrollment
- User Profile Management

---

## Behavioral Verification Challenge

- Random typing passages
- Real-time keystroke capture
- Live typing statistics
- Enrollment sessions
- Authentication sessions

---

## Machine Learning Engine

- Feature Engineering
- Random Forest
- Support Vector Machine
- Logistic Regression
- Stacking Ensemble Model

---

## Explainable AI

- SHAP-based prediction explanations
- Feature importance visualization
- Authentication confidence
- Model contribution analysis

---

## Data Engineering

- ETL Pipeline
- Data Validation
- Data Cleaning
- Feature Transformation
- PostgreSQL Data Warehouse

---

## Analytics Dashboard

- Authentication Trends
- Genuine vs Suspicious Users
- User Statistics
- Typing Metrics
- Model Performance
- Authentication History

---

# System Workflow

User Registration

↓

Behavioral Enrollment

↓

Behavioral Profile Creation

↓

Behavioral Verification Challenge

↓

Feature Extraction

↓

Machine Learning Authentication

↓

Explainable AI

↓

Authentication Result

↓

Store Authentication Event

↓

Analytics Dashboard

---

# Expected Outcomes

- Real-time behavioral authentication.
- Explainable authentication decisions.
- Enterprise-level analytics dashboard.
- Production-ready REST API.
- Modern responsive web application.
- Complete end-to-end AI application demonstrating Data Engineering, Machine Learning, Explainable AI, Backend Development, Frontend Development, and Cloud Deployment.

---

# Technologies

## Frontend

- React
- Vite
- Tailwind CSS
- React Router
- Axios
- Recharts
- Framer Motion

## Backend

- FastAPI
- Pydantic
- Uvicorn

## Machine Learning

- Scikit-learn
- Random Forest
- Support Vector Machine
- Logistic Regression
- Stacking Ensemble

## Explainable AI

- SHAP

## Data Engineering

- Python
- SQL
- PostgreSQL
- ETL Pipelines

## Deployment

- Vercel
- Render
- Neon PostgreSQL

## Version Control

- Git
- GitHub

---

# Future Enhancements

- Continuous Behavioral Authentication
- Risk-Based Authentication
- Multi-Factor Authentication
- Mobile Device Support
- Cloud Monitoring
- Admin Portal
- User Behavior Analytics
- Security Alerts