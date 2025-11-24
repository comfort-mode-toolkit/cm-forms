# Project Brief: cm-forms (Automated Form Accessibility Remediation)

**Status:** Draft
**Authors:** R&D Team
**Date:** 2025-11-23
**Objective:** Architect and build a Python library to automatically detect and safely remediate accessibility violations in HTML forms.

---

## 1. Executive Summary

The "Form Accessibility Crisis" is well-documented (`why.md`). Manual remediation is slow, error-prone, and expensive. `cm-forms` aims to be the **"Prettier for Accessibility"**—a tool that developers can trust to automatically fix common, high-impact accessibility issues in their HTML forms without breaking functionality or styling.

**Key Value Proposition:**
*   **Automated Compliance:** Instantly fix 60-70% of WCAG form failures (labels, required attributes, error linking).
*   **Safety First:** Zero-tolerance for breaking existing JS/CSS. "Do no harm" is the primary directive.
*   **Educational:** The tool explains *why* it made a change, upskilling developers.

---

## 2. Architectural Decisions & Technical Strategy

### 2.1. The Parser Problem: `lxml` vs. `html.parser` vs. CST

**The Challenge:** Standard HTML parsers (like `BeautifulSoup`'s default) are destructive. They normalize whitespace, strip comments, and reorder attributes. For a "linter/fixer" tool, **preserving the original code structure is non-negotiable.** If we reformat the user's entire file, they will reject the tool.

**Options Analysis:**
1.  **`BeautifulSoup` (default):** Easy to use, but destructive to whitespace.
2.  **`lxml`:** Fast, but can be aggressive with "correcting" malformed HTML (which we might not want to touch).
3.  **`html.parser`:** Slower, but more lenient.
4.  **Concrete Syntax Tree (CST) Approach:** Treating HTML as a token stream rather than a DOM.

**Decision:** **Hybrid Approach using `BeautifulSoup` with Custom Output Formatting.**
*   **Why:** Building a full HTML CST parser from scratch is over-engineering for MVP. `BeautifulSoup` is robust enough *if* we control the output.
*   **Implementation:** We will use `bs4` with `html.parser` backend. We will implement a custom `Formatter` class to ensure that untouched nodes are serialized exactly as they were input (preserving indentation where possible).
*   **Risk:** Some minor whitespace shifts are inevitable. We must communicate this as "standardization" (like `black` or `prettier`).

### 2.2. The "SafeDOM" Safety Layer

**The Problem:** Modifying the DOM blindly can break JavaScript event listeners (e.g., changing an ID that JS relies on) or CSS selectors.

**Solution:** The `SafeDOM` Wrapper.
We will not manipulate `bs4` objects directly in the remediation logic. Instead, we wrap them in a `SafeDOM` API that enforces safety checks.

**Safety Rules:**
1.  **Immutable IDs (mostly):** Never change an existing `id` unless explicitly authorized by the user. Only generate *new* IDs for elements that lack them.
2.  **Namespace Protection:** All generated IDs and classes must use a prefix (e.g., `cm-a11y-`) to avoid collisions with user code.
3.  **Attribute Preservation:** Never remove unknown attributes (e.g., `data-react-id`, `ng-model`).

### 2.3. Architecture Components

1.  **`Parser`**: Ingests HTML, produces a DOM.
2.  **`Analyzer`**: Runs `Rules` against the DOM. Produces `Issues`.
3.  **`Rules Engine`**:
    *   **Detection Logic**: "Is this input missing a label?"
    *   **Fix Logic**: "Create a label with `for=id`."
    *   **Confidence Score**: 0.0 to 1.0.
4.  **`Remediator`**: Applies fixes based on `Issues`.
    *   **Auto-Fix**: Confidence > 0.9 (e.g., `required` -> `aria-required`).
    *   **Prompt**: Confidence 0.5 - 0.9 (e.g., "Is 'Submit' the best label for this button?").
    *   **Report**: Confidence < 0.5 (e.g., "Complex custom widget detected, please review manually").
5.  **`Reporter`**: Outputs results (CLI, JSON, HTML).

---

## 3. Form Patterns & Heuristics

We need to identify *types* of forms to apply context-aware fixes.

### 3.1. Taxonomy of Common Forms

| Pattern | Key Characteristics | Critical A11y Requirements |
| :--- | :--- | :--- |
| **Login** | `user`/`email` + `password` + `submit` | `autocomplete` attributes are critical. |
| **Registration** | Multiple text inputs, `password` confirmation | Error message linking (`aria-describedby`) is paramount. |
| **Search** | Single input + button (often icon-only) | Input needs `aria-label` (often visually hidden label). |
| **Checkout** | Address fields, Credit Card | Grouping (`fieldset`/`legend`) for related fields. |
| **Contact** | Name, Email, Textarea | `aria-required` for mandatory fields. |

### 3.2. Detection Heuristics

How do we know it's a "Login Form"?
*   **Heuristic:** `<form>` contains `<input type="password">` AND (`<input type="text">` OR `<input type="email">`).
*   **Action:** If detected, ensure `autocomplete="username"` and `autocomplete="current-password"` are suggested.

### 3.3. The "Label Hunter" Algorithm

The most common failure is missing labels. How do we fix it safely?

**Algorithm:**
1.  **Check Explicit:** Does `<input>` have `id`? Is there a `<label for="id">`? -> **OK**.
2.  **Check Implicit:** Is `<input>` inside a `<label>`? -> **OK**.
3.  **Check `aria-label`:** Does it have `aria-label` or `aria-labelledby`? -> **OK**.
4.  **Hunt for Text:**
    *   Scan previous sibling. Is it a text node? (e.g., `Name: <input>`)
    *   Scan parent's previous sibling.
    *   **If found:** Wrap text in `<label>` (if safe) OR add `id` to input and `for` to a new `<label>` around the text.
    *   **Risk:** We might grab "Please enter your" as the label instead of "Name".
    *   **Mitigation:** Only auto-fix if the text is short (< 5 words) and close to the input. Otherwise, **Prompt User**.

---

## 4. Risks & Mitigation Strategies

### Risk 1: Breaking JavaScript Event Listeners
*   **Scenario:** User has `$('#submit-btn').on('click', ...)` and we change the ID.
*   **Mitigation:** **NEVER change existing IDs.** We only *add* IDs to elements that don't have them (e.g., for `aria-describedby` targets).
*   **Generated ID Pattern:** `cm-{hash(content)}-{random}`.

### Risk 2: CSS Layout Breakage
*   **Scenario:** We wrap a text node in a `<label>` tag, and the user's CSS selector `div > text` stops working, or flexbox layout shifts.
*   **Mitigation:**
    *   Prefer `aria-labelledby` over wrapping in `<label>` if structure is complex.
    *   If we *must* insert a tag, try to use `display: contents` in a companion CSS file (if we were injecting CSS, which we aren't yet).
    *   **Better approach:** Use `for`/`id` association which doesn't require nesting changes.

### Risk 3: "Fixing" Intentional Patterns
*   **Scenario:** Developer used a custom accessible widget pattern that our tool doesn't recognize, and we try to "fix" it, breaking the ARIA interaction.
*   **Mitigation:**
    *   **Ignore List:** Support `<!-- cm-ignore -->` comments.
    *   **Conservative Rules:** If an element already has complex ARIA attributes (`role`, `aria-owns`), **back off**. Assume the developer knows what they are doing.

---

## 5. MVP Roadmap

### Phase 1: The "Safe" Foundation (Weeks 1-2)
*   Implement `SafeDOM` parser/serializer.
*   Verify round-trip fidelity (input HTML == output HTML for no-op).
*   Implement `IDGenerator` (stable, collision-resistant).

### Phase 2: High-Confidence Fixers (Weeks 3-4)
*   **`RequiredFixer`**: `required` -> `aria-required="true"`.
*   **`AutocompleteFixer`**: Suggest `autocomplete` values for common fields (email, name).
*   **`ImgAltFixer`**: `<img src="...">` -> `<img src="..." alt="">` (empty alt for likely decorative images, prompt for others).

### Phase 3: The "Label Hunter" (Weeks 5-6)
*   Implement the heuristic label association.
*   **Interactive Mode:** "I found text 'Email' next to this input. Link them? [Y/n]".

### Phase 4: Error Handling (Weeks 7-8)
*   Detect error message containers (heuristics: `class="error"`, `color: red`).
*   Link them to inputs via `aria-describedby`.

---

## 6. Conclusion

We are building a tool that balances **automation** with **safety**. By focusing on the 80% of common, repetitive accessibility tasks (labels, attributes), we free up developers to focus on the 20% of complex, interactive accessibility challenges. The architecture is designed to be defensive—preserving user intent and code structure above all else.
