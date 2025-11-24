====================================================================
Accessible Forms: A WCAG and ARIA Developer Bible (cm-forms Brief)
====================================================================

.. contents:: Table of Contents
   :depth: 2

Introduction
============

This document offers a rigorous, research-backed brief for developers responsible for form accessibility tooling. Scope: **Standard forms** (login, registration, contact, survey, etc.)—the atomic, everyday interactions of the web.

Goals are to:

- Define all relevant WCAG requirements and best practices for basic forms.
- Document all safe and unsafe automation opportunities ("must/must not automate") with explicit programmatic boundaries.
- Enumerate every ARIA/form pattern that the cm-forms library can and should address, as well as patterns to avoid.
- Provide neutral rationale with full citations, footnotes (Sphinx numbered syntax), and sidenotes for margin notes.

For multi-step/dynamic forms, only minimal context is included to clarify the boundaries; core rules apply to every input-label pair.


Section I: Anatomy of a Standard Accessible Form
===============================================

A standard form is a sequence of input controls—textboxes, radio buttons, select menus, checkboxes, buttons—each with programmatically linked, clear, persistent labels.[^deque-form-tutorial]_ The **core atoms** are:

- Inputs (e.g., `<input>`, `<textarea>`, `<select>`, `<button>`)
- Explicit, always-visible text labels (`<label for="id">`)
- Optional: groupings (`<fieldset>` / `<legend>`), instructions, help text
- Accessible submit/cancel buttons (text-only, never icon-only)

Roles:

- Each field must be uniquely identified for both sighted users and assistive technologies.
- Required/optional status and errors must be communicated both visually and programmatically.[^deque-form-labels]_ Labels must be unique, descriptive, and persistently visible—not obscured or replaced by placeholder text.|sidenote1|

.. |sidenote1| note:: Placeholders are transient hints and disappear on typing; they must never be the sole identifier for a field.[^placeholders]_ Screen readers and users with cognitive disabilities can lose context without a true label. (See below for patterns.)

Core WCAG Success Criteria (atomic forms):

- **1.3.1 Info and Relationships:** Inputs must be programmatically linked to their labels (using native HTML or ARIA-labelling patterns).
- **2.4.3 Focus Order:** Keyboard navigation order matches visual layout; tabbing never jumps illogically.[^wcag-243-focus]_ (Test with real keyboards.)
- **3.3.1 Error Identification:** If a field is invalid/missing, communicate this clearly (ARIA, error text, and linkage).
- **3.3.2 Labels or Instructions:** Every input control has meaningful persistent label and, if necessary, instructions.[^wcag-332-labels]_ (Ambiguity is a user barrier.)
- **3.3.3 Error Suggestion:** If errors can be automatically detected, propose meaningful fixes ("Enter an email address, e.g.").
- **4.1.2 Name, Role, Value:** All interactive elements expose name, role, value to assistive tech.
- **1.3.5 Identify Input Purpose (WCAG 2.1/2.2):** Use autocomplete attributes for recognized purposes (name, email, tel, etc.).|sidenote2|

.. |sidenote2| note:: WCAG 2.1/2.2 requires `autocomplete` for standard personal info fields—"given-name", "email", etc.—so browsers and ATs can present icons/tools.[^wcag-135-input-purpose]_

Section II: Patterns for Safe Automation
=======================================

**What Can Be Safely Automated:**

The following atomic patterns are stable, universal, and safe for automation, provided correct heuristics and context:

- **Label-Linking:** Connect `<label for="id">` with `<input id="id">`; verify the association exists and isn’t duplicated.[^deque-form-labels]_ For non-native/cases, use ARIA labeling (`aria-label`, `aria-labelledby`).
- **Groupings:** Group related controls with `<fieldset>` / `<legend>` for semantic relationships (e.g., radio sets); can be safely added if group detected.|sidenote3|
- **Required Fields:** Add `aria-required="true"` in addition to native `required`; visually mark required fields (e.g., asterisk), but do not rely solely on color.[^tpgi-required]_ Automation can add ARIA on fields with `required` attribute.
- **Autocomplete:** Set appropriate `autocomplete` attribute for recognized field types per WCAG 2.1/2.2 (see official taxonomy).[^
wcag-135-input-purpose]_ (e.g., email, given-name, family-name, tel, etc.)
- **Error Messaging:** Link error message text with its invalid field using `aria-describedby`, and mark invalid fields with `aria-invalid="true"` after validation. Error messages should be actionable, not generic.[^aria-invalid-wai]_ Automation may not produce error logic but can link messages programmatically.
- **Button Text:** Flag buttons with vague text like "Submit" or "OK" for developer intervention; can’t safely rewrite button labels automatically as intent is not programmatically determinable.[^stanford-meaningful-button]_ (Prompt, do not auto-fix.)
- **Focus Management:** Preserve tab order to match visual flow; automation may warn on illogical tabindex but should never generate or reorder tabindex except in trivial cases.[^deque-accessibility-checklist]_ Tabbing order and focus indicators MUST reflect logical sequence, but choosing specific order is a manual design decision.

.. |sidenote3| note:: When grouping fails (no `<fieldset>` or `<legend>`), programmatic roles/`aria-describedby` can supplement for AT, but native elements always preferred for broad AT compatibility.[^adg-fieldset-grouping]_

**What Must NOT Be Automated or Should Only Be Warned About:**

These require user judgment, contextual domain knowledge, or human review—any automation risks user confusion or broken semantics.

- **Ambiguous/Non-Descriptive Button & Field Labels:** Cannot safely rewrite button label "Submit" to "Subscribe" or "Create Account"; developer must define meaning.[^stanford-meaningful-button]_
- **Instruction/Help Text Placement or Content:** Automated placement may align visually but not logically; custom instructions often domain-specific.
- **Complex Validation Logic:** Error recognition and suggestion for domain logic (e.g., password rules) must be outlined by developer; only the linkage (aria-describedby) and markup can be automated.
- **Custom Widget Accessibility:** Advanced widgets (datepickers, autocomplete, sliders) require manual ARIA mapping, keyboard support, and testing with AT; core fields only in MVP.[^adg-fieldset-grouping]_
- **Keyboard Trap Prevention:** Detecting/fixing keyboard traps/dysfunction often requires full interface context and user testing; warn only.
- **Dynamic/Multi-Step Form Management:** Detection can warn of multi-step but can’t automate correct announcement, focus management, or step communication without design context.
- **Color Contrast Assessment:** Marking contrast failures can be automated, but correct fix needs visual designer input.[^d11y-placeholder-contrast]_

**Automation Decision Algorithm (for cm-forms):**
- Automate only when context is explicit and deterministic.
- Prompt developer when ambiguity is detected (e.g., label/button not meaningful, multiple `for` attributes, etc.).
- Never overwrite user-provided text; augment or warn only.
- Favor native HTML semantics over ARIA wherever possible.
- Provide always clear explanations for each automated change.|sidenote4|

.. |sidenote4| note:: Every decision should be logged with rationale and change summary, so developers can review and learn as fixes are made. Transparency is key.

Section III: ARIA and Native Semantics for Forms
==============================================

ARIA attributes supplement—but must never substitute for—native HTML. Automation must follow the ARIA Authoring Practices Guide and WCAG techniques.

Core ARIA Patterns (Safe for Automation):

- `aria-label`/`aria-labelledby`: When no native label, provide accessible naming.
- `aria-describedby`: Links help/error messages to fields.
- `aria-required`: Indicates required field (always supplement visually, as ARIA is for AT).
- `aria-invalid`: Marks field invalid **only after failed validation**; should not be present before validation step.[^aria-invalid-wai]_

Unsafe ARIA Application:

- ARIA alone must not replace label, legend, or group semantics if native elements can do the job.[^adg-fieldset-grouping]_
- Excess/duplicate ARIA attributes can cause confusion for AT users; must be programmatically minimal and only where required.

**Native Semantics First:**
- Use `<label>`, `<fieldset>`, `<legend>`, `<button>`—not only ARIA markup.
- Any automation must preserve user markup; never remove or override explicit semantics except to correct broken programmatic links.

Section IV: Real-World Form Example (Atomic Patterns Only)
==========================================================

.. code-block:: html

    <form>
        <fieldset>
            <legend>Personal Info</legend>
            <label for="fullname">Full Name</label>
            <input type="text" id="fullname" name="fullname" autocomplete="name" required aria-required="true">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" autocomplete="email" required aria-required="true">
        </fieldset>
        <button type="submit">Sign Up</button>
    </form>

- Each input has an explicit `<label>` and an appropriate `autocomplete` attribute.
- Required fields are visually marked and programmatically announced.
- Buttons have meaningful text linked to the action.
- Grouping is semantically clear via `<fieldset>`/`<legend>`.

Section V: Edge Cases, Warning Patterns, and MVP Scope
=====================================================

- **Edge Case:** Field label is missing; automation can insert, but must report for human review.
- **Edge Case:** Multiple inputs with same label or ambiguous label detected; warn, do not fix.
- **Warning:** Placeholder is used as label; can insert label, but must not remove developer intent without audit.
- **Warning:** Button text unclear; flag but never rewrite.
- **Scope out:** Custom widgets, validation beyond markup, multi-step/nested forms; warn only for future coverage.

**Minimum Viable Product (MVP) Scope for cm-forms:**
- Label-linking for `<label>`/`<input>` and `<fieldset>`/`<legend>`
- ARIA patterns: `aria-label`, `aria-labelledby`, `aria-required`, `aria-describedby`, `aria-invalid` (only for validated errors)
- `autocomplete` attribute for recognized standard fields
- Visual and programmatic required indicators
- Error linkage via ARIA
- Programmatic group/legend repair
- Comprehensive logging and change explanation

Section VI: Non-Atomic Forms and Algorithmic Boundaries
=======================================================

For dynamic, multi-step, or custom control forms:
- Automation may only warn/report, as correct accessible patterns require live context, visual audit, and human testing.|sidenote5|
- Algorithm should never make irreversible changes; must always favor user review and clarity.

.. |sidenote5| note:: Multi-step forms usually require progress indication and focus/announcement management. These are out of scope for safe automation except for basic grouping.


Glossary
========

:ARIA: Accessible Rich Internet Applications; HTML attributes for marking up roles/states/labels for assistive tech.
:WCAG: Web Content Accessibility Guidelines
:Fieldset/Legend: Native HTML tags to group related controls and give semantic headings.
:Autocomplete: Attribute to define purpose of input fields ("given-name", "email", etc.) for browser autofill and AT.[^wcag-135-input-purpose]_
:Label-Linking: Connecting visible text label to HTML input for programmatic identification.
:ARIA-Invalid: Attribute that, when set to "true" on a field, makes AT announce "invalid" status.

References (Numbered Footnotes)
===============================

.. [^deque-form-tutorial] W3C WAI, Forms Tutorial, https://www.w3.org/WAI/tutorials/forms/
.. [^deque-form-labels] Deque University, Inputs/Labels Checklists, https://dequeuniversity.com/checklists/web/form-input-labels-instructions
.. [^placeholders] BrowserStack, The Problem with Placeholders, https://www.browserstack.com/guide/input-placeholder
.. [^wcag-243-focus] Stark, WCAG Focus Order Explained, https://www.getstark.co/wcag-explained/operable/navigable/focus-order/
.. [^wcag-332-labels] WCAG.com, Understanding Labels and Instructions, https://www.wcag.com/developers/3-3-2-labels-instructions/
.. [^wcag-135-input-purpose] W3.org, SC 1.3.5: Identify Input Purpose, https://www.w3.org/WAI/WCAG21/Understanding/identify-input-purpose.html
.. [^tpgi-required] TPGi, Required Attribute Requirements, https://www.tpgi.com/required-attribute-requirements/
.. [^aria-invalid-wai] W3C WAI, ARIA21: Using aria-invalid, https://www.w3.org/WAI/WCAG21/Techniques/aria/ARIA21
.. [^stanford-meaningful-button] Stanford University, Meaningful Links and Buttons, https://uit.stanford.edu/accessibility/testing/links-and-buttons
.. [^deque-accessibility-checklist] Deque University, Web Accessibility Checklist, https://dequeuniversity.com/checklists/web-accessibility-checklist
.. [^adg-fieldset-grouping] Accessibility Developer Guide, Grouping Controls Fieldset, https://www.accessibility-developer-guide.com/examples/forms/grouping-with-fieldset-legend/
.. [^d11y-placeholder-contrast] Digital A11y, Placeholder Mirage, https://www.digitala11y.com/anatomy-of-accessible-forms-placeholder-is-a-mirage/
