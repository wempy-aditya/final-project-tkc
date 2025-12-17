/**
 * Main Application Logic for Multimodal RAG System
 * Handles user interactions and coordinates API calls
 */

// Global state
let currentMode = 'text';
let uploadedImage = null;
let currentSearchData = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

async function initializeApp() {
    console.log('Initializing Multimodal RAG System...');

    // Setup event listeners
    setupEventListeners();

    // Load history
    await loadHistory();

    // Health check
    try {
        const health = await api.healthCheck();
        console.log('Backend health:', health);
        updateStatusIndicator(true);
    } catch (error) {
        console.error('Backend not available:', error);
        updateStatusIndicator(false);
        showToast('Backend server not available', 'error');
    }
}

function setupEventListeners() {
    // Top-K slider
    const topKSlider = document.getElementById('top-k-slider');
    const topKValue = document.getElementById('top-k-value');
    topKSlider.addEventListener('input', (e) => {
        topKValue.textContent = e.target.value;
    });

    // Text weight slider
    const weightSlider = document.getElementById('text-weight-slider');
    const weightValue = document.getElementById('weight-value');
    weightSlider.addEventListener('input', (e) => {
        const value = parseFloat(e.target.value);
        let label = 'Balanced';
        if (value < 0.3) label = 'Image Heavy';
        else if (value > 0.7) label = 'Text Heavy';
        weightValue.textContent = `${label} (${value.toFixed(1)})`;
    });
}

function updateStatusIndicator(isOnline) {
    const indicator = document.getElementById('status-indicator');
    if (isOnline) {
        indicator.innerHTML = '<span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span><span class="text-gray-700 dark:text-gray-300 font-medium">Online</span>';
    } else {
        indicator.innerHTML = '<span class="w-2 h-2 bg-red-500 rounded-full"></span><span class="text-gray-700 dark:text-gray-300 font-medium">Offline</span>';
    }
}

/**
 * Initialize dark mode from localStorage
 */
function initializeDarkMode() {
    const isDark = localStorage.getItem('darkMode') === 'true';
    if (isDark) {
        document.documentElement.classList.add('dark');
        updateThemeIcon(true);
    }
}

/**
 * Toggle dark mode
 */
function toggleDarkMode() {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('darkMode', isDark);
    updateThemeIcon(isDark);
}

/**
 * Update theme icon
 */
function updateThemeIcon(isDark) {
    const icon = document.getElementById('theme-icon');
    if (isDark) {
        icon.className = 'fas fa-sun text-yellow-400';
    } else {
        icon.className = 'fas fa-moon text-gray-700';
    }
}

/**
 * Set search mode
 */
function setMode(mode) {
    currentMode = mode;

    // Update button styles
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.remove('mode-active');
    });
    document.querySelector(`[data-mode="${mode}"]`).classList.add('mode-active');

    // Show/hide inputs
    const textContainer = document.getElementById('text-input-container');
    const imageContainer = document.getElementById('image-input-container');
    const weightContainer = document.getElementById('weight-slider-container');
    const textInput = document.getElementById('text-query');
    const imageUpload = document.getElementById('image-upload');

    if (mode === 'text') {
        textContainer.classList.remove('opacity-50');
        imageContainer.classList.add('opacity-50');
        weightContainer.classList.add('hidden');
        textInput.disabled = false;
        imageUpload.disabled = true;
    } else if (mode === 'image') {
        textContainer.classList.add('opacity-50');
        imageContainer.classList.remove('opacity-50');
        weightContainer.classList.add('hidden');
        textInput.disabled = true;
        imageUpload.disabled = false;
    } else {
        textContainer.classList.remove('opacity-50');
        imageContainer.classList.remove('opacity-50');
        weightContainer.classList.remove('hidden');
        textInput.disabled = false;
        imageUpload.disabled = false;
    }
}

/**
 * Handle image upload
 */
function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        uploadedImage = file;

        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.getElementById('image-preview');
            const previewImg = document.getElementById('preview-img');
            previewImg.src = e.target.result;
            preview.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
}

/**
 * Perform search
 */
async function performSearch() {
    const textQuery = document.getElementById('text-query').value;
    const topK = parseInt(document.getElementById('top-k-slider').value);
    const generateText = document.getElementById('generate-text-toggle').checked;
    const generateImage = document.getElementById('generate-image-toggle').checked;
    const autoSave = document.getElementById('auto-save-toggle').checked;

    // Validation
    if (currentMode === 'text' && !textQuery) {
        showToast('Please enter a text query', 'warning');
        return;
    }
    if (currentMode === 'image' && !uploadedImage) {
        showToast('Please upload an image', 'warning');
        return;
    }
    if (currentMode === 'multimodal' && (!textQuery || !uploadedImage)) {
        showToast('Please provide both text and image', 'warning');
        return;
    }

    // Show loading
    showLoading('Searching...');

    try {
        let searchResult;
        const startTime = performance.now();

        // Perform search based on mode
        if (currentMode === 'text') {
            searchResult = await api.searchText(textQuery, topK);
        } else if (currentMode === 'image') {
            searchResult = await api.searchImage(uploadedImage, topK);
        } else {
            const textWeight = parseFloat(document.getElementById('text-weight-slider').value);
            searchResult = await api.searchMultimodal(textQuery, uploadedImage, textWeight, topK);
        }

        const retrievalTime = (performance.now() - startTime) / 1000;

        if (!searchResult.success) {
            throw new Error(searchResult.error || 'Search failed');
        }

        // Store search data
        currentSearchData = {
            mode: currentMode,
            query: textQuery,
            topK: topK,
            results: searchResult.results,
            metrics: searchResult.metrics,
            retrievalTime: retrievalTime
        };

        // Display results
        renderResults(searchResult);

        // Extract captions for generation
        const allCaptions = searchResult.results.flatMap(r => r.captions);

        // Generate text if enabled
        let textGenData = null;
        if (generateText) {
            showLoading('Generating description...');
            try {
                textGenData = await api.generateText(textQuery || '', allCaptions, currentMode);
                if (textGenData.success) {
                    renderGeneratedText(textGenData);
                    currentSearchData.generatedText = textGenData.description;
                    currentSearchData.textMetrics = textGenData.metrics;
                    currentSearchData.textGenTime = textGenData.generation_time;
                }
            } catch (error) {
                console.error('Text generation failed:', error);
                showToast('Text generation failed', 'error');
            }
        }

        // Generate image if enabled
        let imageGenData = null;
        if (generateImage) {
            showLoading('Generating image...');
            try {
                imageGenData = await api.generateImage(textQuery || '', allCaptions);
                if (imageGenData.success) {
                    renderGeneratedImage(imageGenData);
                    currentSearchData.generatedImage = imageGenData.image_base64;
                    currentSearchData.imageGenTime = imageGenData.generation_time;
                }
            } catch (error) {
                console.error('Image generation failed:', error);
                showToast(error.message, 'warning');
            }
        }

        hideLoading();

        // Calculate total time
        const totalTime = (performance.now() - startTime) / 1000;

        // Auto-save to history
        if (autoSave) {
            try {
                // Prepare query image base64 if exists
                let queryImageBase64 = null;
                if (uploadedImage) {
                    queryImageBase64 = await fileToBase64(uploadedImage);
                }

                const saveResult = await api.saveToHistory(
                    {
                        query_mode: currentMode === 'text' ? 'Text Only' :
                            currentMode === 'image' ? 'Image Only' : 'Text + Image (Multimodal)',
                        query_text: textQuery,
                        query_image_base64: queryImageBase64,
                        text_weight: currentMode === 'multimodal' ?
                            parseFloat(document.getElementById('text-weight-slider').value) : null,
                        top_k: topK
                    },
                    searchResult.results,
                    searchResult.metrics,
                    {
                        retrieval_time: retrievalTime,
                        text_gen_time: textGenData ? textGenData.generation_time : 0,
                        image_gen_time: imageGenData ? imageGenData.generation_time : 0,
                        total_time: totalTime
                    },
                    textGenData ? textGenData.description : null,
                    textGenData ? textGenData.metrics : null,
                    imageGenData ? imageGenData.image_base64 : null
                );

                if (saveResult.success) {
                    showToast(`Saved as Query #${saveResult.query_id}`, 'success');
                    loadHistory(); // Refresh history
                }
            } catch (error) {
                console.error('Failed to save to history:', error);
                showToast('Failed to save to history', 'error');
            }
        }

        showToast('Search completed!', 'success');

    } catch (error) {
        hideLoading();
        console.error('Search error:', error);
        showToast(error.message || 'Search failed', 'error');
    }
}

/**
 * Load history
 */
async function loadHistory() {
    try {
        const historyData = await api.getHistory(20);
        if (historyData.success) {
            renderHistory(historyData.queries);

            // Load stats
            const statsData = await api.getStats();
            if (statsData.success) {
                document.getElementById('stat-total').textContent = statsData.stats.total_queries;
                document.getElementById('stat-similarity').textContent = statsData.stats.avg_similarity.toFixed(3);
            }
        }
    } catch (error) {
        console.error('Failed to load history:', error);
    }
}

/**
 * Load query from history
 */
async function loadQueryFromHistory(queryId) {
    showLoading('Loading query...');

    try {
        const result = await api.getQuery(queryId);
        if (result.success) {
            renderLoadedQuery(result.query);
            hideLoading();
            showToast('Query loaded successfully', 'success');
        }
    } catch (error) {
        hideLoading();
        console.error('Failed to load query:', error);
        showToast('Failed to load query', 'error');
    }
}

/**
 * Delete query from history
 */
async function deleteQueryFromHistory(queryId, event) {
    event.stopPropagation(); // Prevent triggering load

    if (!confirm('Are you sure you want to delete this query?')) {
        return;
    }

    try {
        const result = await api.deleteQuery(queryId);
        if (result.success) {
            showToast('Query deleted', 'success');
            loadHistory(); // Refresh history
        }
    } catch (error) {
        console.error('Failed to delete query:', error);
        showToast('Failed to delete query', 'error');
    }
}

/**
 * Show loading indicator
 */
function showLoading(message = 'Processing...') {
    const loading = document.getElementById('loading-indicator');
    const loadingText = document.getElementById('loading-text');
    loadingText.textContent = message;
    loading.classList.remove('hidden');

    // Don't hide results - allow showing results while generation is in progress
    // document.getElementById('results-section').classList.add('hidden');
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    document.getElementById('loading-indicator').classList.add('hidden');
}

/**
 * Convert file to base64
 */
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Make functions globally available
window.setMode = setMode;
window.handleImageUpload = handleImageUpload;
window.performSearch = performSearch;
window.loadHistory = loadHistory;
window.loadQueryFromHistory = loadQueryFromHistory;
window.deleteQueryFromHistory = deleteQueryFromHistory;
window.toggleDarkMode = toggleDarkMode;
