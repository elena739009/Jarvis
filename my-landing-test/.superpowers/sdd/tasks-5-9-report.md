# Tasks 5-9 Review Report

**Reviewer:** Claude Code  
**Reviewed:** Tasks 5–9 diff + index.html lines 942–1296

---

## Summary

Task 5 — Spec ✅ | Quality: Approved  
Task 6 — Spec ✅ | Quality: Approved  
Task 7 — Spec ✅ | Quality: Approved  
Task 8 — Spec ✅ | Quality: Approved  
Task 9 — Spec ✅ | Quality: Approved  

---

## Per-task verification

### Task 5 — Services (lines 942–993)
- `<section id="services">` present after `#problem` ✅
- 3 `<article class="service-card">` elements ✅
- Card 2: `.service-card--featured` + `.service-badge` "Популярно" ✅
- Prices: `от 5 000 ₽` / `от 3 000 ₽` / `от 15 000 ₽` in `.service-price` ✅
- All 3 service CTAs `href="#contact"` ✅
- CSS: 3-column grid (`repeat(3, 1fr)`), collapses to 1 column at `≤900px` ✅
- `.service-list li::before { content: '✓'; color: var(--accent-3) }` ✅

### Task 6 — Works (lines 995–1037)
- `<section id="works">` present after `#services` ✅
- 2 `<article class="work-card">` elements ✅
- Tag "Демо-проект" with `.tag--purple` on card 1 ✅
- Tag "Концепт" with `.tag--green` on card 2 ✅
- `.works-disclaimer` paragraph containing "учебные работы" ✅
- CSS: 2-column grid, 1-column at `≤768px` ✅
- `.work-preview` height `220px` with gradient backgrounds (purple + coral) ✅

### Task 7 — Process (lines 1039–1083)
- `<section id="process">` present after `#works` ✅
- 4 `.process-step` divs with numbers 01–04 ✅
- `.process-steps::before` uses `repeating-linear-gradient` dashed connector ✅
- Each `.step-result` starts with "→" ✅
- `.step-result { color: var(--accent-3) }` ✅
- Mobile `≤900px`: 1-column vertical layout with side connector line ✅

### Task 8 — Trust (lines 1085–1126)
- `<section id="trust">` present after `#process` ✅
- 4 `.trust-card` divs: 📋 Договор, 💳 Поэтапная оплата, ✏️ Правки включены, 🎓 Обучение ✅
- All trust icons have `aria-hidden="true"` ✅
- `.trust-stats` with 3 stats: `2` / `100%` / `~1 ч` (with labels "проекта создано", "сдано в срок", "время ответа") ✅
- `.stat-num { color: var(--accent); font-family: 'Bricolage Grotesque' }` ✅

### Task 9 — Contact + Footer + Utilities (lines 1128–1203)
- `<section id="contact">` present after `#trust` ✅
- Form `action="https://formspree.io/f/ЗАМЕНИ_НА_СВОЙ_ID"` (correct placeholder) ✅
- Exactly 3 fields: `name` (text), `contact` (text), `message` (textarea) ✅
- `.form-success` and `.form-error` both have `aria-live="polite"` and `hidden` attr ✅
- Submit button has classes `.btn.btn-primary.form-submit` ✅
- Telegram `href="https://t.me/elena_morozova_5555"` with `target="_blank" rel="noopener noreferrer"` in contact section ✅
- `</main>` at line 1180, `<footer>` at line 1182 — `</main>` closes BEFORE `<footer>` ✅
- `<footer class="footer">` with logo, "© 2026", Telegram link ✅
- `.back-to-top` button: `aria-label="Вернуться наверх"` and `hidden` attr ✅
- `.mobile-cta` link to `https://t.me/elena_morozova_5555` with `aria-label` ✅
- CSS: `.mobile-cta { display: none }` at `min-width: 769px` (`display: none !important`) ✅
- Touch targets: `input`, `textarea` have `min-height: 44px`; `.back-to-top` is `44×44px` ✅

---

## Issues

### Minor — `back-to-top` `hidden` attribute immediately removed by JS
**Location:** HTML line 1196, JS line 1248  
`<button class="back-to-top" aria-label="Вернуться наверх" hidden>` is correct per spec, but JS immediately runs `backBtn.hidden = false` on page load. Visibility is then controlled exclusively by CSS `opacity: 0` / `.visible` class toggle.  
**Impact:** The spec's `hidden` attr requirement is met at the HTML level (pre-JS state is correct). The JS pattern is intentional and functional — `opacity`+`pointer-events` animate the button in/out while `hidden` would cause a layout jump. No user-facing bug; the approach is acceptable.  
**Recommendation:** No action required. If strict no-JS progressive enhancement is needed, consider removing `backBtn.hidden = false` and relying solely on CSS opacity.

### Minor — Step 04 shares `reveal-delay-3` with step 03
**Location:** Lines 1063 and 1072  
Both `.process-step` divs for steps 03 and 04 use `reveal-delay-3`. Steps should ideally cascade (01→`delay-1`, 02→`delay-2`, 03→`delay-3`, 04→`delay-4`). Not a spec requirement — cosmetic only.  
**Recommendation:** Change step 04's class to `reveal-delay-4` if a `--delay-4` CSS variable is defined, otherwise leave as-is.

### Minor — Inconsistent indentation of `#contact` section
**Location:** Line 1128 vs lines 942/995/1039/1085  
Sections #services through #trust are at column 0 inside `<main>`; `#contact` is indented 4 spaces. All sections are correctly inside `<main>` (verified: `</section>` at 1178, `</main>` at 1180). Purely cosmetic.

---

## Implementation commits

| Task | Commit | Summary |
|------|--------|---------|
| 5 | `3717569` | Services section — three pricing cards (Сайты, Визитка, AI-агент) with featured card badge and hover lift |
| 6 | `7950b76` | Works section — two demo project cards with gradient previews and honest "учебные работы" disclaimer |
| 7 | `d630415` | Process section — 4-step workflow with dashed connector line (horizontal desktop / vertical mobile) |
| 8 | `85db501` | Trust section — 4 guarantee cards + stats counters (2 projects, 100% on time, ~1h response) |
| 9 | `5e1cd64` | Contact section (form + Telegram alt), footer, back-to-top button, mobile sticky CTA; async form submit handler wired in JS |
