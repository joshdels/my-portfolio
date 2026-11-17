// Section palettes and a gently delayed, upward homepage card stack.
(() => {
  const header = document.querySelector(".site-header");
  const sections = [...document.querySelectorAll("[data-nav-theme]")];
  if (!header || !sections.length) return;

  const links = [...header.querySelectorAll("[data-section]")];
  const home = document.documentElement.classList.contains("home-scroll");
  const cards = home
    ? [...document.querySelectorAll("[data-home-stack] > section")]
    : [];
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  const originalStyles = cards.map((card) => card.getAttribute("style"));
  const originalSnap = document.documentElement.style.scrollSnapType;
  const offsets = cards.map(() => 0);
  let enabled = false;
  let keyboardNavigation = false;
  let frame = 0;
  let lastTime = 0;
  let easedScroll = scrollY;

  // Sticky positioning supplies the overlap. Every incoming panel settles
  // directly below the navigation instead of sliding underneath it.
  function configure() {
    enabled = cards.length > 1 && !reducedMotion.matches && !keyboardNavigation;
    const headerHeight = header.getBoundingClientRect().height;
    // A section taller than the space below the header cannot be pinned without
    // trapping its lower content, so it scrolls normally while still stacking.
    const available = innerHeight - headerHeight;

    // Pin the leading run of viewport-sized sections. The first section that
    // is too tall to pin — and everything after it — scrolls normally, so a
    // following panel can never cover a tall section's lower content.
    let pinning = true;
    cards.forEach((card, index) => {
      if (originalStyles[index] === null) card.removeAttribute("style");
      else card.setAttribute("style", originalStyles[index]);
      offsets[index] = 0;
      if (!enabled) return;
      if (card.offsetHeight > available) pinning = false;
      Object.assign(card.style, {
        position: pinning ? "sticky" : "relative",
        top: pinning ? `${headerHeight}px` : "",
        zIndex: String(index + 1),
        boxShadow: pinning && index ? "0 -18px 40px rgb(0 0 0 / 10%)" : "none",
      });
    });

    // Native snapping fights the card's easing; retain ordinary page scrolling.
    if (home)
      document.documentElement.style.scrollSnapType = enabled
        ? "none"
        : originalSnap;
    easedScroll = scrollY;
    lastTime = 0;
    schedule();
  }

  function update(time) {
    frame = 0;
    const elapsed = lastTime ? Math.min(time - lastTime, 64) : 16;
    lastTime = time;
    // About 140 ms of follow-through, independent of display refresh rate.
    easedScroll += (scrollY - easedScroll) * (1 - Math.exp(-elapsed / 140));
    const lag = Math.max(-48, Math.min(48, (scrollY - easedScroll) * 0.65));

    if (enabled) {
      const positions = cards.map((card, index) => ({
        top: card.getBoundingClientRect().top - offsets[index],
        pin: parseFloat(card.style.top),
      }));
      cards.forEach((card, index) => {
        // Only pinned (sticky) cards have a numeric resting position; cards
        // that scroll normally are left untouched.
        if (Number.isNaN(positions[index].pin)) {
          offsets[index] = 0;
          card.style.transform = "none";
          return;
        }
        const distance = Math.max(
          0,
          positions[index].top - positions[index].pin,
        );
        // Ease away the offset as a card reaches its resting position.
        const offset = index ? lag * Math.min(1, distance / 120) : 0;
        offsets[index] = Math.abs(offset) < 0.1 ? 0 : offset;
        card.style.transform = offsets[index]
          ? `translateY(${offsets[index]}px)`
          : "none";
      });
    }

    // Switch exactly when a section meets the navbar's bottom edge, so the
    // palette changes on contact rather than approximating it early.
    const edge = Math.min(
      innerHeight - 1,
      header.getBoundingClientRect().bottom,
    );
    // Later cards paint over earlier ones, so inspect the stack from the top.
    const active = [...sections].reverse().find((section) => {
      const rect = section.getBoundingClientRect();
      return rect.top <= edge && rect.bottom > edge;
    });
    header.dataset.theme = active ? active.dataset.navTheme : "light";
    links.forEach((link) => {
      if (active && link.dataset.section === active.id)
        link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });

    if (enabled && Math.abs(scrollY - easedScroll) > 0.1) schedule();
    else lastTime = 0;
  }

  function schedule() {
    if (!frame) frame = requestAnimationFrame(update);
  }

  addEventListener("scroll", schedule, { passive: true });
  addEventListener("resize", configure);
  addEventListener("pageshow", configure);
  reducedMotion.addEventListener("change", configure);

  // Unstack for keyboard browsing so focus never lands behind another card.
  addEventListener("keydown", (event) => {
    if (event.key === "Tab" && !keyboardNavigation) {
      keyboardNavigation = true;
      configure();
    }
  });
  addEventListener(
    "pointerdown",
    () => {
      if (keyboardNavigation) {
        keyboardNavigation = false;
        configure();
      }
    },
    { passive: true },
  );

  // Recalculate pin positions after images or web fonts change section heights.
  if (cards.length && "ResizeObserver" in window) {
    const observer = new ResizeObserver(configure);
    cards.forEach((card) => observer.observe(card));
    observer.observe(header);
  }
  configure();
})();
