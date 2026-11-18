/*!
 * ML in PL Jekyll Theme - Navigation
 * This script handles some events related with the navigation bar
 */

// Collapse the navbar background on scroll
window.addEventListener('scroll', function () {
    var navbar = document.querySelector('.navbar');
    if (!navbar) return;
    if (window.scrollY > 18) {
        navbar.classList.add('top-nav-collapse');
    } else {
        navbar.classList.remove('top-nav-collapse');
    }
});

// Scroll to in-page anchors without adding the #hash to the URL.
// No explicit behavior: the default ('auto') follows Bootstrap's `:root { scroll-behavior: smooth }`, which is off for users who prefer reduced motion.
document.querySelectorAll('a.page-scroll').forEach(function (link) {
    link.addEventListener('click', function (event) {
        var href = this.getAttribute('href');
        if (!href || href.charAt(0) !== '#') return;
        var target = document.querySelector(href);
        if (!target) return;
        event.preventDefault();
        target.scrollIntoView();
    });
});

// Close the responsive menu when a nav link is clicked
document.querySelectorAll('.navbar-collapse a').forEach(function (link) {
    link.addEventListener('click', function () {
        if (!this.getAttribute('href')) return;
        var collapseEl = document.querySelector('.navbar-collapse.show');
        if (collapseEl && window.bootstrap) {
            bootstrap.Collapse.getOrCreateInstance(collapseEl).hide();
        }
    });
});

// Remove the focused state after click, otherwise the link stays highlighted
document.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('mouseup', function () {
        if (this.getAttribute('href')) this.blur();
    });
});
