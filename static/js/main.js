/* =============================================================
   Team AI Showcase — main.js
   Minimal vanilla JS for search UX and small enhancements.
   ============================================================= */

(function () {
  "use strict";

  // ---------- Search ----------
  var searchInput = document.getElementById("search-input");

  if (searchInput) {
    var searchTimer = null;
    var searchForm = searchInput.closest("form");

    searchInput.addEventListener("input", function () {
      clearTimeout(searchTimer);
      searchTimer = setTimeout(function () {
        searchForm.requestSubmit();
      }, 350);
    });

    document.addEventListener("keydown", function (e) {
      // "/" focuses the search bar
      if (e.key === "/" && document.activeElement !== searchInput) {
        var tag = (document.activeElement && document.activeElement.tagName) || "";
        if (!/INPUT|TEXTAREA|SELECT/.test(tag)) {
          e.preventDefault();
          searchInput.focus();
          searchInput.select();
        }
      }
      // Escape clears and resets results
      if (e.key === "Escape" && document.activeElement === searchInput) {
        clearTimeout(searchTimer);
        searchInput.value = "";
        searchForm.requestSubmit();
      }
    });
  }

  // ---------- Smooth in-page anchor scrolling ----------
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener("click", function (e) {
      const id = link.getAttribute("href").slice(1);
      const target = id && document.getElementById(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  // ---------- Lazy fade-in for cards below the fold only ----------
  // Cards already visible on load are NOT hidden first, preventing
  // the flash/reset effect after a search form submission.
  if ("IntersectionObserver" in window) {
    const cards = document.querySelectorAll(".card");
    const viewportHeight = window.innerHeight;

    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });

    cards.forEach(function (card) {
      var rect = card.getBoundingClientRect();
      // Only animate cards that start below the visible viewport
      if (rect.top > viewportHeight) {
        card.style.opacity = "0";
        card.style.transform = "translateY(8px)";
        card.style.transition = "opacity .4s ease, transform .4s ease";
        io.observe(card);
      }
    });
  }
})();
