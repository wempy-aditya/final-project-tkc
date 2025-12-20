/**
 * UI Components for Multimodal RAG System
 * Handles rendering of results, history, and other UI elements
 * Updated for robust Dark Mode support using CSS variables
 */

/**
 * Render search results
 */
function renderResults(data) {
    const container = document.getElementById('results-section');
    container.innerHTML = '';
    container.classList.remove('hidden');

    let html = '';

    // Query Info Card
    html += `
        <div class="card border-l-4 border-blue-500 p-6">
            <h3 class="text-base font-semibold text-[var(--text-main)] mb-4 flex items-center gap-2">
                <i class="fas fa-info-circle text-blue-600"></i> Query Information
            </h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="metric-card">
                    <div class="metric-value">${data.results.length}</div>
                    <div class="metric-label">Results Found</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${data.metrics.avg_similarity.toFixed(3)}</div>
                    <div class="metric-label">Avg Similarity</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${(data.metrics.diversity * 100).toFixed(0)}%</div>
                    <div class="metric-label">Diversity</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${data.metrics.retrieval_time.toFixed(2)}s</div>
                    <div class="metric-label">Retrieval Time</div>
                </div>
            </div>
        </div>
    `;

    // Retrieved Images
    html += `
        <div class="card border-l-4 border-green-500 overflow-hidden mt-6">
            <div class="px-6 py-4 gradient-header-green">
                <h3 class="text-base font-semibold text-[var(--text-main)] flex items-center gap-2">
                    <i class="fas fa-images text-green-600"></i> Retrieved Images
                </h3>
            </div>
            <div class="p-6">
                <div class="image-grid">
    `;

    data.results.forEach(result => {
        const qualityClass = result.similarity_score > 0.8 ? 'badge-high' :
            result.similarity_score > 0.6 ? 'badge-medium' : 'badge-low';

        html += `
            <div class="result-card">
                <div class="relative">
                    <img src="${result.image_base64}" alt="${result.file_name}" 
                         class="w-full h-48 object-cover">
                    <div class="absolute top-2 left-2">
                        <span class="badge badge-rank">#${result.rank}</span>
                    </div>
                    <div class="absolute top-2 right-2">
                        <span class="badge ${qualityClass}">${result.similarity_score.toFixed(3)}</span>
                    </div>
                </div>
                <div class="p-4">
                    <p class="text-xs text-[var(--text-muted)] mb-2 truncate" title="${result.file_name}">${result.file_name}</p>
                    <details class="text-sm">
                        <summary class="cursor-pointer text-indigo-500 hover:text-indigo-600 font-medium">
                            <i class="fas fa-comment-alt"></i> View Captions
                        </summary>
                        <ul class="mt-2 space-y-1 text-[var(--text-main)]">
                            ${result.captions.map(cap => `<li class="text-xs">• ${cap}</li>`).join('')}
                        </ul>
                    </details>
                </div>
            </div>
        `;
    });

    html += `
                </div>
            </div>
        </div>
    `;

    container.innerHTML = html;
}

/**
 * Render generated text
 */
function renderGeneratedText(data) {
    const container = document.getElementById('results-section');

    const html = `
        <div class="card border-l-4 border-purple-500 overflow-hidden mt-6">
            <div class="px-6 py-4 gradient-header-purple">
                <h3 class="text-base font-semibold text-[var(--text-main)] flex items-center gap-2">
                    <i class="fas fa-robot text-purple-600"></i> Generated Description
                </h3>
            </div>
            <div class="p-6">
                <div class="bg-[var(--bg-hover)] rounded-lg p-6 mb-4 border border-[var(--border-color)]">
                    <p class="text-[var(--text-main)] italic leading-relaxed">"${data.description}"</p>
                </div>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div class="metric-card">
                        <div class="metric-value">${data.metrics.word_count}</div>
                        <div class="metric-label">Words</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${data.metrics.sentence_count}</div>
                        <div class="metric-label">Sentences</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${(data.metrics.vocabulary_richness * 100).toFixed(0)}%</div>
                        <div class="metric-label">Vocabulary</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${data.generation_time.toFixed(2)}s</div>
                        <div class="metric-label">Gen Time</div>
                    </div>
                </div>
            </div>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', html);
}

/**
 * Render generated image
 */
function renderGeneratedImage(data) {
    const container = document.getElementById('results-section');

    const html = `
        <div class="card border-l-4 border-pink-500 overflow-hidden mt-6">
            <div class="px-6 py-4 gradient-header-pink">
                <h3 class="text-base font-semibold text-[var(--text-main)] flex items-center gap-2">
                    <i class="fas fa-palette text-pink-600"></i> Generated Image
                </h3>
            </div>
            <div class="p-6">
                <div class="mb-4">
                    <img src="${data.image_base64}" alt="Generated Image" 
                         class="w-full max-w-2xl mx-auto rounded-lg border border-[var(--border-color)]">
                </div>
                <details class="text-sm">
                    <summary class="cursor-pointer text-blue-500 hover:text-blue-600 text-sm font-medium mb-2">
                        View Prompt
                    </summary>
                    <div class="bg-[var(--bg-hover)] rounded-lg p-4 text-[var(--text-muted)]">
                        ${data.prompt}
                    </div>
                </details>
                <div class="mt-4 text-center text-sm text-[var(--text-muted)]">
                    Generation time: ${data.generation_time.toFixed(2)}s
                </div>
            </div>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', html);
}

/**
 * Render history list
 */
function renderHistory(queries) {
    const container = document.getElementById('history-list');

    if (!queries || queries.length === 0) {
        container.innerHTML = `
            <div class="text-center text-[var(--text-muted)] py-8">
                <i class="fas fa-clock text-4xl mb-2 opacity-30"></i>
                <p>No history yet</p>
            </div>
        `;
        return;
    }

    let html = '';
    queries.forEach(query => {
        const timestamp = query.timestamp ? query.timestamp.split('.')[0] : 'Just now';
        const modeIcon = query.query_mode === 'Text Only' ? 'fa-font' :
            query.query_mode === 'Image Only' ? 'fa-image' : 'fa-layer-group';

        html += `
            <div class="p-3 mb-2 rounded-lg cursor-pointer hover:bg-[var(--bg-hover)] border border-transparent hover:border-[var(--border-color)] transition-all" onclick="loadQueryFromHistory(${query.id})">
                <div class="flex items-start justify-between">
                    <div class="flex-1 overflow-hidden">
                        <div class="flex items-center gap-2 mb-1">
                            <i class="fas ${modeIcon} text-indigo-500 text-xs"></i>
                            <span class="text-xs font-semibold text-[var(--text-main)]">${query.query_mode}</span>
                        </div>
                        ${query.query_text ? `<p class="text-xs text-[var(--text-muted)] truncate">${query.query_text}</p>` : ''}
                        <div class="flex items-center gap-3 mt-1 text-xs text-[var(--text-light)]">
                            <span><i class="fas fa-chart-line"></i> ${query.avg_similarity.toFixed(2)}</span>
                        </div>
                    </div>
                    <button onclick="deleteQueryFromHistory(${query.id}, event)" 
                            class="text-[var(--text-light)] hover:text-red-500 ml-2 transition-colors">
                        <i class="fas fa-trash text-xs"></i>
                    </button>
                </div>
                <div class="text-[10px] text-[var(--text-light)] mt-1 text-right">${timestamp}</div>
            </div>
        `;
    });

    container.innerHTML = html;
}

/**
 * Render loaded query
 */
function renderLoadedQuery(queryData) {
    const container = document.getElementById('results-section');
    container.innerHTML = '';
    container.classList.remove('hidden');

    let html = `
        <div class="bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500 p-4 mb-6 rounded">
            <div class="flex items-center gap-2">
                <i class="fas fa-folder-open text-blue-500"></i>
                <p class="text-blue-700 dark:text-blue-300 font-medium">Loaded from history: ${queryData.timestamp}</p>
            </div>
        </div>
    `;

    // Query info
    html += `
        <div class="card p-6 mb-6">
            <h3 class="text-lg font-bold text-[var(--text-main)] mb-4">Query Information</h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="metric-card">
                    <div class="text-sm text-[var(--text-muted)]">Mode</div>
                    <div class="font-semibold text-[var(--text-main)]">${queryData.query_mode}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${queryData.avg_similarity.toFixed(3)}</div>
                    <div class="metric-label">Avg Similarity</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${(queryData.diversity * 100).toFixed(0)}%</div>
                    <div class="metric-label">Diversity</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${queryData.total_time.toFixed(2)}s</div>
                    <div class="metric-label">Total Time</div>
                </div>
            </div>
            ${queryData.query_text ? `<div class="mt-4 p-4 bg-[var(--bg-hover)] rounded-lg border border-[var(--border-color)]"><strong class="text-[var(--text-main)]">Query:</strong> <span class="text-[var(--text-muted)]">${queryData.query_text}</span></div>` : ''}
        </div>
    `;

    // Query image if exists
    if (queryData.query_image_base64) {
        html += `
            <div class="card p-6 mb-6">
                <h3 class="text-lg font-bold text-[var(--text-main)] mb-4">Query Image</h3>
                <img src="${queryData.query_image_base64}" class="max-w-sm rounded-lg shadow border border-[var(--border-color)]">
            </div>
        `;
    }

    // Retrieved images
    html += `
        <div class="card border-l-4 border-green-500 overflow-hidden mb-6">
            <div class="px-6 py-4 gradient-header-green">
                <h3 class="text-base font-semibold text-[var(--text-main)] flex items-center gap-2">
                    <i class="fas fa-images text-green-600"></i> Retrieved Images
                </h3>
            </div>
            <div class="p-6">
                <div class="image-grid">
    `;

    queryData.retrieval_results.forEach(result => {
        const qualityClass = result.similarity_score > 0.8 ? 'badge-high' :
            result.similarity_score > 0.6 ? 'badge-medium' : 'badge-low';

        html += `
            <div class="result-card">
                <div class="relative">
                    <img src="${result.image_base64}" alt="${result.file_name}" 
                         class="w-full h-48 object-cover">
                    <div class="absolute top-2 left-2">
                        <span class="badge badge-rank">#${result.rank}</span>
                    </div>
                    <div class="absolute top-2 right-2">
                        <span class="badge ${qualityClass}">${result.similarity_score.toFixed(3)}</span>
                    </div>
                </div>
                <div class="p-4">
                    <p class="text-xs text-[var(--text-muted)] mb-2 truncate">${result.file_name}</p>
                    <details class="text-sm">
                        <summary class="cursor-pointer text-indigo-500 hover:text-indigo-600 font-medium">
                            View Captions
                        </summary>
                        <ul class="mt-2 space-y-1 text-[var(--text-main)]">
                            ${result.captions.map(cap => `<li class="text-xs">• ${cap}</li>`).join('')}
                        </ul>
                    </details>
                </div>
            </div>
        `;
    });

    html += `</div></div></div>`;

    // Generated text if exists
    if (queryData.generated_text) {
        html += `
            <div class="card p-6 mb-6">
                <h3 class="text-lg font-bold text-[var(--text-main)] mb-4">Generated Description</h3>
                <div class="bg-[var(--bg-hover)] rounded-lg p-6 border border-[var(--border-color)]">
                    <p class="text-[var(--text-main)] italic">"${queryData.generated_text}"</p>
                </div>
            </div>
        `;
    }

    // Generated image if exists
    if (queryData.generated_image_base64) {
        html += `
            <div class="card p-6 mb-6">
                <h3 class="text-lg font-bold text-[var(--text-main)] mb-4">Generated Image</h3>
                <img src="${queryData.generated_image_base64}" class="max-w-2xl mx-auto rounded-lg shadow-lg border border-[var(--border-color)]">
            </div>
        `;
    }

    container.innerHTML = html;
}

/**
 * Show toast notification
 */
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const icon = document.getElementById('toast-icon');
    const messageEl = document.getElementById('toast-message');

    const icons = {
        success: '<i class="fas fa-check-circle text-green-500 text-2xl"></i>',
        error: '<i class="fas fa-exclamation-circle text-red-500 text-2xl"></i>',
        info: '<i class="fas fa-info-circle text-blue-500 text-2xl"></i>',
        warning: '<i class="fas fa-exclamation-triangle text-yellow-500 text-2xl"></i>'
    };

    // Helper to determine toast colors based on type
    let bgClass = 'bg-white';
    let textClass = 'text-gray-800';
    let borderClass = 'border-l-4';

    // In our new system, toast ID in CSS handles the background color from proper variable
    // We just need to make sure we don't hardcode conflicting classes here.
    // The CSS #toast handles basics. We just update content.

    icon.innerHTML = icons[type] || icons.info;
    messageEl.textContent = message;

    // Ensure text color matches theme
    messageEl.className = 'text-sm font-medium text-[var(--text-main)]';

    toast.classList.add('translate-y-0');
    toast.classList.remove('translate-y-24');

    setTimeout(() => {
        toast.classList.add('translate-y-24');
        toast.classList.remove('translate-y-0');
    }, 3000);
}
