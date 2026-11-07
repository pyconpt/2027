/* PyCon Portugal 2027 – navigation and carousel behavior (no framework needed). */
(function () {
  "use strict";

  /* Mobile navigation panel */
  const toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      const open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  /* Dropdown menus (click/tap; hover is handled in CSS) */
  const dropdowns = Array.prototype.slice.call(document.querySelectorAll(".has-dropdown"));

  function closeDropdowns(except) {
    dropdowns.forEach(function (item) {
      if (item === except) return;
      item.classList.remove("is-open");
      item.querySelector(".site-nav__link").setAttribute("aria-expanded", "false");
    });
  }

  dropdowns.forEach(function (item) {
    const button = item.querySelector(".site-nav__link");
    button.addEventListener("click", function () {
      const open = item.classList.toggle("is-open");
      button.setAttribute("aria-expanded", String(open));
      closeDropdowns(item);
    });
  });

  document.addEventListener("click", function (event) {
    if (!event.target.closest(".has-dropdown")) closeDropdowns(null);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closeDropdowns(null);
      document.body.classList.remove("nav-open");
      if (toggle) toggle.setAttribute("aria-expanded", "false");
    }
  });

  /* Previous editions carousel: native horizontal scroll + arrow buttons */
  document.querySelectorAll("[data-carousel]").forEach(function (carousel) {
    const track = carousel.querySelector(".carousel__track");
    const section = carousel.closest("section") || carousel;
    const step = function () {
      const item = track.querySelector(".edition");
      return item ? item.getBoundingClientRect().width + 20 : track.clientWidth * 0.8;
    };
    const prev = section.querySelector("[data-prev]");
    const next = section.querySelector("[data-next]");
    if (prev) prev.addEventListener("click", function () { track.scrollBy({ left: -step(), behavior: "smooth" }); });
    if (next) next.addEventListener("click", function () { track.scrollBy({ left: step(), behavior: "smooth" }); });
  });

  /* Cookie consent: Google Analytics (gtag.js) is only loaded after "Accept" */
  const consent = document.querySelector("[data-consent]");
  const CONSENT_KEY = "pyconpt-consent";

  function storedChoice() {
    try { return localStorage.getItem(CONSENT_KEY); } catch (e) { return null; }
  }

  function storeChoice(choice) {
    try { localStorage.setItem(CONSENT_KEY, choice); } catch (e) { /* private mode: ask again next visit */ }
  }

  function loadAnalytics() {
    if (document.getElementById("gtag-js")) return;
    window.gtag("consent", "update", { analytics_storage: "granted" });
    const script = document.createElement("script");
    script.id = "gtag-js";
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + consent.dataset.ga;
    document.head.appendChild(script);
  }

  function removeAnalyticsCookies() {
    // GA sets _ga and _ga_<id> on the widest domain it can, so try every parent domain
    const parts = location.hostname.split(".");
    document.cookie.split(";").forEach(function (cookie) {
      const name = cookie.split("=")[0].trim();
      if (name !== "_ga" && name.indexOf("_ga_") !== 0) return;
      for (let i = 0; i < parts.length; i++) {
        const domain = parts.slice(i).join(".");
        document.cookie = name + "=; Max-Age=0; path=/; domain=" + domain;
      }
      document.cookie = name + "=; Max-Age=0; path=/";
    });
  }

  if (consent && window.gtag) {
    if (storedChoice() === "granted") loadAnalytics();
    else if (storedChoice() !== "denied") consent.hidden = false;

    consent.querySelector("[data-consent-accept]").addEventListener("click", function () {
      storeChoice("granted");
      consent.hidden = true;
      loadAnalytics();
    });

    consent.querySelector("[data-consent-decline]").addEventListener("click", function () {
      storeChoice("denied");
      consent.hidden = true;
      window.gtag("consent", "update", { analytics_storage: "denied" });
      removeAnalyticsCookies();
    });

    document.querySelectorAll("[data-consent-open]").forEach(function (button) {
      button.addEventListener("click", function () {
        consent.hidden = false;
        consent.querySelector("[data-consent-accept]").focus();
      });
    });
  }
})();
