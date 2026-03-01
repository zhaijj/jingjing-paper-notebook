/**
 * paper.js — Paper detail page
 * Reads ?id= from URL, finds paper in papers.json, renders full view
 */

document.addEventListener('DOMContentLoaded', async () => {
    const base = getBasePath();
    const id = new URLSearchParams(window.location.search).get('id');

    if (!id) { showError('No paper ID specified.'); return; }

    let papers;
    try {
        const res = await fetch(`${base}/js/papers.json`);
        papers = await res.json();
    } catch (e) {
        showError('Could not load paper database.'); return;
    }

    const paper = papers.find(p => p.id === id);
    if (!paper) { showError(`Paper "${id}" not found.`); return; }

    renderPaper(paper, base);
});

function getBasePath() {
    const path = window.location.pathname;
    if (path.includes('/jingjing-paper-notebook/')) return '/jingjing-paper-notebook/docs';
    return '.';
}

const JOURNAL_SLUGS = {
    'Nature Plants': 'nature-plants',
    'Nature Genetics': 'nature-genetics',
    'Nature Methods': 'nature-methods',
    'Nature Biotechnology': 'nature-biotech',
    'Nature': 'nature',
    'Cell': 'cell',
    'Cell Genomics': 'cell-genomics',
    'Genome Biology': 'genome-biology',
    'PNAS': 'pnas',
    'bioRxiv': 'biorxiv',
    'MBE': 'mbe',
    'arXiv': 'arxiv',
};

const JOURNAL_ACCENTS = {
    'nature-plants': '#4caf50',
    'nature-genetics': '#ab47bc',
    'nature-methods': '#29b6f6',
    'nature-biotech': '#ff7043',
    'nature': '#ef5350',
    'cell': '#ffa726',
    'cell-genomics': '#26c6da',
    'genome-biology': '#66bb6a',
    'pnas': '#5c6bc0',
    'biorxiv': '#ec407a',
    'mbe': '#8d6e63',
    'arxiv': '#ff7043',
    'default': '#8b949e',
};

function renderPaper(paper, base) {
    const slug = JOURNAL_SLUGS[paper.journal] || 'default';
    const accent = JOURNAL_ACCENTS[slug] || JOURNAL_ACCENTS.default;

    // Page title
    document.title = `${paper.title} | Jingjing's Paper Notebook`;

    // Accent CSS var
    document.documentElement.style.setProperty('--accent', accent);
    document.documentElement.style.setProperty('--accent-glow', hexToRgba(accent, 0.25));

    // Top hero bar color strip
    const heroBar = document.getElementById('paper-color-bar');
    if (heroBar) heroBar.style.background = `linear-gradient(90deg, ${accent}, transparent)`;

    // Journal badge
    setHTML('paper-journal-badge', `<span class="journal-badge journal-${slug}">${paper.journal}</span>`);

    // Year chip
    setHTML('paper-year', `<span class="card-year">${paper.year}</span>`);

    // Title
    setHTML('paper-title', paper.title);

    // Authors
    setHTML('paper-authors', (paper.authors || []).join(', '));

    // Stars
    setHTML('paper-stars', renderStars(paper.rating || 0));

    // Abstract
    setHTML('paper-abstract', paper.abstract || '<em>No abstract available.</em>');

    // Notes (parse simple markdown)
    setHTML('paper-notes', parseMarkdown(paper.notes || '_No notes yet._'));

    // DOI link
    const doiBtn = document.getElementById('btn-doi');
    if (doiBtn && paper.doi) {
        doiBtn.href = `https://doi.org/${paper.doi}`;
    } else if (doiBtn) {
        doiBtn.style.display = 'none';
    }

    // Sidebar info
    setHTML('info-journal', paper.journal || '—');
    setHTML('info-year', paper.year || '—');
    setHTML('info-doi', paper.doi ? `<a href="https://doi.org/${paper.doi}" target="_blank" style="color:var(--accent);word-break:break-all;">${paper.doi}</a>` : '—');
    setHTML('info-added', paper.addedDate || '—');
    setHTML('info-rating', renderStars(paper.rating || 0));

    // Tags
    const tagsEl = document.getElementById('paper-tags-cloud');
    if (tagsEl && paper.tags) {
        tagsEl.innerHTML = paper.tags.map(t =>
            `<span class="tag">${t}</span>`
        ).join('');
    }
}

// ── Simple Markdown Parser ────────────────────────────────────
function parseMarkdown(md) {
    if (!md) return '';
    return md
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/^- \[ \] (.+)$/gm, '<li class="task-item">$1</li>')
        .replace(/^- \[x\] (.+)$/gm, '<li class="task-item done">$1</li>')
        .replace(/^- (.+)$/gm, '<li>$1</li>')
        .replace(/(<li.*<\/li>\n?)+/g, m => `<ul>${m}</ul>`)
        .replace(/\n{2,}/g, '</p><p>')
        .replace(/^(?!<[hul])/gm, '')
        .trim();
}

// ── Helpers ───────────────────────────────────────────────────
function setHTML(id, html) {
    const el = document.getElementById(id);
    if (el) el.innerHTML = html;
}

function renderStars(rating) {
    return Array.from({ length: 5 }, (_, i) =>
        `<span class="star ${i < rating ? 'filled' : 'empty'}">${i < rating ? '★' : '☆'}</span>`
    ).join('');
}

function hexToRgba(hex, alpha) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r},${g},${b},${alpha})`;
}

function showError(msg) {
    const main = document.querySelector('main');
    if (main) main.innerHTML = `
    <div class="container" style="padding: 80px 0; text-align:center; color: var(--text-dim);">
      <h2 style="margin-bottom:12px;">Oops</h2>
      <p>${msg}</p>
      <a href="index.html" class="back-link" style="margin:24px auto 0;">← Back to Papers</a>
    </div>`;
}
