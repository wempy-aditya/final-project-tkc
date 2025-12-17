/**
 * UI Components for Multimodal RAG System
 * Handles rendering of results, history, and other UI elements
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
        <div class="bg-white rounded-lg shadow-sm border-l-4 border-blue-500 p-6">
            <h3 class="text-base font-semibold text-gray-900 mb-4 flex items-center gap-2">
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
        <div class="bg-white rounded-lg shadow-sm border-l-4 border-green-500 overflow-hidden">
            <div class="px-6 py-4 bg-gradient-to-r from-green-50 to-white border-b border-gray-100">
                <h3 class="text-base font-semibold text-gray-900 flex items-center gap-2">
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
            <div class="result-card bg-white rounded-lg overflow-hidden">
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
                    <p class="text-xs text-gray-600 mb-2 truncate">${result.file_name}</p>
                    <details class="text-sm">
                        <summary class="cursor-pointer text-indigo-600 hover:text-indigo-700 font-medium">
                            <i class="fas fa-comment-alt"></i> View Captions
                        </summary>
                        <ul class="mt-2 space-y-1 text-gray-700">
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
        <div class="bg-white rounded-lg shadow-sm border-l-4 border-purple-500 overflow-hidden">
            <div class="px-6 py-4 bg-gradient-to-r from-purple-50 to-white border-b border-gray-100">
                <h3 class="text-base font-semibold text-gray-900 flex items-center gap-2">
                    <i class="fas fa-robot text-purple-600"></i> Generated Description
                </h3>
            </div>
            <div class="p-6">
                <div class="bg-gray-50 rounded-lg p-6 mb-4 border border-gray-200">
                    <p class="text-gray-800 italic leading-relaxed">"${data.description}"</p>
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
        <div class="bg-white rounded-lg shadow-sm border-l-4 border-pink-500 overflow-hidden">
            <div class="px-6 py-4 bg-gradient-to-r from-pink-50 to-white border-b border-gray-100">
                <h3 class="text-base font-semibold text-gray-900 flex items-center gap-2">
                    <i class="fas fa-palette text-pink-600"></i> Generated Image
                </h3>
            </div>
            <div class="p-6">
                <div class="mb-4">
                    <img src="${data.image_base64}" alt="Generated Image" 
                         class="w-full max-w-2xl mx-auto rounded-lg border border-gray-200">
                </div>
                <details class="text-sm">
                    <summary class="cursor-pointer text-blue-600 hover:text-blue-700 text-sm font-medium mb-2">
                        View Prompt
                    </summary>
                    <div class="bg-gray-50 rounded-lg p-4 text-gray-700">
                        ${data.prompt}
                    </div>
                </details>
                <div class="mt-4 text-center text-sm text-gray-600">
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
            <div class="text-center text-gray-500 py-8">
                <i class="fas fa-clock text-4xl mb-2"></i>
                <p>No history yet</p>
            </div>
        `;
        return;
    }

    let html = '';
    queries.forEach(query => {
        const timestamp = query.timestamp.split('.')[0];
        const modeIcon = query.query_mode === 'Text Only' ? 'fa-font' :
            query.query_mode === 'Image Only' ? 'fa-image' : 'fa-layer-group';

        html += `
            <div class="history-item mb-2" onclick="loadQueryFromHistory(${query.id})">
                <div class="flex items-start justify-between">
                    <div class="flex-1">
                        <div class="flex items-center gap-2 mb-1">
                            <i class="fas ${modeIcon} text-indigo-600 text-xs"></i>
                            <span class="text-xs font-semibold text-gray-700">${query.query_mode}</span>
                        </div>
                        ${query.query_text ? `<p class="text-xs text-gray-600 truncate">${query.query_text.substring(0, 30)}...</p>` : ''}
                        <div class="flex items-center gap-3 mt-1 text-xs text-gray-500">
                            <span><i class="fas fa-chart-line"></i> ${query.avg_similarity.toFixed(2)}</span>
                            <span><i class="fas fa-clock"></i> ${query.total_time.toFixed(1)}s</span>
                        </div>
                    </div>
                    <button onclick="deleteQueryFromHistory(${query.id}, event)" 
                            class="text-red-500 hover:text-red-700 ml-2">
                        <i class="fas fa-trash text-xs"></i>
                    </button>
                </div>
                <div class="text-xs text-gray-400 mt-1">${timestamp}</div>
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
        <div class="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6 rounded">
            <div class="flex items-center gap-2">
                <i class="fas fa-folder-open text-blue-500"></i>
                <p class="text-blue-700 font-medium">Loaded from history: ${queryData.timestamp}</p>
            </div>
        </div>
    `;

    // Query info
    html += `
        <div class="bg-white rounded-xl shadow-md p-6 mb-6">
            <h3 class="text-lg font-bold text-gray-800 mb-4">Query Information</h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="metric-card">
                    <div class="text-sm text-gray-600">Mode</div>
                    <div class="font-semibold text-gray-800">${queryData.query_mode}</div>
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
            ${queryData.query_text ? `<div class="mt-4 p-4 bg-gray-50 rounded-lg"><strong>Query:</strong> ${queryData.query_text}</div>` : ''}
        </div>
    `;

    // Query image if exists
    if (queryData.query_image_base64) {
        html += `
            <div class="bg-white rounded-xl shadow-md p-6 mb-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">Query Image</h3>
                <img src="${queryData.query_image_base64}" class="max-w-sm rounded-lg shadow">
            </div>
        `;
    }

    // Retrieved images
    html += `
        <div class="bg-white rounded-lg shadow-sm border-l-4 border-green-500 overflow-hidden mb-6">
            <div class="px-6 py-4 bg-gradient-to-r from-green-50 to-white border-b border-gray-100">
                <h3 class="text-base font-semibold text-gray-900 flex items-center gap-2">
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
            <div class="result-card bg-white rounded-lg shadow-md overflow-hidden">
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
                    <p class="text-xs text-gray-600 mb-2 truncate">${result.file_name}</p>
                    <details class="text-sm">
                        <summary class="cursor-pointer text-indigo-600 hover:text-indigo-700 font-medium">
                            View Captions
                        </summary>
                        <ul class="mt-2 space-y-1 text-gray-700">
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
            <div class="bg-white rounded-xl shadow-md p-6 mb-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">Generated Description</h3>
                <div class="bg-gray-50 rounded-lg p-6 border border-gray-200">
                    <p class="text-gray-800 italic">"${queryData.generated_text}"</p>
                </div>
            </div>
        `;
    }

    // Generated image if exists
    if (queryData.generated_image_base64) {
        html += `
            <div class="bg-white rounded-xl shadow-md p-6 mb-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">Generated Image</h3>
                <img src="${queryData.generated_image_base64}" class="max-w-2xl mx-auto rounded-lg shadow-lg">
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

    icon.innerHTML = icons[type] || icons.info;
    messageEl.textContent = message;

    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
