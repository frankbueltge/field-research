// Same-origin script. Under the policy under test, script-src is "'self' + hashes",
// so a same-origin external file is allowed to run while an inline <script> would not be.
// It reads back the computed style of an element that carries an inline style="" attribute
// and writes the answer into the DOM, where --dump-dom can read it.
(function () {
  var el = document.getElementById('probe');
  var cs = window.getComputedStyle(el);
  var out = document.getElementById('out');
  out.textContent = JSON.stringify({
    backgroundColor: cs.backgroundColor,
    color: cs.color,
    width: cs.width,
    height: cs.height
  });
})();
