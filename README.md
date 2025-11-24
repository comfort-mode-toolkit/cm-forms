# cm-forms

> Catches the mechanical errors so you can focus on the meaningful content.

A tool that fixes what it can verify and warns about what needs your judgment.

## The Problem

Forms lock people out. Missing labels, broken connections, unclear requirements—these aren't just WCAG violations, they're actual barriers to logging in, checking out, getting help, applying for jobs.

The frustrating part? Some of these errors are purely mechanical. A label needs to connect to its input via matching `for` and `id` attributes. That's not subjective—it's either correct or it isn't.

But fixing these mechanical errors manually is tedious, error-prone, and scales poorly when you're maintaining multiple projects.

## What cm-forms Does

cm-forms handles the mechanical parts of form accessibility so you can focus on the parts that actually require your judgment and context.

```bash
cm-forms signup.html
```

```
NOTICE: Pre-alpha planning release (v0.0.1). Minimal features, no guarantees.
Visit https://github.com/comfort-mode-toolkit/cm-forms/ for details.

Processed: signup.html -> signup_cm.html
- Added label to <input id="username">
- Added label to <input id="email">
- Added aria-required="true" to <input id="email">
- Added aria-required="true" to <input id="password">
- WARNING: <button> label "Submit" is ambiguous, developer review needed

For feedback: https://github.com/comfort-mode-toolkit/cm-forms/
```

It catches obvious structural problems and warns you about things that need your attention. That's it.

## What It Actually Fixes

cm-forms only automates things that meet two criteria:
1. Can be verified as 100% correct by reading the code
2. Have zero risk of breaking functionality or making assumptions about context

Currently that means:
- Linking labels to inputs when the connection is unambiguous
- Adding `aria-required` to inputs that already have the `required` attribute
- Flagging generic button text that needs clarification

That's a small list on purpose.

## What It Doesn't Do

cm-forms will never:
- Generate label text from field names (guessing "email_addr" means "Email Address" is making assumptions)
- Write error messages (we don't know your application's tone or what will help your users)
- Modify existing labels (we can't know if you wrote them that way intentionally)
- Promise your form is accessible (structural correctness is necessary but not sufficient)
- Replace testing with actual users

Think of it like a spell checker: it catches "teh" but can't tell you if your sentence makes sense. Useful, but not the whole job.

## Why This Approach?

We've seen accessibility automation that promises the moon and delivers harm. Tools that slap `aria-label="button"` on everything and call it accessible. Overlays that make things worse for the people they claim to help.

We'd rather catch 20% of errors safely than attempt 80% and cause harm.

The philosophy: automate the tedious mechanical stuff, give you clear warnings about judgment calls, and be honest about what requires human context.

## Current Status: Research Phase

Right now cm-forms is in active research. We're figuring out:
- Which form errors can be detected reliably through static analysis
- Which fixes are genuinely safe to automate vs. which require context
- How to communicate uncertainty without overwhelming developers
- What the failure modes of form automation look like

v0.0.1 is intentionally limited. We're starting small and being cautious.

## How to Contribute

We need people with different perspectives:

**Developers:** Test it on real forms. Tell us what breaks, what helps, what's confusing. Run it on open source projects and report findings.

**People who use assistive technology:** Tell us what actually matters. What makes forms unusable vs. just annoying? What warnings would you want developers to see?

**Accessibility professionals:** Tell us where we're being naive. What are we missing? What's dangerous about this approach?

**Researchers:** Help us understand the landscape. What do studies tell us about common form errors? What's evidence vs. speculation?

**Beginners:** Ask questions. If our documentation doesn't make sense, that means it needs work.

### Research We Need

We're documenting what can and cannot be safely automated. This means:
- Finding patterns in real-world forms (both broken and accessible)
- Testing edge cases (dynamic forms, multi-step flows, custom controls)
- Understanding how screen readers interpret different markup patterns
- Identifying where automation typically goes wrong

Check out our [research documentation](https://github.com/comfort-mode-toolkit/cm-forms/blob/main/RESEARCH.md) for current findings and how to contribute.

## Installation

Not ready for production use. If you want to experiment:

```bash
pip install cm-forms  # Coming soon
```

Or clone and install locally:
```bash
git clone https://github.com/comfort-mode-toolkit/cm-forms.git
cd cm-forms
pip install -e .
```

## Why Forms?

Forms are everywhere: logins, checkouts, contact pages, surveys, job applications. When forms have accessibility barriers, people get locked out of essential services.

The good news: form accessibility follows clear patterns. There are mechanical requirements that can be verified.

The bad news: doing it manually is tedious and easy to mess up, especially across multiple projects.

Let's automate the tedious parts so developers can focus on the meaningful parts—like writing labels that actually help people understand what to enter.

## Part of Comfort Mode Toolkit

cm-forms is part of the [Comfort Mode Toolkit](https://github.com/comfort-mode-toolkit)—tools that bridge the gap between wanting to build accessible sites and having the time/expertise to learn every detail of WCAG.

Other tools:
- [cm-colors](https://github.com/comfort-mode-toolkit/cm-colors): You pick your colors, we make them readable

---

**Questions? Concerns? Think we're approaching this wrong?**  
Open an issue. We're trying to figure this out and need honest feedback about what works and what doesn't.

*Building bridges across the accessibility gap—one small, honest tool at a time.*
