// Section palettes and a homepage card stack.
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
  let enabled = false;
  let keyboardNavigation = false;
  let frame = 0;

  // Sticky positioning supplies the overlap. Every incoming panel settles
  // directly below the navigation instead of sliding underneath it.
  function configure() {
    enabled = cards.length > 1 && !reducedMotion.matches && !keyboardNavigation;
    const headerHeight = header.getBoundingClientRect().height;
    const available = innerHeight - headerHeight;

    // Short cards pin below the navigation. Tall cards use a negative sticky
    // offset: their content scrolls normally until the bottom has been seen,
    // then that bottom edge pins to the viewport before the next card covers it.
    cards.forEach((card, index) => {
      if (originalStyles[index] === null) card.removeAttribute("style");
      else card.setAttribute("style", originalStyles[index]);
      if (!enabled) return;
      const stickyTop = Math.min(headerHeight, innerHeight - card.offsetHeight);
      Object.assign(card.style, {
        position: "sticky",
        top: `${stickyTop}px`,
        zIndex: String(index + 1),
        boxShadow: index ? "0 -18px 40px rgb(0 0 0 / 10%)" : "none",
      });
    });
    schedule();
  }

  function update() {
    frame = 0;
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
