# Лендинг «Алё...на!» — План реализации

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Создать одностраничный лендинг-портфолио `index.html` для Елены — специалиста по сайтам, визиткам и AI-агентам — с тёплым игривым стилем, SVG-аватаром и формой заявки.

**Architecture:** Один файл `index.html` с встроенными `<style>` и `<script>`. Семь контентных секций + nav + footer. Анимации — нативный CSS (IntersectionObserver + CSS классы для reveal). Форма — Formspree (static-friendly).

**Tech Stack:** HTML5 семантика, CSS custom properties, Vanilla JS (ES6), Google Fonts (Bricolage Grotesque + Inter), Inline SVG аватар, Formspree для формы.

## Global Constraints

- Один файл: `index.html` — никаких внешних CSS/JS файлов
- Шрифты: Google Fonts через `<link>` с `font-display: swap`
- Цвет акцента (кнопки): `#FF6B6B` (коралловый) — единственный CTA-цвет
- Второй акцент: `#A78BFA` (лавандовый)
- Третий акцент: `#34D399` (мятный) — иконки гарантий
- Фон страницы: `#FFF8F3` (кремовый)
- Telegram: `https://t.me/elena_morozova_5555`
- Все анимации отключаются при `prefers-reduced-motion: reduce`
- Тач-цели ≥ 44×44px
- Семантическая разметка: `<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`
- `<script>` с атрибутом `defer` или в конце `<body>`

---

## Файловая структура

```
my-landing-test/
├── index.html                              ← весь сайт
└── docs/
    └── superpowers/
        ├── specs/2026-06-20-alena-landing-design.md
        └── plans/2026-06-20-alena-landing.md
```

Структура `index.html`:
```html
<head>
  <!-- meta, fonts, <style> -->
</head>
<body>
  <div class="cursor"></div>          <!-- кастомный курсор (десктоп) -->
  <header>
    <nav>...</nav>
  </header>
  <main>
    <section id="hero">...</section>
    <section id="problem">...</section>
    <section id="services">...</section>
    <section id="works">...</section>
    <section id="process">...</section>
    <section id="trust">...</section>
    <section id="contact">...</section>
  </main>
  <footer>...</footer>
  <button class="back-to-top">↑</button>
  <a class="mobile-cta">✈️ Написать Алёне</a>
  <script>...</script>
</body>
```

---

## Task 1: HTML-скелет, мета-теги и CSS-переменные

**Files:**
- Create: `index.html`

**Interfaces:**
- Produces: базовый HTML-документ с CSS custom properties, импортом шрифтов, CSS reset и глобальными стилями

- [ ] **Шаг 1: Создать `index.html` с базовой структурой**

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Алёна — создаю сайты, визитки и AI-агентов под ключ для экспертов и малого бизнеса. Первая консультация бесплатно." />
  <meta property="og:title" content="Алё...на! — Сайты, визитки и AI-агенты" />
  <meta property="og:description" content="Создаю цифровые продукты с душой. Первая консультация бесплатно." />
  <meta property="og:type" content="website" />
  <title>Алё...на! — Сайты, визитки и AI-агенты</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,700;12..96,800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
  <style>
    /* ── CSS Custom Properties ── */
    :root {
      --bg:           #FFF8F3;
      --surface:      #FFFFFF;
      --text:         #1A1A2E;
      --text-muted:   #6B7280;
      --accent:       #FF6B6B;
      --accent-2:     #A78BFA;
      --accent-3:     #34D399;
      --border:       #F0E6DF;
      --shadow:       rgba(255, 107, 107, 0.15);
      --radius:       16px;
      --radius-sm:    8px;
      --transition:   0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);

      --font-hero:    clamp(2.5rem, 6vw, 4.5rem);
      --font-h2:      clamp(1.8rem, 4vw, 2.8rem);
      --font-h3:      clamp(1.1rem, 2vw, 1.4rem);
      --font-body:    1rem;

      --container:    1200px;
      --section-gap:  clamp(5rem, 10vw, 9rem);
    }

    /* ── Reset ── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      font-family: 'Inter', sans-serif;
      font-size: var(--font-body);
      line-height: 1.6;
      color: var(--text);
      background: var(--bg);
      overflow-x: hidden;
    }
    img, svg { display: block; max-width: 100%; }
    a { color: inherit; text-decoration: none; }
    button { cursor: pointer; border: none; background: none; font: inherit; }
    ul { list-style: none; }

    /* ── Container ── */
    .container {
      width: min(var(--container), 100% - 2rem);
      margin-inline: auto;
    }

    /* ── Утилиты ── */
    .section-label {
      font-size: 0.8rem;
      font-weight: 600;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 0.75rem;
    }
    .section-title {
      font-family: 'Bricolage Grotesque', sans-serif;
      font-size: var(--font-h2);
      font-weight: 800;
      line-height: 1.1;
      color: var(--text);
      margin-bottom: 1rem;
    }
    .accent { color: var(--accent); }
    .accent-2 { color: var(--accent-2); }

    /* ── Кнопки ── */
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.85rem 1.75rem;
      border-radius: 50px;
      font-weight: 600;
      font-size: 1rem;
      transition: var(--transition);
      min-height: 44px;
    }
    .btn-primary {
      background: var(--accent);
      color: #fff;
      box-shadow: 0 4px 20px var(--shadow);
    }
    .btn-primary:hover {
      background: #ff5252;
      transform: translateY(-2px);
      box-shadow: 0 8px 30px var(--shadow);
    }
    .btn-outline {
      border: 2px solid var(--accent);
      color: var(--accent);
      background: transparent;
    }
    .btn-outline:hover {
      background: var(--accent);
      color: #fff;
      transform: translateY(-2px);
    }

    /* ── Reveal-анимации ── */
    .reveal {
      opacity: 0;
      transform: translateY(30px);
      transition: opacity 0.6s ease, transform 0.6s ease;
    }
    .reveal.visible {
      opacity: 1;
      transform: translateY(0);
    }
    .reveal-delay-1 { transition-delay: 0.1s; }
    .reveal-delay-2 { transition-delay: 0.2s; }
    .reveal-delay-3 { transition-delay: 0.3s; }

    /* ── Пульс на hero CTA ── */
@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 4px 20px var(--shadow); }
  50%       { box-shadow: 0 4px 40px rgba(255,107,107,0.45); }
}
.hero-btn { animation: pulse-glow 2.5s ease-in-out infinite; }
.hero-btn:hover { animation: none; }

/* ── Reduced motion ── */
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
      }
      html { scroll-behavior: auto; }
      .reveal { opacity: 1; transform: none; }
    }
  </style>
</head>
<body>
  <!-- Контент будет добавлен в следующих задачах -->
  <main>
    <section id="hero" style="min-height:100vh;display:flex;align-items:center;justify-content:center;">
      <h1 style="font-family:sans-serif;">Алё...на! 👋 Скелет готов</h1>
    </section>
  </main>
</body>
</html>
```

- [ ] **Шаг 2: Открыть файл в браузере и проверить**

Открыть `index.html` двойным кликом или через Live Server в VS Code.
Ожидаемый результат: кремовый фон `#FFF8F3`, заголовок «Алё...на! 👋 Скелет готов» — шрифт Bricolage Grotesque загружен.

- [ ] **Шаг 3: Коммит**

```bash
git add index.html
git commit -m "feat: HTML skeleton with CSS custom properties and global styles"
```

---

## Task 2: Навигация (NAV)

**Files:**
- Modify: `index.html` — добавить `<header><nav>` и CSS для него

**Interfaces:**
- Consumes: CSS переменные из Task 1 (--accent, --surface, --text, --transition)
- Produces: sticky nav с якорями, кнопкой CTA и мобильным гамбургером; JS-классы `.nav-scrolled`, `.nav-open`

- [ ] **Шаг 1: Добавить HTML навигации**

Вставить сразу после `<body>`, перед `<main>`:

```html
<header class="nav-wrapper">
  <nav class="nav container">
    <a href="#hero" class="nav-logo">Алё<span class="accent">...</span>на!</a>
    <button class="nav-burger" aria-label="Открыть меню" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <ul class="nav-links" role="list">
      <li><a href="#services" class="nav-link">Услуги</a></li>
      <li><a href="#works"    class="nav-link">Работы</a></li>
      <li><a href="#process"  class="nav-link">Процесс</a></li>
      <li><a href="#contact"  class="nav-link">Контакт</a></li>
    </ul>
    <a href="#contact" class="btn btn-primary nav-cta">Написать →</a>
  </nav>
</header>
```

- [ ] **Шаг 2: Добавить CSS навигации**

В `<style>`, после блока `.btn-outline`:

```css
/* ── Навигация ── */
.nav-wrapper {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  transition: background var(--transition), box-shadow var(--transition);
}
.nav-wrapper.scrolled {
  background: rgba(255, 248, 243, 0.92);
  backdrop-filter: blur(12px);
  box-shadow: 0 1px 0 var(--border);
}
.nav {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding-block: 1.1rem;
}
.nav-logo {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 1.4rem;
  font-weight: 800;
  margin-right: auto;
}
.nav-links {
  display: flex;
  gap: 2rem;
}
.nav-link {
  font-weight: 500;
  color: var(--text-muted);
  transition: color var(--transition);
  position: relative;
}
.nav-link::after {
  content: '';
  position: absolute;
  bottom: -3px; left: 0;
  width: 0; height: 2px;
  background: var(--accent);
  transition: width var(--transition);
}
.nav-link:hover,
.nav-link.active { color: var(--text); }
.nav-link:hover::after,
.nav-link.active::after { width: 100%; }

.nav-burger {
  display: none;
  flex-direction: column;
  gap: 5px;
  padding: 8px;
  min-width: 44px; min-height: 44px;
  justify-content: center;
}
.nav-burger span {
  display: block;
  width: 22px; height: 2px;
  background: var(--text);
  border-radius: 2px;
  transition: var(--transition);
}
.nav-wrapper.open .nav-burger span:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); }
.nav-wrapper.open .nav-burger span:nth-child(2) { opacity: 0; }
.nav-wrapper.open .nav-burger span:nth-child(3) { transform: rotate(-45deg) translate(5px, -5px); }

/* Отступ под фиксированный nav */
body { padding-top: 72px; }

@media (max-width: 768px) {
  .nav-burger { display: flex; }
  .nav-cta { display: none; }
  .nav-links {
    display: none;
    position: absolute;
    top: 100%; left: 0; right: 0;
    flex-direction: column;
    background: var(--bg);
    padding: 1.5rem;
    border-top: 1px solid var(--border);
    gap: 1rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
  }
  .nav-wrapper.open .nav-links { display: flex; }
  .nav-link { font-size: 1.1rem; }
}
```

- [ ] **Шаг 3: Добавить JS навигации**

В конце `<body>`, добавить `<script>`:

```html
<script>
  // ── Nav: scrolled state ──
  const navWrapper = document.querySelector('.nav-wrapper');
  const navLinks   = document.querySelectorAll('.nav-link');
  const sections   = document.querySelectorAll('main section[id]');

  window.addEventListener('scroll', () => {
    navWrapper.classList.toggle('scrolled', window.scrollY > 20);
  }, { passive: true });

  // ── Nav: гамбургер ──
  const burger = document.querySelector('.nav-burger');
  burger.addEventListener('click', () => {
    const isOpen = navWrapper.classList.toggle('open');
    burger.setAttribute('aria-expanded', isOpen);
  });
  // Закрыть при клике на ссылку
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      navWrapper.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
    });
  });

  // ── Nav: активный пункт по скроллу ──
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        navLinks.forEach(l => l.classList.remove('active'));
        const active = document.querySelector(`.nav-link[href="#${entry.target.id}"]`);
        if (active) active.classList.add('active');
      }
    });
  }, { rootMargin: '-40% 0px -55% 0px' });
  sections.forEach(s => observer.observe(s));

  // ── Reveal при скролле ──
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));
</script>
```

- [ ] **Шаг 4: Проверить в браузере**

- Nav фиксируется при скролле и появляется полупрозрачный фон
- На мобильном (<768px) гамбургер открывает/закрывает меню
- Якорные ссылки плавно скроллят к секциям

- [ ] **Шаг 5: Коммит**

```bash
git add index.html
git commit -m "feat: sticky navigation with burger menu and active-link tracking"
```

---

## Task 3: Секция Hero + SVG-аватар

**Files:**
- Modify: `index.html` — заменить заглушку Hero на полную секцию

**Interfaces:**
- Consumes: CSS переменные, классы `.btn`, `.btn-primary`, `.reveal`
- Produces: секция `#hero` с SVG-аватаром, H1, подзаголовком, CTA и декоративным blob

- [ ] **Шаг 1: Заменить заглушку Hero**

Найти `<section id="hero" style="...">...</section>` и заменить на:

```html
<section id="hero">
  <div class="hero-blob" aria-hidden="true"></div>
  <div class="container hero-inner">

    <div class="hero-text">
      <p class="section-label">Цифровой мастер · Делаю с душой</p>
      <h1 class="hero-title">
        Алё<span class="accent">...</span>на!<br>
        Создаю сайты,<br>
        визитки и <span class="accent-2">AI-агентов</span><br>
        — под ключ
      </h1>
      <p class="hero-sub">
        Помогаю экспертам и малому бизнесу выглядеть
        профессионально в интернете.<br>
        <strong>Первая консультация — бесплатно.</strong>
      </p>
      <div class="hero-actions">
        <a href="#contact" class="btn btn-primary hero-btn">Обсудить проект →</a>
        <span class="hero-microcopy">Без обязательств · Отвечу в течение часа</span>
      </div>
    </div>

    <div class="hero-avatar" aria-label="Аватар Алёны">
      <!-- SVG-аватар: стилизованная девушка с телефонной трубкой -->
      <svg viewBox="0 0 320 400" fill="none" xmlns="http://www.w3.org/2000/svg"
           class="avatar-svg" role="img" aria-label="Улыбающаяся Алёна с телефонной трубкой">
        <!-- Фон-круг -->
        <circle cx="160" cy="200" r="155" fill="#FFF0E8"/>
        <!-- Тело -->
        <rect x="90" y="230" width="140" height="120" rx="30" fill="#A78BFA"/>
        <!-- Шея -->
        <rect x="140" y="205" width="40" height="35" rx="8" fill="#FDBCB4"/>
        <!-- Голова -->
        <ellipse cx="160" cy="180" rx="62" ry="68" fill="#FDBCB4"/>
        <!-- Волосы верх -->
        <ellipse cx="160" cy="128" rx="62" ry="30" fill="#3D2B1F"/>
        <!-- Волосы бока -->
        <rect x="98" y="128" width="22" height="80" rx="11" fill="#3D2B1F"/>
        <rect x="200" y="128" width="22" height="80" rx="11" fill="#3D2B1F"/>
        <!-- Чёлка -->
        <path d="M100 140 Q130 115 160 118 Q190 115 220 140" stroke="#3D2B1F" stroke-width="18" stroke-linecap="round" fill="none"/>
        <!-- Глаза -->
        <ellipse cx="138" cy="178" rx="9" ry="10" fill="#3D2B1F"/>
        <ellipse cx="182" cy="178" rx="9" ry="10" fill="#3D2B1F"/>
        <!-- Блики в глазах -->
        <circle cx="141" cy="174" r="3" fill="#fff"/>
        <circle cx="185" cy="174" r="3" fill="#fff"/>
        <!-- Румянец -->
        <ellipse cx="122" cy="194" rx="12" ry="7" fill="#FFB5B5" opacity="0.6"/>
        <ellipse cx="198" cy="194" rx="12" ry="7" fill="#FFB5B5" opacity="0.6"/>
        <!-- Улыбка -->
        <path d="M140 205 Q160 222 180 205" stroke="#D4887A" stroke-width="3.5" stroke-linecap="round" fill="none"/>
        <!-- Рука с трубкой — левая -->
        <rect x="62" y="248" width="32" height="80" rx="16" fill="#FDBCB4"/>
        <!-- Телефонная трубка -->
        <rect x="36" y="238" width="38" height="18" rx="9" fill="#FF6B6B"/>
        <rect x="36" y="298" width="38" height="18" rx="9" fill="#FF6B6B"/>
        <rect x="48" y="246" width="14" height="60" rx="7" fill="#FF6B6B"/>
        <!-- Звёздочки вокруг -->
        <text x="248" y="160" font-size="22" fill="#A78BFA">✦</text>
        <text x="55"  y="170" font-size="16" fill="#34D399">✦</text>
        <text x="260" y="240" font-size="14" fill="#FF6B6B">✦</text>
      </svg>
    </div>

  </div>
  <a href="#problem" class="hero-scroll" aria-label="Прокрутить вниз">
    <span>↓</span>
  </a>
</section>
```

- [ ] **Шаг 2: Добавить CSS Hero**

В `<style>`, после блока `@media (prefers-reduced-motion)`:

```css
/* ── Hero ── */
#hero {
  position: relative;
  min-height: calc(100vh - 72px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
}
.hero-blob {
  position: absolute;
  top: -200px; right: -150px;
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(167,139,250,0.18) 0%, transparent 70%);
  pointer-events: none;
  animation: drift 8s ease-in-out infinite alternate;
}
@keyframes drift {
  from { transform: translate(0, 0); }
  to   { transform: translate(40px, 30px); }
}
.hero-inner {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 4rem;
  align-items: center;
  padding-block: 5rem;
}
.hero-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: var(--font-hero);
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -0.02em;
  margin-bottom: 1.5rem;
}
.hero-sub {
  font-size: 1.1rem;
  color: var(--text-muted);
  max-width: 42ch;
  margin-bottom: 2rem;
  line-height: 1.7;
}
.hero-sub strong { color: var(--text); }
.hero-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}
.hero-microcopy {
  font-size: 0.85rem;
  color: var(--text-muted);
}
.hero-avatar {
  display: flex;
  justify-content: center;
}
.avatar-svg {
  width: 100%;
  max-width: 340px;
  animation: float 3.5s ease-in-out infinite;
  filter: drop-shadow(0 20px 40px rgba(167,139,250,0.2));
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-12px); }
}
.hero-scroll {
  display: flex;
  justify-content: center;
  padding-bottom: 2rem;
  color: var(--text-muted);
  animation: bounce 2s ease-in-out infinite;
  font-size: 1.4rem;
}
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(6px); }
}

@media (max-width: 900px) {
  .hero-inner {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 2.5rem;
  }
  .hero-sub { margin-inline: auto; }
  .hero-actions { justify-content: center; }
  .hero-avatar { order: -1; }
  .avatar-svg { max-width: 240px; }
}
```

- [ ] **Шаг 3: Проверить в браузере**

- Аватар отображается с анимацией покачивания
- Заголовок читается, акцентные слова в цвете
- На мобильном аватар сверху, текст снизу
- Стрелка ↓ анимируется

- [ ] **Шаг 4: Коммит**

```bash
git add index.html
git commit -m "feat: hero section with SVG avatar, title and CTA"
```

---

## Task 4: Секция Problem

**Files:**
- Modify: `index.html` — добавить секцию `#problem` после `#hero`

**Interfaces:**
- Consumes: `.container`, `.section-label`, `.section-title`, `.reveal`, `.reveal-delay-*`
- Produces: секция с 3 карточками болей клиента

- [ ] **Шаг 1: Добавить HTML секции Problem**

Вставить после закрытия `</section>` Hero:

```html
<section id="problem">
  <div class="container">
    <p class="section-label reveal">Вы не одиноки</p>
    <h2 class="section-title reveal reveal-delay-1">Узнаёте себя?</h2>
    <div class="problem-grid">
      <div class="problem-card reveal reveal-delay-1">
        <span class="problem-icon" aria-hidden="true">🕐</span>
        <p>«Хочу сайт — но объяснять технарям что нужно это как говорить на другом языке»</p>
      </div>
      <div class="problem-card reveal reveal-delay-2">
        <span class="problem-icon" aria-hidden="true">💸</span>
        <p>«Заплатила дизайнеру — получила что-то совсем не то, что хотела»</p>
      </div>
      <div class="problem-card reveal reveal-delay-3">
        <span class="problem-icon" aria-hidden="true">🤖</span>
        <p>«Слышу про AI везде, но не понимаю, как это поможет именно моему делу»</p>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Шаг 2: Добавить CSS секции Problem**

```css
/* ── Problem ── */
#problem {
  padding-block: var(--section-gap);
}
.problem-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-top: 3rem;
}
.problem-card {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 2rem;
  border-left: 4px solid var(--accent);
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  transition: transform var(--transition), box-shadow var(--transition);
}
.problem-card:nth-child(2) { border-color: var(--accent-2); }
.problem-card:nth-child(3) { border-color: var(--accent-3); }
.problem-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.09);
}
.problem-icon {
  display: block;
  font-size: 2rem;
  margin-bottom: 1rem;
}
.problem-card p {
  font-size: 1rem;
  color: var(--text);
  line-height: 1.6;
  font-style: italic;
}
@media (max-width: 768px) {
  .problem-grid { grid-template-columns: 1fr; }
}
```

- [ ] **Шаг 3: Проверить в браузере**

- 3 карточки в ряд на десктопе, стопкой на мобильном
- При скролле к секции карточки появляются с задержкой
- Левая цветная полоска у каждой карточки

- [ ] **Шаг 4: Коммит**

```bash
git add index.html
git commit -m "feat: problem section with three pain-point cards"
```

---

## Task 5: Секция Services

**Files:**
- Modify: `index.html` — добавить секцию `#services` после `#problem`

**Interfaces:**
- Consumes: `.container`, `.section-label`, `.section-title`, `.reveal`, `.btn`
- Produces: секция с 3 карточками услуг с ценами и CTA

- [ ] **Шаг 1: Добавить HTML Services**

```html
<section id="services">
  <div class="container">
    <p class="section-label reveal">Что я делаю</p>
    <h2 class="section-title reveal reveal-delay-1">Услуги</h2>
    <div class="services-grid">

      <article class="service-card reveal reveal-delay-1">
        <div class="service-icon" aria-hidden="true">🌐</div>
        <h3 class="service-title">Сайты и лендинги</h3>
        <p class="service-for">Для экспертов и малого бизнеса</p>
        <ul class="service-list">
          <li>Дизайн + разработка под ключ</li>
          <li>Адаптив для мобильных</li>
          <li>Форма заявки и аналитика</li>
          <li>Сдача за 7–14 дней</li>
        </ul>
        <div class="service-price">от 5 000 ₽</div>
        <a href="#contact" class="btn btn-outline service-cta">Узнать стоимость</a>
      </article>

      <article class="service-card service-card--featured reveal reveal-delay-2">
        <div class="service-badge">Популярно</div>
        <div class="service-icon" aria-hidden="true">💳</div>
        <h3 class="service-title">Цифровая визитка</h3>
        <p class="service-for">Для фрилансеров и экспертов</p>
        <ul class="service-list">
          <li>Ссылка вместо бумажной карточки</li>
          <li>Фото, соцсети, портфолио</li>
          <li>Уникальный стиль под вас</li>
          <li>Готово за 2–5 дней</li>
        </ul>
        <div class="service-price">от 3 000 ₽</div>
        <a href="#contact" class="btn btn-primary service-cta">Узнать стоимость</a>
      </article>

      <article class="service-card reveal reveal-delay-3">
        <div class="service-icon" aria-hidden="true">🤖</div>
        <h3 class="service-title">AI-агент</h3>
        <p class="service-for">Для бизнеса, который устал от рутины</p>
        <ul class="service-list">
          <li>Ответы клиентам 24/7</li>
          <li>Квалификация заявок</li>
          <li>Интеграция в Telegram/WhatsApp</li>
          <li>Внедрение от 10 дней</li>
        </ul>
        <div class="service-price">от 15 000 ₽</div>
        <a href="#contact" class="btn btn-outline service-cta">Узнать стоимость</a>
      </article>

    </div>
  </div>
</section>
```

- [ ] **Шаг 2: Добавить CSS Services**

```css
/* ── Services ── */
#services {
  padding-block: var(--section-gap);
  background: var(--surface);
}
.services-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-top: 3rem;
  align-items: start;
}
.service-card {
  background: var(--bg);
  border-radius: var(--radius);
  padding: 2rem;
  border: 1px solid var(--border);
  position: relative;
  transition: transform var(--transition), box-shadow var(--transition);
}
.service-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 50px var(--shadow);
}
.service-card--featured {
  background: #fff;
  border-color: var(--accent);
  box-shadow: 0 8px 30px var(--shadow);
}
.service-badge {
  position: absolute;
  top: -12px; right: 20px;
  background: var(--accent);
  color: #fff;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 50px;
  letter-spacing: 0.05em;
}
.service-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}
.service-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: var(--font-h3);
  font-weight: 700;
  margin-bottom: 0.4rem;
}
.service-for {
  font-size: 0.875rem;
  color: var(--text-muted);
  margin-bottom: 1.25rem;
}
.service-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}
.service-list li {
  font-size: 0.9rem;
  color: var(--text);
  padding-left: 1.2rem;
  position: relative;
}
.service-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: var(--accent-3);
  font-weight: 700;
}
.service-price {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--accent);
  margin-bottom: 1.25rem;
}
.service-cta { width: 100%; justify-content: center; }

@media (max-width: 900px) {
  .services-grid { grid-template-columns: 1fr; max-width: 480px; margin-inline: auto; }
}
```

- [ ] **Шаг 3: Проверить в браузере**

- 3 карточки, средняя выделена (badge «Популярно», акцентная рамка)
- Цены крупные, кнопки разные (outline / primary)
- Hover поднимает карточку

- [ ] **Шаг 4: Коммит**

```bash
git add index.html
git commit -m "feat: services section with three pricing cards"
```

---

## Task 6: Секция Works

**Files:**
- Modify: `index.html` — добавить секцию `#works` после `#services`

**Interfaces:**
- Consumes: `.container`, `.section-label`, `.section-title`, `.reveal`
- Produces: секция с 2 демо-проектами и честным дисклеймером

- [ ] **Шаг 1: Добавить HTML Works**

```html
<section id="works">
  <div class="container">
    <p class="section-label reveal">Мои работы</p>
    <h2 class="section-title reveal reveal-delay-1">Что уже создано</h2>
    <div class="works-grid">

      <article class="work-card reveal reveal-delay-1">
        <div class="work-preview work-preview--purple" aria-hidden="true">
          <span class="work-preview-text">Калькулятор<br>призвания</span>
        </div>
        <div class="work-info">
          <div class="work-tags">
            <span class="tag tag--purple">Демо-проект</span>
            <span class="tag">Лендинг</span>
            <span class="tag">CSS-анимации</span>
          </div>
          <h3 class="work-title">Калькулятор призвания</h3>
          <p class="work-desc">Лендинг для психологического теста. Адаптивная вёрстка, анимации на CSS, форма сбора контактов.</p>
        </div>
      </article>

      <article class="work-card reveal reveal-delay-2">
        <div class="work-preview work-preview--coral" aria-hidden="true">
          <span class="work-preview-text">Поздрав-<br>лятор</span>
        </div>
        <div class="work-info">
          <div class="work-tags">
            <span class="tag tag--green">Концепт</span>
            <span class="tag">UX</span>
            <span class="tag">MVP-план</span>
          </div>
          <h3 class="work-title">Поздравлятор</h3>
          <p class="work-desc">Концепт сервиса для видеооткрыток. UX-проектирование, прототип интерфейса, план MVP.</p>
        </div>
      </article>

    </div>
    <p class="works-disclaimer reveal">
      ✨ Это мои учебные работы — я только начинаю путь.
      Именно поэтому каждому проекту уделяю максимум внимания.
    </p>
  </div>
</section>
```

- [ ] **Шаг 2: Добавить CSS Works**

```css
/* ── Works ── */
#works {
  padding-block: var(--section-gap);
}
.works-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin-top: 3rem;
}
.work-card {
  background: var(--surface);
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid var(--border);
  transition: transform var(--transition), box-shadow var(--transition);
}
.work-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 50px rgba(0,0,0,0.1);
}
.work-preview {
  height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.work-preview--purple {
  background: linear-gradient(135deg, #A78BFA 0%, #7C3AED 100%);
}
.work-preview--coral {
  background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
}
.work-preview-text {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 1.8rem;
  font-weight: 800;
  color: rgba(255,255,255,0.9);
  text-align: center;
  line-height: 1.2;
}
.work-info { padding: 1.5rem; }
.work-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}
.tag {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 50px;
  background: var(--border);
  color: var(--text-muted);
}
.tag--purple { background: rgba(167,139,250,0.15); color: #7C3AED; }
.tag--green  { background: rgba(52,211,153,0.15);  color: #059669; }
.work-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.work-desc { font-size: 0.9rem; color: var(--text-muted); line-height: 1.6; }
.works-disclaimer {
  margin-top: 2.5rem;
  text-align: center;
  font-style: italic;
  color: var(--text-muted);
  font-size: 0.95rem;
}
@media (max-width: 768px) {
  .works-grid { grid-template-columns: 1fr; }
}
```

- [ ] **Шаг 3: Проверить в браузере**

- 2 карточки с цветными превью-плашками
- Тэги «Демо-проект» и «Концепт» видны
- Дисклеймер внизу курсивом

- [ ] **Шаг 4: Коммит**

```bash
git add index.html
git commit -m "feat: works section with two demo projects and honest disclaimer"
```

---

## Task 7: Секция Process

**Files:**
- Modify: `index.html` — добавить секцию `#process` после `#works`

**Interfaces:**
- Consumes: `.container`, `.section-label`, `.section-title`, `.reveal`
- Produces: 4 пронумерованных шага с пунктирной линией-коннектором

- [ ] **Шаг 1: Добавить HTML Process**

```html
<section id="process">
  <div class="container">
    <p class="section-label reveal">Прозрачность</p>
    <h2 class="section-title reveal reveal-delay-1">Как мы будем работать</h2>
    <div class="process-steps">

      <div class="process-step reveal reveal-delay-1">
        <div class="step-num" aria-hidden="true">01</div>
        <div class="step-body">
          <h3 class="step-title">Звонок — 20 минут</h3>
          <p class="step-desc">Разбираем задачу, отвечаю на вопросы о процессе и стоимости</p>
          <p class="step-result">→ Вы понимаете, что и как будет сделано</p>
        </div>
      </div>

      <div class="process-step reveal reveal-delay-2">
        <div class="step-num" aria-hidden="true">02</div>
        <div class="step-body">
          <h3 class="step-title">ТЗ и договор — 1–2 дня</h3>
          <p class="step-desc">Фиксируем требования, дизайн и функционал письменно</p>
          <p class="step-result">→ Документ, который защищает нас обоих</p>
        </div>
      </div>

      <div class="process-step reveal reveal-delay-3">
        <div class="step-num" aria-hidden="true">03</div>
        <div class="step-body">
          <h3 class="step-title">Разработка — 7–14 дней</h3>
          <p class="step-desc">Еженедельные апдейты, вы видите прогресс на каждом этапе</p>
          <p class="step-result">→ Никаких сюрпризов на финале</p>
        </div>
      </div>

      <div class="process-step reveal reveal-delay-3">
        <div class="step-num" aria-hidden="true">04</div>
        <div class="step-body">
          <h3 class="step-title">Сдача и поддержка</h3>
          <p class="step-desc">Обучаю пользоваться результатом, месяц бесплатных правок</p>
          <p class="step-result">→ Вы не остаётесь одни с готовым продуктом</p>
        </div>
      </div>

    </div>
  </div>
</section>
```

- [ ] **Шаг 2: Добавить CSS Process**

```css
/* ── Process ── */
#process {
  padding-block: var(--section-gap);
  background: var(--surface);
}
.process-steps {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  margin-top: 3rem;
  position: relative;
}
.process-steps::before {
  content: '';
  position: absolute;
  top: 2.2rem;
  left: 3rem;
  right: 3rem;
  height: 2px;
  background: repeating-linear-gradient(
    90deg, var(--accent) 0, var(--accent) 8px, transparent 8px, transparent 16px
  );
}
.process-step {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 0 1.5rem;
  position: relative;
}
.step-num {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 3rem;
  font-weight: 800;
  color: var(--accent);
  line-height: 1;
  margin-bottom: 1rem;
  background: var(--surface);
  position: relative;
  z-index: 1;
  padding-right: 0.5rem;
}
.step-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.step-desc {
  font-size: 0.875rem;
  color: var(--text-muted);
  line-height: 1.5;
  margin-bottom: 0.75rem;
}
.step-result {
  font-size: 0.875rem;
  color: var(--accent-3);
  font-weight: 600;
}
@media (max-width: 900px) {
  .process-steps {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  .process-steps::before {
    top: 0; bottom: 0;
    left: 1.8rem; right: auto;
    width: 2px; height: auto;
    background: repeating-linear-gradient(
      180deg, var(--accent) 0, var(--accent) 8px, transparent 8px, transparent 16px
    );
  }
  .process-step { flex-direction: row; gap: 1.5rem; align-items: flex-start; padding: 0 0 0 1rem; }
  .step-num { font-size: 2rem; min-width: 48px; text-align: center; padding: 0; }
}
```

- [ ] **Шаг 3: Проверить в браузере**

- 4 шага в ряд на десктопе, пунктирная линия между ними
- На мобильном — вертикальный список с боковой линией
- Числа 01–04 крупные, акцентный цвет

- [ ] **Шаг 4: Коммит**

```bash
git add index.html
git commit -m "feat: process section with 4 steps and connector line"
```

---

## Task 8: Секция Trust (Гарантии)

**Files:**
- Modify: `index.html` — добавить секцию `#trust` после `#process`

**Interfaces:**
- Consumes: `.container`, `.section-label`, `.section-title`, `.reveal`
- Produces: 4 карточки гарантий + 3 счётчика-стата

- [ ] **Шаг 1: Добавить HTML Trust**

```html
<section id="trust">
  <div class="container">
    <p class="section-label reveal">Спокойствие</p>
    <h2 class="section-title reveal reveal-delay-1">Работаем спокойно</h2>
    <div class="trust-grid">
      <div class="trust-card reveal reveal-delay-1">
        <span class="trust-icon" aria-hidden="true">📋</span>
        <h3 class="trust-title">Договор</h3>
        <p class="trust-desc">На каждый проект — письменное соглашение с зафиксированными сроками и стоимостью</p>
      </div>
      <div class="trust-card reveal reveal-delay-2">
        <span class="trust-icon" aria-hidden="true">💳</span>
        <h3 class="trust-title">Поэтапная оплата</h3>
        <p class="trust-desc">Аванс только после утверждения ТЗ. Финальная оплата — после сдачи</p>
      </div>
      <div class="trust-card reveal reveal-delay-3">
        <span class="trust-icon" aria-hidden="true">✏️</span>
        <h3 class="trust-title">Правки включены</h3>
        <p class="trust-desc">Месяц бесплатных правок после сдачи — не «за отдельную плату»</p>
      </div>
      <div class="trust-card reveal reveal-delay-3">
        <span class="trust-icon" aria-hidden="true">🎓</span>
        <h3 class="trust-title">Обучение</h3>
        <p class="trust-desc">Покажу как пользоваться результатом и отвечу на вопросы — не оставлю одну</p>
      </div>
    </div>
    <div class="trust-stats">
      <div class="stat reveal reveal-delay-1">
        <span class="stat-num">2</span>
        <span class="stat-label">проекта создано</span>
      </div>
      <div class="stat reveal reveal-delay-2">
        <span class="stat-num">100%</span>
        <span class="stat-label">сдано в срок</span>
      </div>
      <div class="stat reveal reveal-delay-3">
        <span class="stat-num">~1 ч</span>
        <span class="stat-label">время ответа</span>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Шаг 2: Добавить CSS Trust**

```css
/* ── Trust ── */
#trust {
  padding-block: var(--section-gap);
}
.trust-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
  margin-top: 3rem;
}
.trust-card {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1.75rem;
  border: 1px solid var(--border);
  transition: transform var(--transition), box-shadow var(--transition);
}
.trust-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(52,211,153,0.1);
  border-color: var(--accent-3);
}
.trust-icon {
  display: block;
  font-size: 2rem;
  margin-bottom: 0.75rem;
}
.trust-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 1.05rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.trust-desc {
  font-size: 0.875rem;
  color: var(--text-muted);
  line-height: 1.5;
}
.trust-stats {
  display: flex;
  justify-content: center;
  gap: 5rem;
  margin-top: 4rem;
  padding-top: 3rem;
  border-top: 1px solid var(--border);
}
.stat { text-align: center; }
.stat-num {
  display: block;
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: clamp(2.5rem, 5vw, 3.5rem);
  font-weight: 800;
  color: var(--accent);
  line-height: 1;
}
.stat-label {
  display: block;
  font-size: 0.875rem;
  color: var(--text-muted);
  margin-top: 0.4rem;
}
@media (max-width: 900px) {
  .trust-grid { grid-template-columns: repeat(2, 1fr); }
  .trust-stats { gap: 2.5rem; }
}
@media (max-width: 480px) {
  .trust-grid { grid-template-columns: 1fr; }
  .trust-stats { flex-direction: column; gap: 1.5rem; }
}
```

- [ ] **Шаг 3: Проверить в браузере**

- 4 карточки в ряд (2×2 на планшете)
- Счётчики крупные, коралловый цвет
- Hover на карточке — мятная рамка

- [ ] **Шаг 4: Коммит**

```bash
git add index.html
git commit -m "feat: trust section with guarantee cards and stats counters"
```

---

## Task 9: Секция CTA + Contact, Footer, Back-to-top

**Files:**
- Modify: `index.html` — добавить `#contact`, `<footer>`, кнопку «наверх» и мобильный sticky CTA

**Interfaces:**
- Consumes: `.container`, `.section-label`, `.section-title`, `.reveal`, `.btn`
- Produces: форма (Formspree-ready), footer, .back-to-top, .mobile-cta — используются JS в Task 10

- [ ] **Шаг 1: Добавить HTML Contact, Footer и вспомогательные элементы**

```html
<!-- Секция Contact -->
<section id="contact">
  <div class="contact-blob" aria-hidden="true"></div>
  <div class="container">
    <p class="section-label reveal">Давайте начнём</p>
    <h2 class="section-title reveal reveal-delay-1">
      Есть задача? Расскажите —<br>разберёмся вместе
    </h2>
    <p class="contact-sub reveal reveal-delay-2">
      Без технического жаргона. Первая консультация бесплатно.
    </p>
    <div class="contact-inner">
      <form class="contact-form reveal reveal-delay-2"
            action="https://formspree.io/f/ЗАМЕНИ_НА_СВОЙ_ID"
            method="POST">
        <div class="form-group">
          <label for="name">Ваше имя</label>
          <input type="text" id="name" name="name" required
                 placeholder="Как вас зовут?" autocomplete="name" />
        </div>
        <div class="form-group">
          <label for="contact-field">Telegram или email</label>
          <input type="text" id="contact-field" name="contact" required
                 placeholder="@username или name@mail.ru" />
        </div>
        <div class="form-group">
          <label for="message">Что нужно сделать?</label>
          <textarea id="message" name="message" rows="4" required
                    placeholder="Коротко опишите задачу — разберёмся вместе"></textarea>
        </div>
        <button type="submit" class="btn btn-primary form-submit">
          Отправить заявку →
        </button>
        <div class="form-success" aria-live="polite" hidden>
          Спасибо! Отвечу в течение часа 👋
        </div>
        <div class="form-error" aria-live="polite" hidden>
          Что-то пошло не так — напишите напрямую в Telegram
        </div>
      </form>
      <div class="contact-alt reveal reveal-delay-3">
        <p class="contact-alt-title">Или напишите напрямую:</p>
        <a href="https://t.me/elena_morozova_5555"
           class="btn btn-outline contact-tg"
           target="_blank" rel="noopener noreferrer">
          ✈️ Написать в Telegram
        </a>
        <p class="contact-promise">Отвечаю в рабочие дни в течение часа</p>
      </div>
    </div>
  </div>
</section>

<!-- Footer -->
<footer class="footer">
  <div class="container footer-inner">
    <a href="#hero" class="footer-logo">Алё<span class="accent">...</span>на!</a>
    <p class="footer-copy">
      © 2026 Алёна · Сделано с <span aria-label="любовью">♥</span> и кодом
    </p>
    <div class="footer-links">
      <a href="https://t.me/elena_morozova_5555"
         target="_blank" rel="noopener noreferrer"
         aria-label="Telegram">✈️ Telegram</a>
    </div>
  </div>
</footer>

<!-- Кнопка наверх -->
<button class="back-to-top" aria-label="Вернуться наверх" hidden>↑</button>

<!-- Мобильный sticky CTA -->
<a href="https://t.me/elena_morozova_5555"
   class="mobile-cta"
   target="_blank" rel="noopener noreferrer"
   aria-label="Написать Алёне в Telegram">
  ✈️ Написать Алёне
</a>
```

- [ ] **Шаг 2: Добавить CSS Contact, Footer и вспомогательных элементов**

```css
/* ── Contact ── */
#contact {
  padding-block: var(--section-gap);
  background: var(--surface);
  position: relative;
  overflow: hidden;
}
.contact-blob {
  position: absolute;
  bottom: -200px; left: -150px;
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(255,107,107,0.12) 0%, transparent 70%);
  pointer-events: none;
}
.contact-sub {
  color: var(--text-muted);
  font-size: 1.05rem;
  margin-bottom: 3rem;
  max-width: 50ch;
}
.contact-inner {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 4rem;
  align-items: start;
}
.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.form-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text);
}
.form-group input,
.form-group textarea {
  padding: 0.85rem 1rem;
  border: 1.5px solid var(--border);
  border-radius: var(--radius-sm);
  font: inherit;
  font-size: 1rem;
  background: var(--bg);
  color: var(--text);
  transition: border-color var(--transition), box-shadow var(--transition);
  outline: none;
  min-height: 44px;
}
.form-group input:focus,
.form-group textarea:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(255,107,107,0.1);
}
.form-group textarea { resize: vertical; min-height: 120px; }
.form-submit { align-self: flex-start; }
.form-success,
.form-error {
  padding: 0.85rem 1rem;
  border-radius: var(--radius-sm);
  font-weight: 500;
  font-size: 0.9rem;
}
.form-success { background: rgba(52,211,153,0.1); color: #059669; }
.form-error   { background: rgba(255,107,107,0.1); color: #dc2626; }

.contact-alt { padding-top: 1rem; }
.contact-alt-title {
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--text-muted);
}
.contact-tg { width: 100%; justify-content: center; }
.contact-promise {
  margin-top: 1rem;
  font-size: 0.8rem;
  color: var(--text-muted);
  text-align: center;
}

@media (max-width: 768px) {
  .contact-inner { grid-template-columns: 1fr; gap: 2rem; }
  .form-submit { width: 100%; justify-content: center; }
}

/* ── Footer ── */
.footer {
  padding-block: 2rem;
  border-top: 1px solid var(--border);
}
.footer-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}
.footer-logo {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 1.2rem;
  font-weight: 800;
}
.footer-copy {
  font-size: 0.875rem;
  color: var(--text-muted);
}
.footer-links a {
  font-size: 0.875rem;
  color: var(--text-muted);
  transition: color var(--transition);
}
.footer-links a:hover { color: var(--accent); }

/* ── Back to top ── */
.back-to-top {
  position: fixed;
  bottom: 2rem; right: 1.5rem;
  width: 44px; height: 44px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px var(--shadow);
  z-index: 50;
  transition: var(--transition);
  opacity: 0;
  pointer-events: none;
}
.back-to-top.visible {
  opacity: 1;
  pointer-events: auto;
}
.back-to-top:hover { transform: translateY(-3px); }

/* ── Мобильный sticky CTA ── */
.mobile-cta {
  display: none;
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background: var(--accent);
  color: #fff;
  text-align: center;
  padding: 1rem;
  font-weight: 700;
  font-size: 1rem;
  z-index: 90;
  box-shadow: 0 -4px 20px var(--shadow);
  transform: translateY(100%);
  transition: transform 0.4s ease;
}
.mobile-cta.show { transform: translateY(0); }

@media (max-width: 768px) {
  .mobile-cta { display: block; }
  .back-to-top { bottom: 5rem; }
  footer { padding-bottom: 5rem; }
}
@media (min-width: 769px) {
  .mobile-cta { display: none !important; }
}
```

- [ ] **Шаг 3: Проверить в браузере**

- Форма отображается корректно, поля с focus-стилями
- Footer на всю ширину, лого + копирайт + Telegram
- На мобильном mobile-cta прилипает снизу (после JS в Task 10)

- [ ] **Шаг 4: Коммит**

```bash
git add index.html
git commit -m "feat: contact section, footer, back-to-top and mobile sticky CTA"
```

---

## Task 10: JavaScript — интерактивность и форма

**Files:**
- Modify: `index.html` — расширить `<script>` полной JS-логикой

**Interfaces:**
- Consumes: `.back-to-top`, `.mobile-cta`, `.contact-form`, `.form-success`, `.form-error`, `.reveal`, навигационные элементы из Task 2
- Produces: полностью рабочий интерактивный сайт

- [ ] **Шаг 1: Заменить `<script>` на полную версию**

Найти весь блок `<script>...</script>` (созданный в Task 2) и заменить:

```html
<script>
  // ── Nav: scrolled state ──
  const navWrapper = document.querySelector('.nav-wrapper');
  const navLinks   = document.querySelectorAll('.nav-link');
  const sections   = document.querySelectorAll('main section[id]');

  window.addEventListener('scroll', onScroll, { passive: true });

  function onScroll() {
    const y = window.scrollY;
    navWrapper.classList.toggle('scrolled', y > 20);
    backToTop.classList.toggle('visible', y > 300);
    // Мобильный CTA: показать после 300px, скрыть у секции contact
    const contactTop = document.getElementById('contact')?.getBoundingClientRect().top ?? 9999;
    const shouldShow = y > 300 && contactTop > window.innerHeight * 0.5;
    mobileCta.classList.toggle('show', shouldShow);
  }

  // ── Nav: гамбургер ──
  const burger = document.querySelector('.nav-burger');
  burger.addEventListener('click', () => {
    const isOpen = navWrapper.classList.toggle('open');
    burger.setAttribute('aria-expanded', String(isOpen));
  });
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      navWrapper.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
    });
  });

  // ── Nav: активный пункт ──
  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      navLinks.forEach(l => l.classList.remove('active'));
      const active = document.querySelector(`.nav-link[href="#${entry.target.id}"]`);
      if (active) active.classList.add('active');
    });
  }, { rootMargin: '-40% 0px -55% 0px' });
  sections.forEach(s => sectionObserver.observe(s));

  // ── Reveal при скролле ──
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

  // ── Кнопка наверх ──
  const backToTop = document.querySelector('.back-to-top');
  backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  // ── Мобильный sticky CTA ──
  const mobileCta = document.querySelector('.mobile-cta');

  // ── Форма ──
  const form       = document.querySelector('.contact-form');
  const formSuccess = form?.querySelector('.form-success');
  const formError   = form?.querySelector('.form-error');

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = form.querySelector('.form-submit');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Отправляем...';
    formSuccess.hidden = true;
    formError.hidden   = true;

    try {
      const res = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      });
      if (res.ok) {
        formSuccess.hidden = false;
        form.reset();
        submitBtn.textContent = 'Отправить заявку →';
      } else {
        throw new Error('Server error');
      }
    } catch {
      formError.hidden = false;
      submitBtn.textContent = 'Отправить заявку →';
    } finally {
      submitBtn.disabled = false;
    }
  });

  // Инициализация на загрузке
  onScroll();
</script>
```

- [ ] **Шаг 2: Проверить в браузере**

**Чек-лист:**
- [ ] Nav появляется прозрачный/размытый после скролла
- [ ] Гамбургер открывает и закрывает меню на мобильном (<768px)
- [ ] Активный пункт nav подсвечивается при скролле к секции
- [ ] Секции плавно появляются при скролле (reveal)
- [ ] Кнопка «↑» появляется после 300px прокрутки и возвращает наверх
- [ ] Мобильный sticky CTA появляется после 300px и скрывается у секции Contact
- [ ] Форма: заполнить поля и нажать — появляется «Отправляем...», потом сообщение
  *(Для теста формы нужен реальный Formspree ID — без него будет error state, это ожидаемо)*

- [ ] **Шаг 3: Коммит**

```bash
git add index.html
git commit -m "feat: full JS interactions — nav, reveal, form submit, back-to-top, mobile CTA"
```

---

## Task 11: Финальная полировка и доступность

**Files:**
- Modify: `index.html` — добавить focus-стили, проверить aria, протестировать по чек-листу

**Interfaces:**
- Consumes: весь index.html из предыдущих задач
- Produces: полностью готовый к публикации `index.html`

- [ ] **Шаг 1: Добавить focus-стили и финальные CSS-улучшения**

Добавить в конец блока `<style>`:

```css
/* ── Focus visible (навигация с клавиатуры) ── */
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 3px;
  border-radius: 4px;
}

/* ── Скролл-полоса прогресса (опционально) ── */
@supports (animation-timeline: scroll()) {
  .scroll-progress {
    position: fixed;
    top: 0; left: 0;
    width: 0; height: 3px;
    background: var(--accent);
    z-index: 200;
    animation: progress-bar linear;
    animation-timeline: scroll();
  }
  @keyframes progress-bar {
    from { width: 0; }
    to   { width: 100%; }
  }
}

/* ── Выделение текста ── */
::selection {
  background: rgba(255, 107, 107, 0.2);
  color: var(--text);
}
```

Добавить `<div class="scroll-progress" aria-hidden="true"></div>` сразу после `<body>`.

- [ ] **Шаг 2: Проверить чек-лист из спецификации**

Открыть сайт в браузере и проверить каждый пункт:

```
Контент:
✓ Заголовок Hero описывает результат для клиента
✓ Честный дисклеймер для учебных проектов
✓ Стартовые цены видны в секции Services
✓ Процесс описан пошагово с этапами и сроками
✓ Форма содержит 3 поля
✓ CTA-кнопка — конкретное действие

Технические стандарты:
✓ Все изображения/SVG имеют alt/aria-label
✓ font-display: swap (в URL Google Fonts — display=swap)
✓ Мета-теги: title, description, og:title, og:description
✓ Copyright 2026

UX / Доступность:
✓ Мобильная версия проверена (DevTools → Toggle device)
✓ Тач-цели ≥ 44px (кнопки, ссылки)
✓ Sticky nav работает корректно
✓ Кнопка наверх появляется после прокрутки
✓ :focus-visible стили добавлены
✓ prefers-reduced-motion обрабатывается
✓ Семантическая разметка: header, nav, main, section, footer
```

- [ ] **Шаг 3: Проверить мобильную версию**

В DevTools (F12) → Toggle device toolbar (Ctrl+Shift+M):
- iPhone SE (375px) — самый узкий тест
- iPad (768px) — переломная точка

- [ ] **Шаг 4: Финальный коммит**

```bash
git add index.html
git commit -m "feat: final polish — focus styles, scroll progress, a11y audit complete"
```

---

## Task 12: Настройка Formspree и деплой (опционально)

**Files:**
- Modify: `index.html` — заменить заглушку Formspree ID

**Interfaces:**
- Consumes: `<form action="https://formspree.io/f/ЗАМЕНИ_НА_СВОЙ_ID">`
- Produces: работающая форма заявки

- [ ] **Шаг 1: Зарегистрироваться на Formspree**

1. Зайти на [formspree.io](https://formspree.io)
2. Создать аккаунт (бесплатный план — до 50 заявок/мес)
3. Создать новую форму, скопировать ID (вида `xpznabcd`)

- [ ] **Шаг 2: Заменить заглушку в форме**

Найти в `index.html`:
```
action="https://formspree.io/f/ЗАМЕНИ_НА_СВОЙ_ID"
```
Заменить `ЗАМЕНИ_НА_СВОЙ_ID` на реальный ID.

- [ ] **Шаг 3: Задеплоить сайт**

**Вариант A — GitHub Pages (бесплатно):**
```bash
git remote add origin https://github.com/ВАШ_USERNAME/my-landing.git
git push -u origin main
# В настройках репозитория → Pages → Source: main branch
```

**Вариант B — Netlify (перетащить папку):**
1. Зайти на netlify.com
2. Перетащить папку `my-landing-test` в область деплоя
3. Получить URL вида `random-name.netlify.app`

- [ ] **Шаг 4: Проверить форму на живом сайте**

Отправить тестовую заявку. В Formspree должно появиться письмо на вашу почту.

- [ ] **Шаг 5: Финальный коммит**

```bash
git add index.html
git commit -m "feat: configure Formspree form submission"
```

---

## Итог

После выполнения всех задач у вас будет:

| Задача | Результат |
|--------|-----------|
| Task 1 | HTML-скелет, CSS-переменные, шрифты |
| Task 2 | Sticky nav с гамбургером |
| Task 3 | Hero с SVG-аватаром |
| Task 4 | Секция Problem (боли клиента) |
| Task 5 | Секция Services (3 услуги с ценами) |
| Task 6 | Секция Works (2 демо-проекта) |
| Task 7 | Секция Process (4 шага) |
| Task 8 | Секция Trust (гарантии + счётчики) |
| Task 9 | Секция Contact + Footer + мобильный CTA |
| Task 10 | Полная JS-интерактивность |
| Task 11 | Финальная полировка и a11y |
| Task 12 | Formspree + деплой |
