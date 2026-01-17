const API_BASE = '/api';

// Utils
const formatCurrency = (str) => {
    if (!str) return 'N/A';
    return str; // API usually returns formatted string like "$29.99"
};

// State
let currentProducts = [];

// Functions
async function searchProducts() {
    const query = document.getElementById('searchInput').value;
    if (!query) return;

    // UI Updates
    document.getElementById('loadingIndicator').classList.remove('hidden');
    document.getElementById('resultsArea').classList.add('hidden');

    try {
        const response = await fetch(`${API_BASE}/recommend/${encodeURIComponent(query)}?limit=5`);
        const products = await response.json();
        currentProducts = products;

        renderProducts(products);
    } catch (error) {
        console.error("Search failed:", error);
        alert("Failed to fetch products. Please try again.");
    } finally {
        document.getElementById('loadingIndicator').classList.add('hidden');
    }
}

function renderProducts(products) {
    const grid = document.getElementById('productsGrid');
    grid.innerHTML = '';

    if (products.length === 0) {
        grid.innerHTML = '<div class="col-span-3 text-center text-slate-500">No products found.</div>';
    }

    products.forEach((p, index) => {
        const delay = index * 100;
        const card = document.createElement('div');
        card.className = `glass-panel rounded-2xl overflow-hidden hover:shadow-[0_0_20px_rgba(56,189,248,0.2)] transition-all duration-300 hover:-translate-y-1 animate-fade-in group cursor-pointer`;
        card.style.animationDelay = `${delay}ms`;
        card.onclick = () => openAnalysis(p.asin);

        card.innerHTML = `
            <div class="relative h-48 bg-white p-4 flex items-center justify-center">
                <img src="${p.product_photo}" alt="${p.product_title}" class="max-h-full max-w-full object-contain group-hover:scale-110 transition-transform duration-500">
                <div class="absolute top-3 right-3 bg-slate-900/80 backdrop-blur text-white text-xs font-bold px-2 py-1 rounded">
                    #${p.rank}
                </div>
            </div>
            
            <div class="p-5">
                <div class="flex justify-between items-start mb-2">
                    <h3 class="text-white font-semibold line-clamp-2 h-12 text-sm leading-relaxed">${p.product_title}</h3>
                </div>
                
                <div class="flex items-center gap-2 mb-4">
                    <div class="flex text-yellow-400 text-xs">
                        ${getStarRating(p.product_star_rating)}
                    </div>
                    <span class="text-slate-500 text-xs">(${p.product_num_ratings || 0})</span>
                </div>

                <div class="flex justify-between items-center border-t border-slate-700/50 pt-4">
                    <div>
                        <span class="text-slate-400 text-xs block">Price</span>
                        <span class="text-lg font-bold text-sky-300">${formatCurrency(p.product_price)}</span>
                    </div>
                    
                    <div class="text-right">
                        <span class="text-slate-400 text-xs block">AI Score</span>
                        <div class="flex items-center gap-1">
                            <span class="text-xl font-bold ${getScoreColor(p.quality_score)}">${p.quality_score}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });

    document.getElementById('resultsArea').classList.remove('hidden');
}

function getStarRating(rating) {
    const r = parseFloat(rating) || 0;
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        if (i <= r) stars += '<i class="fas fa-star"></i>';
        else if (i - 0.5 <= r) stars += '<i class="fas fa-star-half-alt"></i>';
        else stars += '<i class="far fa-star"></i>';
    }
    return stars;
}

function getScoreColor(score) {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
}

// Modal Logic
async function openAnalysis(asin) {
    const modal = document.getElementById('analysisModal');
    modal.classList.remove('hidden');

    // Show loading state in modal if needed, or pre-fill with basics
    const product = currentProducts.find(p => p.asin === asin);
    if (product) {
        document.getElementById('modalTitle').textContent = product.product_title;
        document.getElementById('modalImage').src = product.product_photo;
        document.getElementById('modalPrice').textContent = product.product_price;
        document.getElementById('modalScore').textContent = product.quality_score;
        document.getElementById('modalScoreBar').style.width = `${product.quality_score}%`;

        if (product.is_prime) document.getElementById('modalPrime').classList.remove('hidden');
        else document.getElementById('modalPrime').classList.add('hidden');
    }

    // Fetch deep analysis
    try {
        const response = await fetch(`${API_BASE}/product/${asin}/analysis`);
        const fullData = await response.json();

        updateModalWithDetails(fullData);
    } catch (e) {
        console.error(e);
    }
}

function updateModalWithDetails(data) {
    // Populate reviews
    const reviewsList = document.getElementById('reviewsList');
    reviewsList.innerHTML = '';

    if (data.reviews && data.reviews.length > 0) {
        data.reviews.forEach(r => {
            const div = document.createElement('div');
            div.className = "bg-slate-900/50 p-3 rounded border border-slate-700/50";
            div.innerHTML = `
                <div class="flex justify-between mb-1">
                    <span class="text-xs text-slate-500">${r.review_date || 'Recent'}</span>
                    <span class="text-xs ${r.sentiment_label === 'Positive' ? 'text-green-400' : 'text-slate-400'}">${r.sentiment_label}</span>
                </div>
                <p class="text-slate-300 italic">"${r.review_comment ? r.review_comment.substring(0, 100) + '...' : ''}"</p>
            `;
            reviewsList.appendChild(div);
        });

        // Sentiment Text Summary (Mock generation based on data)
        const posCount = data.reviews.filter(r => r.sentiment_label === 'Positive').length;
        const total = data.reviews.length;
        const percent = Math.round((posCount / total) * 100);

        document.getElementById('modalSentimentText').textContent =
            `Analysis of ${total} recent reviews indicates a ${percent}% positive sentiment rate. ${percent > 70 ? 'Users strongly recommend this product.' : 'Opinions are mixed on this item.'}`;
    } else {
        reviewsList.textContent = "No detailed reviews available.";
    }
}

function closeModal() {
    document.getElementById('analysisModal').classList.add('hidden');
}

// Event Listeners
document.getElementById('searchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchProducts();
});
