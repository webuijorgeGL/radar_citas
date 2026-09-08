(function () {
  "use strict";

  function track(eventName, parameters) {
    if (typeof window.gtag !== "function") return;
    window.gtag("event", eventName, parameters || {});
  }

  document.addEventListener("click", function (event) {
    var link = event.target.closest("a");
    if (!link) return;

    var eventName = link.dataset.analyticsEvent;
    if (eventName) {
      track(eventName, {
        link_url: link.href,
        link_text: link.textContent.trim().replace(/\s+/g, " "),
        page_path: window.location.pathname,
      });
    }

    if (link.closest(".main-nav, .footer-nav")) {
      track("navigation_click", {
        destination: link.getAttribute("href"),
        link_text: link.textContent.trim(),
      });
    }
  });

  var reachedDepths = {};
  window.addEventListener("scroll", function () {
    var scrollable = document.documentElement.scrollHeight - window.innerHeight;
    if (scrollable <= 0) return;
    var depth = Math.round((window.scrollY / scrollable) * 100);
    [25, 50, 75, 90].forEach(function (threshold) {
      if (depth >= threshold && !reachedDepths[threshold]) {
        reachedDepths[threshold] = true;
        track("scroll_depth", { percent_scrolled: threshold });
      }
    });
  }, { passive: true });

  if ("IntersectionObserver" in window) {
    var observedAds = new WeakSet();
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting || observedAds.has(entry.target)) return;
        observedAds.add(entry.target);
        track("ad_placement_view", {
          placement: entry.target.dataset.placement || "unknown",
          page_path: window.location.pathname,
        });
      });
    }, { threshold: 0.5 });

    document.querySelectorAll(".ad-placement").forEach(function (placement) {
      observer.observe(placement);
    });
  }
})();
