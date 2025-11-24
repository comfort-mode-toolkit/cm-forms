# cm-forms 📝

> You build the form. We make it accessible.

Ever spent hours coding a perfect signup form, only to realize screen readers can't understand it? Yeah, that's frustrating.

## The Problem

Forms are everywhere - logins, checkouts, contact pages, surveys. But most forms create accessibility barriers:
- Inputs without proper labels
- Buttons that just say "Submit" (submit what?)
- Error messages that aren't linked to the fields
- Required fields with no indication they're required

When the structure isn't there, screen reader users have to fill in the gaps. That's not okay.

## The Solution

cm-forms is like [Black](https://github.com/psf/black) for HTML forms. Point it at your HTML files, and it automatically adds the accessibility attributes everyone needs.

Note: This isn't an all in one solution. It's a tool to help you make your forms accessible. You still need to test them with screen readers and make sure they work for everyone.

```bash
cm-forms signup.html
```

```

NOTICE: This is a pre-alpha planning release (v0.0.1). No guarantees, minimal features live. Visit https://github.com/comfort-mode-toolkit/cm-forms/ to contribute or share feedback.

Processed: signup.html -> signup_cm.html
- Added label to <input id="username">
- Added label to <input id="email">
- Added aria-required="true" to <input id="email">
- Added aria-required="true" to <input id="password">
- WARNING: <button> label "Submit" is ambiguous, developer review needed

For more info and feedback, visit: https://github.com/comfort-mode-toolkit/cm-forms/
```

That's it. Seriously.

## What It Does

- Finds all forms in your HTML files
- Adds ARIA labels, roles, and required attributes automatically
- Asks you when things are ambiguous (we can't read your mind!)
- Explains what changed and why
- Makes your forms work for everyone

Think of it as a helpful friend who knows WCAG guidelines and saves you hours of tedious work.

## Current Status

**🔬 Research Phase**

We're figuring out the best way to build this. What we're exploring:
- Which fixes are always safe to auto-apply
- When we should ask instead of assuming
- How to explain accessibility without overwhelming people
- What forms need most in real projects

## Want to Help? Go Down the Rabbit Hole

We need people to research and document **what makes forms accessible**. Not theory - practical stuff.

**What we're looking for:**

- **Best practices**: What should every form have? (real examples, not just "add labels")
- **Risk areas**: When could auto-fixing break things or make wrong assumptions?
- **Edge cases**: Multi-step forms, dynamic forms, custom controls - what's tricky?
- **Testing insights**: How do screen reader users actually interact with forms?
- **Pattern library**: What are the correct ARIA patterns for different form types?

**How to contribute:**

Dive into HTML form accessibility. Read the specs, test with screen readers, find real broken forms and document what they need. Write it in plain language.

Check out our [research wiki](https://comfort-mode-toolkit.github.io/wiki/research/intro/) to see how to submit your findings. No expertise required - if you can spot a problem and explain how to fix it, that helps.

GitHub issues, wiki edits, random notes in a text file - all welcome.

## why forms?

Forms are everywhere. Login pages, checkouts, contact forms, surveys. When forms have accessibility barriers, people get locked out of important things.

Good news: form accessibility has clear patterns. Bad news: doing it manually is tedious and easy to mess up.

Let's automate the tedious parts.

## part of comfort mode toolkit

cm-forms is part of the [comfort mode toolkit](https://github.com/comfort-mode-toolkit) – tools that make the web more comfortable for everyone.

---

*Simple tools for a more accessible web.*
