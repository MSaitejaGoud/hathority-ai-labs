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
    var cardGrid = document.getElementById("card-grid");
    var resultsSection = document.getElementById("results-section");
    var searchMeta = document.getElementById("search-meta");
    var searchMetaText = document.getElementById("search-meta-text");
    var activeCategory = searchForm.querySelector("input[name='category']");

    function pluralize(n) { return n === 1 ? "" : "s"; }

    function renderCards(projects, query) {
      if (projects.length === 0) {
        resultsSection.innerHTML = '<div class="empty" id="empty-state"><h2>No projects found</h2><p>Try a different search term.</p></div>';
        if (searchMeta) { searchMeta.style.display = query ? "" : "none"; }
        return;
      }
      var html = '<div class="card-grid" id="card-grid">';
      projects.forEach(function (p) {
        var media = p.image_url
          ? '<img src="' + p.image_url + '" alt="' + p.title + '" loading="lazy" />'
          : '<div class="card-media-placeholder" aria-hidden="true"><span>' + p.title + '</span></div>';
        var slug = p.category.toLowerCase().replace(/\s+/g, "-");
        html += '<a class="card" href="/project/' + p.pk + '/">';
        html += '<div class="card-media">' + media + '</div>';
        html += '<div class="card-body"><span class="tag">' + p.category + '</span><h3 class="card-title">' + p.title + '</h3><p class="card-desc">' + p.short_description + '</p></div>';
        html += '<div class="card-footer"><span class="card-link">View details →</span></div>';
        html += '</a>';
      });
      html += '</div>';
      resultsSection.innerHTML = html;
    }

    searchInput.addEventListener("focus", function () {
      document.querySelectorAll(".category-btn").forEach(function (btn) {
        btn.classList.remove("active");
      });
      document.querySelector(".category-btn[href*='category=all']").classList.add("active");
      fetch("/search/?q=&category=all")
        .then(function (r) { return r.json(); })
        .then(function (data) { renderCards(data.projects, ""); });
    });

    searchInput.addEventListener("input", function () {
      clearTimeout(searchTimer);
      var q = searchInput.value.trim();
      var cat = "all";
      searchTimer = setTimeout(function () {
        fetch("/search/?q=" + encodeURIComponent(q) + "&category=" + encodeURIComponent(cat))
          .then(function (r) { return r.json(); })
          .then(function (data) {
            renderCards(data.projects, data.query);
            if (searchMeta) {
              if (data.query) {
                searchMetaText.innerHTML = data.result_count + " result" + pluralize(data.result_count) + " for <strong>&ldquo;" + data.query + "&rdquo;</strong>";
                searchMeta.style.display = "";
              } else {
                searchMeta.style.display = "none";
              }
            }
          });
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
