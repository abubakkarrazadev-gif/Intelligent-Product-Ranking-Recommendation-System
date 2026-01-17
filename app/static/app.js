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
let radarChartInstance = null;

async function openAnalysis(asin) {
    const modal = document.getElementById('analysisModal');
    modal.classList.remove('hidden');

    // Show loading...

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

    try {
        const response = await fetch(`${API_BASE}/product/${asin}/analysis`);
        const fullData = await response.json();

        updateModalWithDetails(fullData);
        renderRadarChart(fullData);
    } catch (e) {
        console.error(e);
    }
}

function updateModalWithDetails(data) {
    // Populate Pros/Cons
    const tagsDiv = document.getElementById('sentimentTags');
    tagsDiv.innerHTML = '';

    if (data.pros && data.pros.length > 0) {
        data.pros.forEach(p => {
            tagsDiv.innerHTML += `<span class="bg-green-500/20 text-green-400 text-xs px-2 py-1 rounded border border-green-500/30"><i class="fas fa-check mr-1"></i>${p}</span>`;
        });
    }

    if (data.cons && data.cons.length > 0) {
        data.cons.forEach(c => {
            tagsDiv.innerHTML += `<span class="bg-red-500/20 text-red-400 text-xs px-2 py-1 rounded border border-red-500/30"><i class="fas fa-times mr-1"></i>${c}</span>`;
        });
    }

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

        // Sentiment Text Summary
        const posCount = data.reviews.filter(r => r.sentiment_label === 'Positive').length;
        const total = data.reviews.length;
        const percent = Math.round((posCount / total) * 100);

        document.getElementById('modalSentimentText').textContent =
            `Analysis based on verified purchase reviews. ${percent}% positive sentiment detected.`;
    } else {
        reviewsList.textContent = "No detailed reviews available.";
    }
}

function renderRadarChart(data) {
    const ctx = document.getElementById('radarChart').getContext('2d');

    if (radarChartInstance) radarChartInstance.destroy();

    // Normalize values roughly
    const ratingNorm = (parseFloat(data.product_star_rating || 0) / 5) * 100;
    const sentimentNorm = data.quality_score; // Rough proxy
    const popularityNorm = Math.min(100, (data.product_num_ratings || 0) / 100);
    const priceVal = 80; // Placeholder as price is inverted value often

    radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Rating', 'Sentiment', 'Popularity', 'Value', 'Reliability'],
            datasets: [{
                label: 'Product Metrics',
                data: [ratingNorm, sentimentNorm, popularityNorm, priceVal, 90],
                backgroundColor: 'rgba(56, 189, 248, 0.2)',
                borderColor: '#38bdf8',
                pointBackgroundColor: '#fff',
                pointBorderColor: '#38bdf8',
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                r: {
                    angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    pointLabels: { color: '#94a3b8', font: { size: 12 } },
                    ticks: { display: false, backdropColor: 'transparent' },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}


function closeModal() {
    document.getElementById('analysisModal').classList.add('hidden');
}

// Event Listeners
document.getElementById('searchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchProducts();
});
