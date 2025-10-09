'use strict';

const cards = document.querySelectorAll('.card');

function onCardChange(cardId) {
    history.replaceState(null, '', `#${cardId}`);

    const tocArticles = document.querySelectorAll('.toc-article');
    tocArticles.forEach(article => {
        article.classList.remove('read', 'current');
    });

    tocArticles.forEach(article => {
        const href = article.getAttribute('href');
        if (!href) return;

        const tocCardId = href.substring(1);

        if (tocCardId === cardId) {
            article.classList.add('current');
        }

        const isRead = Number(tocCardId) <= Number(cardId);
        if (!isRead) return;
        article.classList.add('read');
    });
}

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        if (entry.intersectionRatio <= 0.5) return;
        const cardId = entry.target.id;
        onCardChange(cardId);
    });
}, {
    threshold: 0.5
});

cards.forEach(card => {
    observer.observe(card);
});
