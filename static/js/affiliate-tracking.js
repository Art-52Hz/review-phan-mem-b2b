/* Uses the site's existing GA setup; sends no referral query, token or link text. */
(function () {
  "use strict";
  document.addEventListener("click", function (event) {
    var link = event.target && event.target.closest ? event.target.closest("a[data-affiliate='true']") : null;
    if (!link || typeof window.gtag !== "function") return;
    var dnt = navigator.doNotTrack || window.doNotTrack || navigator.msDoNotTrack;
    if (dnt === "1" || dnt === "yes") return;
    var target;
    try { target = new URL(link.href, window.location.href); } catch (_) { return; }
    if (target.protocol !== "https:" || target.hostname === window.location.hostname) return;
    window.gtag("event", "affiliate_click", {
      affiliate_domain: target.hostname,
      article_path: window.location.pathname,
      transport_type: "beacon"
    });
  });
})();
