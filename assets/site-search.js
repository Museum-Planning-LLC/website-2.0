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
    return [page.type, page.title, page.desc, page.url]
      .filter(Boolean)
      .join(" ")
      .toLowerCase();
  }

  function pageMatches(page, query) {
    var h = haystack(page);
    var words = query.split(/\s+/).filter(Boolean);
    if (!words.length) return false;
    return words.every(function (word) {
      return h.indexOf(word) !== -1;
    });
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

      var matches = pages.filter(function (p) {
        return pageMatches(p, q);
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
