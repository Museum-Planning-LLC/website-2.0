(function () {
  function init() {
    var nav = document.getElementById('site-nav');
    var btn = nav && nav.querySelector('.nav-hamburger');
    var menu = document.getElementById('site-nav-menu');
    if (!nav || !btn || !menu) return;

    function close() {
      nav.classList.remove('nav-open');
      btn.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }

    function open() {
      nav.classList.add('nav-open');
      btn.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    }

    function toggle() {
      if (nav.classList.contains('nav-open')) close();
      else open();
    }

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      toggle();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });

    window.addEventListener(
      'resize',
      function () {
        if (window.innerWidth > 900) close();
      },
      { passive: true }
    );

    document.addEventListener(
      'click',
      function (e) {
        if (!nav.classList.contains('nav-open')) return;
        if (!nav.contains(e.target)) close();
      },
      true
    );

    menu.querySelectorAll('a[href]').forEach(function (a) {
      a.addEventListener('click', function () {
        close();
      });
    });

    menu.querySelectorAll('button').forEach(function (b) {
      if (b === btn) return;
      b.addEventListener('click', function () {
        close();
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
