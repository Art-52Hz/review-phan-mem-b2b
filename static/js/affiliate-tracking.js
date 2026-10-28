/* Uses the site's existing GA setup; sends no referral query, token or link text. */
(function () {
  "use strict";
  document.addEventListener("click", function (event) {
    var link = event.target && event.target.closest ? event.target.closest("a[href]") : null;
    if (!link || typeof window.gtag !== "function") return;
    var dnt = navigator.doNotTrack || window.doNotTrack || navigator.msDoNotTrack;
    if (dnt === "1" || dnt === "yes") return;
    var target;
    try { target = new URL(link.href, window.location.href); } catch (_) { return; }
    if (target.protocol !== "https:" || target.hostname !== window.location.hostname) return;
    if (!/^\/downloads\/[a-z0-9-]+\.(txt|pdf|csv)$/.test(target.pathname)) return;
    window.gtag("event", "checklist_download_click", {
      asset_path: target.pathname,
      article_path: window.location.pathname,
      transport_type: "beacon"
    });
  });
  document.addEventListener("click", function (event) {
    var link = event.target && event.target.closest ? event.target.closest("a[data-affiliate='true']") : null;
    if (!link || typeof window.gtag !== "function") return;
    var dnt = navigator.doNotTrack || window.doNotTrack || navigator.msDoNotTrack;
    if (dnt === "1" || dnt === "yes") return;
    var target;
    try { target = new URL(link.href, window.location.href); } catch (_) { return; }
    if (target.protocol !== "https:" || target.hostname === window.location.hostname) return;
    var programs = {
      "mangools.com": "mangools", "get.murf.ai": "murf",
      "try.elevenlabs.io": "elevenlabs", "beautifulai.partnerlinks.io": "beautifulai",
      "ultahost.com": "ultahost", "www.hostinger.com": "hostinger"
    };
    var article = link.getAttribute("data-article");
    var content = link.closest(".post-content");
    if (!programs[target.hostname] || !article || !/^[a-z0-9][a-z0-9-]{0,254}$/.test(article) || !content) return;
    var bounds = content.getBoundingClientRect();
    var ratio = bounds.height > 0 ? (link.getBoundingClientRect().top - bounds.top) / bounds.height : 0;
    var position = ratio < 1 / 3 ? "top" : ratio < 2 / 3 ? "middle" : "bottom";
    window.gtag("event", "affiliate_click", {
      program: programs[target.hostname],
      article: article,
      position: position,
      transport_type: "beacon"
    });
  });
})();
