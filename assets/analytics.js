(function () {
  var w = typeof window !== "undefined" ? window : null;
  if (!w || typeof document === "undefined") return;

  var gtmRaw = w.GTM_CONTAINER_ID;
  var gtmId = gtmRaw && String(gtmRaw).trim();
  if (gtmId && /^GTM-[A-Z0-9]+$/i.test(gtmId)) {
    w.dataLayer = w.dataLayer || [];
    w.dataLayer.push({ "gtm.start": new Date().getTime(), event: "gtm.js" });
    var first = document.getElementsByTagName("script")[0];
    var j = document.createElement("script");
    j.async = true;
    j.src = "https://www.googletagmanager.com/gtm.js?id=" + encodeURIComponent(gtmId);
    if (first && first.parentNode) {
      first.parentNode.insertBefore(j, first);
    } else {
      document.head.appendChild(j);
    }
    return;
  }

  var raw = w.GA4_MEASUREMENT_ID;
  var id = raw && String(raw).trim();
  if (!id || !/^G-[A-Z0-9]+$/i.test(id)) {
    return;
  }

  w.dataLayer = w.dataLayer || [];
  function gtag() {
    w.dataLayer.push(arguments);
  }
  w.gtag = gtag;
  gtag("js", new Date());
  gtag("config", id);

  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(id);
  document.head.appendChild(s);
})();
