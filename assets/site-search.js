(function () {
  "use strict";

  function rootPrefix() {
    var parts = window.location.pathname.split("/").filter(Boolean);
    if (parts.length <= 1) return "";
    return "../".repeat(parts.length - 1);
  }

  function resolveUrl(url) {
    if (!url) return url;
    if (/^https?:\/\//i.test(url) || url.charAt(0) === "/") return url;
    return rootPrefix() + url;
  }

  function haystack(page) {
    return [page.type, page.title, page.desc, page.url, page.keywords]
      .filter(Boolean)
      .join(" ")
      .toLowerCase();
  }

  function matchScore(page, query) {
    var h = haystack(page);
    var title = (page.title || "").toLowerCase();
    var words = query.split(/\s+/).filter(Boolean);
    if (!words.length || !words.every(function (word) { return h.indexOf(word) !== -1; })) {
      return -1;
    }
    if (title === query) return 100;
    if (title.indexOf(query) === 0) return 90;
    if ((page.type || "").toLowerCase() === query) return 85;
    if (title.indexOf(query) !== -1) return 80;
    if ((page.url || "").toLowerCase().indexOf(query) !== -1) return 70;
    return 10;
  }

  function pageMatches(page, query) {
    return matchScore(page, query) >= 0;
  }

  function initSiteSearch() {
    var pages = window.SITE_SEARCH_PAGES;
    if (!Array.isArray(pages) || !pages.length) return;

    var input = document.getElementById("search-input");
    var results = document.getElementById("searchResults");
    var overlay = document.getElementById("searchOverlay");
    var toggle = document.getElementById("searchToggle");
    var closeBtn = document.getElementById("searchClose");
    if (!input || !results || !overlay || !toggle || !closeBtn) return;

    function closeSearch() {
      overlay.classList.remove("open");
      input.value = "";
      results.innerHTML = "";
    }

    toggle.addEventListener("click", function () {
      overlay.classList.add("open");
      setTimeout(function () {
        input.focus();
      }, 100);
    });

    closeBtn.addEventListener("click", closeSearch);

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeSearch();
    });

    input.addEventListener("input", function () {
      var q = input.value.toLowerCase().trim();
      if (!q) {
        results.innerHTML = "";
        return;
      }

      var matches = pages
        .map(function (p) {
          return { page: p, score: matchScore(p, q) };
        })
        .filter(function (item) {
          return item.score >= 0;
        })
        .sort(function (a, b) {
          return b.score - a.score;
        })
        .map(function (item) {
          return item.page;
        });

      if (!matches.length) {
        results.innerHTML =
          '<div class="search-empty">No results found.</div>';
        return;
      }

      results.innerHTML = matches
        .map(function (p) {
          return (
            '<a href="' +
            resolveUrl(p.url) +
            '" class="search-result"><div class="sr-type">' +
            p.type +
            '</div><div class="sr-title">' +
            p.title +
            '</div><div class="sr-desc">' +
            p.desc +
            "</div></a>"
          );
        })
        .join("");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initSiteSearch);
  } else {
    initSiteSearch();
  }
})();
