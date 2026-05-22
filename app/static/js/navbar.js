/**
 * Premium navbar — scroll, dropdowns, mobile drawer, search
 */
(function () {
    'use strict';

    const nav = document.getElementById('mainNav');
    const progress = document.getElementById('scrollProgress');
    const mobileBtn = document.getElementById('mobileMenuBtn');
    const mobileDrawer = document.getElementById('mobileNavDrawer');
    const mobileOverlay = document.getElementById('mobileNavOverlay');
    const mobileClose = document.getElementById('mobileNavClose');
    const searchModal = document.getElementById('searchModal');
    const searchBtn = document.getElementById('navSearchBtn');
    const mobileSearchBtn = document.getElementById('mobileSearchBtn');

    /* Scroll: progress + smooth nav color modes */
    let ticking = false;

    function updateNavMode() {
        const y = window.scrollY;
        const hasHero = document.body.classList.contains('has-hero-nav');
        const threshold = 50;
        const scrolled = y > threshold;

        document.body.classList.toggle('nav-scrolled', scrolled);
        if (nav) nav.classList.toggle('is-scrolled', scrolled);

        document.body.classList.remove('nav-mode-hero', 'nav-mode-scrolled', 'nav-mode-solid');
        if (hasHero && !scrolled) {
            document.body.classList.add('nav-mode-hero');
        } else if (scrolled) {
            document.body.classList.add('nav-mode-scrolled');
        } else {
            document.body.classList.add('nav-mode-solid');
        }
    }

    function onScroll() {
        const y = window.scrollY;
        const maxScroll = document.body.scrollHeight - window.innerHeight;
        if (progress && maxScroll > 0) {
            progress.style.width = `${Math.min(100, (y / maxScroll) * 100)}%`;
        }
        updateNavMode();
        ticking = false;
    }

    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(onScroll);
            ticking = true;
        }
    }, { passive: true });
    updateNavMode();

    window.addEventListener('resize', updateNavMode);

    /* Desktop dropdowns */
    const menuItems = document.querySelectorAll('.premium-menu-item.has-dropdown');
    let openItem = null;

    function closeAllDropdowns() {
        menuItems.forEach(item => {
            item.classList.remove('is-open');
            const btn = item.querySelector('.premium-dropdown-toggle');
            if (btn) btn.setAttribute('aria-expanded', 'false');
        });
        openItem = null;
    }

    menuItems.forEach(item => {
        const toggle = item.querySelector('.premium-dropdown-toggle');
        if (!toggle) return;

        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            const wasOpen = item.classList.contains('is-open');
            closeAllDropdowns();
            if (!wasOpen) {
                item.classList.add('is-open');
                toggle.setAttribute('aria-expanded', 'true');
                openItem = item;
            }
        });
    });

    document.addEventListener('click', closeAllDropdowns);
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAllDropdowns();
            closeMobile();
            closeSearch();
        }
    });

    /* Mobile drawer */
    function openMobile() {
        mobileDrawer?.classList.add('is-open');
        mobileOverlay?.classList.add('is-open');
        mobileBtn?.classList.add('is-active');
        mobileBtn?.setAttribute('aria-expanded', 'true');
        mobileDrawer?.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
    }

    function closeMobile() {
        mobileDrawer?.classList.remove('is-open');
        mobileOverlay?.classList.remove('is-open');
        mobileBtn?.classList.remove('is-active');
        mobileBtn?.setAttribute('aria-expanded', 'false');
        mobileDrawer?.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }

    mobileBtn?.addEventListener('click', () => {
        if (mobileDrawer?.classList.contains('is-open')) closeMobile();
        else openMobile();
    });
    mobileClose?.addEventListener('click', closeMobile);
    mobileOverlay?.addEventListener('click', closeMobile);

    /* Mobile accordions */
    document.querySelectorAll('.mobile-accordion-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const expanded = btn.getAttribute('aria-expanded') === 'true';
            const panel = btn.nextElementSibling;
            btn.setAttribute('aria-expanded', !expanded);
            panel?.classList.toggle('is-open', !expanded);
        });
    });

    document.querySelectorAll('.mobile-nav-body a').forEach(a => {
        a.addEventListener('click', () => closeMobile());
    });

    /* Search modal */
    function openSearch() {
        searchModal?.classList.add('is-open');
        searchModal?.setAttribute('aria-hidden', 'false');
        searchModal?.querySelector('input')?.focus();
        closeMobile();
    }

    function closeSearch() {
        searchModal?.classList.remove('is-open');
        searchModal?.setAttribute('aria-hidden', 'true');
    }

    searchBtn?.addEventListener('click', openSearch);
    mobileSearchBtn?.addEventListener('click', openSearch);
    document.getElementById('searchModalClose')?.addEventListener('click', closeSearch);
    document.getElementById('searchModalBackdrop')?.addEventListener('click', closeSearch);

    /* Keyboard: focus trap hint for dropdown toggles */
    document.querySelectorAll('.premium-dropdown-toggle').forEach(btn => {
        btn.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                btn.click();
            }
        });
    });
})();
