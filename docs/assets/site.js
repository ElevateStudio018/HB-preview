(function () {
  "use strict";

  // Menu on small screens: opens under the header.
  var btn = document.getElementById("menuBtn");
  var menu = document.getElementById("menu");
  if (btn && menu) {
    function setOpen(open) {
      menu.hidden = !open;
      btn.setAttribute("aria-expanded", String(open));
      btn.setAttribute("aria-label", open ? "Stäng menyn" : "Meny");
    }
    btn.addEventListener("click", function () { setOpen(menu.hidden); });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) setOpen(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !menu.hidden) { setOpen(false); btn.focus(); }
    });
  }

  // The hero film always plays, muted, in a loop, without controls. Phones only autoplay a muted inline video, so both
  // are set as properties too; and where the phone still holds it back (iOS in Low Power Mode) it starts on the first
  // touch or scroll, and again whenever the page comes back into view.
  var film = document.querySelector(".hero-video");
  if (film) {
    film.muted = true;
    film.defaultMuted = true;
    film.playsInline = true;
    film.setAttribute("webkit-playsinline", "");
    film.controls = false;
    var tryPlay = function () {
      if (!film.paused) return;
      var p = film.play();
      if (p && p.catch) p.catch(function () {});
    };
    tryPlay();
    film.addEventListener("loadeddata", tryPlay);
    film.addEventListener("canplay", tryPlay);
    film.addEventListener("pause", function () { if (!document.hidden) setTimeout(tryPlay, 200); });
    ["touchstart", "pointerdown", "scroll", "keydown"].forEach(function (ev) {
      window.addEventListener(ev, tryPlay, { passive: true });
    });
    document.addEventListener("visibilitychange", function () { if (!document.hidden) tryPlay(); });
    window.addEventListener("pageshow", tryPlay);
  }

  // Reference slider: the arrows scroll one project at a time and grey out at the ends.
  var slides = document.getElementById("slides");
  if (slides) {
    var arrows = document.querySelectorAll("[data-slide]");
    function step() { var first = slides.children[0]; return first ? first.getBoundingClientRect().width + parseFloat(getComputedStyle(slides).columnGap || 0) : 300; }
    function update() {
      arrows[0].disabled = slides.scrollLeft < 4;
      arrows[1].disabled = slides.scrollLeft + slides.clientWidth > slides.scrollWidth - 4;
    }
    arrows.forEach(function (b) { b.addEventListener("click", function () { slides.scrollBy({ left: step() * Number(b.dataset.slide), behavior: "smooth" }); }); });
    slides.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  document.querySelectorAll("[data-year]").forEach(function (y) { y.textContent = new Date().getFullYear(); });

  // Reference photos open full size over the page; Esc, the button or a click closes them. Without JS the link opens
  // the photo itself.
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a[data-full]");
    if (!a) return;
    e.preventDefault();
    var box = document.createElement("div");
    box.className = "lightbox";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    var alt = a.querySelector("img").alt;
    box.setAttribute("aria-label", alt);
    box.innerHTML = '<img src="' + a.getAttribute("href") + '" alt=""><button type="button">Stäng</button>';
    box.querySelector("img").alt = alt;
    function close() { box.remove(); document.removeEventListener("keydown", onKey); a.focus(); }
    function onKey(ev) { if (ev.key === "Escape") close(); }
    box.addEventListener("click", close);
    document.addEventListener("keydown", onKey);
    document.body.appendChild(box);
    box.querySelector("button").focus();
  });

  // Quote form: checked here, e-mailed through FormSubmit, then a thank-you in its place.
  var form = document.getElementById("qform");
  if (!form) return;
  var done = document.getElementById("qdone");
  var sendErr = document.getElementById("send-err");
  var f = {
    namn: document.getElementById("f-namn"),
    tel: document.getElementById("f-tel"),
    epost: document.getElementById("f-epost"),
    typ: document.getElementById("f-typ"),
    web: document.getElementById("f-web")
  };

  // "Begär offert" on a service page arrives with ?typ=… and that type chosen.
  var typ = new URLSearchParams(location.search).get("typ");
  if (typ) {
    for (var i = 0; i < f.typ.options.length; i++) if (f.typ.options[i].text === typ) f.typ.selectedIndex = i;
  }

  function mark(key, input, bad) {
    document.getElementById("e-" + key).hidden = !bad;
    input.setAttribute("aria-invalid", bad ? "true" : "false");
    if (bad) input.setAttribute("aria-describedby", "e-" + key); else input.removeAttribute("aria-describedby");
  }
  function validate() {
    var bad = [];
    var tel = f.tel.value.trim(), ep = f.epost.value.trim();
    var namnBad = !f.namn.value.trim();
    var contactBad = !tel && !ep;
    var epBad = !!ep && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(ep);
    mark("namn", f.namn, namnBad); if (namnBad) bad.push(f.namn);
    mark("tel", f.tel, contactBad); if (contactBad) bad.push(f.tel);
    mark("epost", f.epost, epBad); if (epBad) bad.push(f.epost);
    return bad;
  }
  form.addEventListener("input", function (e) {
    if (e.target.getAttribute("aria-invalid") === "true" || e.target === f.tel || e.target === f.epost) validate();
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var bad = validate();
    if (bad.length) { bad[0].focus(); return; }
    var submit = form.querySelector("button[type=submit]");
    submit.disabled = true;
    submit.textContent = "Skickar …";
    sendErr.hidden = true;
    // Every named field goes in the e-mail, in the order of the form; empty ones as "–".
    var payload = { _subject: "Offertförfrågan från hemsidan – " + f.namn.value.trim(), _template: "table", _captcha: "false", _honey: f.web.value };
    Array.prototype.forEach.call(form.elements, function (el) {
      if (el.name && el.name !== "_honey") payload[el.name] = el.value.trim() || "–";
    });
    if (f.epost.value.trim()) payload._replyto = f.epost.value.trim();
    fetch(form.getAttribute("data-endpoint"), {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(payload)
    }).then(function (r) {
      return r.json().catch(function () { return null; }).then(function (j) {
        if (!r.ok || !j || String(j.success) !== "true") throw new Error("not sent");
      });
    }).then(function () {
      form.reset();
      form.hidden = true;
      done.hidden = false;
      done.focus();
    }).catch(function () {
      // Kept as typed, so it can be sent again or read out over the phone.
      sendErr.hidden = false;
    }).then(function () {
      submit.disabled = false;
      submit.textContent = "Begär offert";
    });
  });

  document.getElementById("qagain").addEventListener("click", function () {
    done.hidden = true;
    form.hidden = false;
    f.namn.focus();
  });
})();
