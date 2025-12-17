/**
 * API Client for Multimodal RAG System
 * Handles all HTTP requests to the Flask backend
 */

const API_BASE_URL = 'http://localhost:5000/api';

class API {
    constructor(baseUrl = API_BASE_URL) {
        this.baseUrl = baseUrl;
    }

    /**
     * Search by text query
     */
    async searchText(query, topK = 5) {
        const response = await fetch(`${this.baseUrl}/search/text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                top_k: topK
            })
        });

        if (!response.ok) {
            throw new Error('Search failed');
        }

        return await response.json();
    }

    /**
     * Search by image
     */
    async searchImage(imageFile, topK = 5) {
        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('top_k', topK);

        const response = await fetch(`${this.baseUrl}/search/image`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Image search failed');
        }

        return await response.json();
    }

    /**
     * Search by text + image (multimodal)
     */
    async searchMultimodal(query, imageFile, textWeight = 0.5, topK = 5) {
        const formData = new FormData();
        formData.append('query', query);
        formData.append('image', imageFile);
        formData.append('text_weight', textWeight);
        formData.append('top_k', topK);

        const response = await fetch(`${this.baseUrl}/search/multimodal`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Multimodal search failed');
        }

        return await response.json();
    }

    /**
     * Generate text description
     */
    async generateText(query, captions, queryMode = 'text') {
        const response = await fetch(`${this.baseUrl}/generate/text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                captions: captions,
                query_mode: queryMode
            })
        });

        if (!response.ok) {
            throw new Error('Text generation failed');
        }

        return await response.json();
    }

    /**
     * Generate image
     */
    async generateImage(query, captions) {
        const response = await fetch(`${this.baseUrl}/generate/image`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                captions: captions
            })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Image generation failed');
        }

        return await response.json();
    }

    /**
     * Get history
     */
    async getHistory(limit = 20) {
        const response = await fetch(`${this.baseUrl}/history?limit=${limit}`);

        if (!response.ok) {
            throw new Error('Failed to load history');
        }

        return await response.json();
    }

    /**
     * Get specific query by ID
     */
    async getQuery(queryId) {
        const response = await fetch(`${this.baseUrl}/history/${queryId}`);

        if (!response.ok) {
            throw new Error('Failed to load query');
        }

        return await response.json();
    }

    /**
     * Delete query from history
     */
    async deleteQuery(queryId) {
        const response = await fetch(`${this.baseUrl}/history/${queryId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Failed to delete query');
        }

        return await response.json();
    }

    /**
     * Get history statistics
     */
    async getStats() {
        const response = await fetch(`${this.baseUrl}/history/stats`);

        if (!response.ok) {
            throw new Error('Failed to load statistics');
        }

        return await response.json();
    }

    /**
     * Save query to history
     */
    async saveToHistory(queryData, results, retrievalMetrics, performance, generatedText = null, textMetrics = null, generatedImageBase64 = null) {
        const response = await fetch(`${this.baseUrl}/history/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query_data: queryData,
                results: results,
                retrieval_metrics: retrievalMetrics,
                performance: performance,
                generated_text: generatedText,
                text_metrics: textMetrics,
                generated_image_base64: generatedImageBase64
            })
        });

        if (!response.ok) {
            throw new Error('Failed to save to history');
        }

        return await response.json();
    }

    /**
     * Health check
     */
    async healthCheck() {
        const response = await fetch(`${this.baseUrl}/health`);

        if (!response.ok) {
            throw new Error('Health check failed');
        }

        return await response.json();
    }
}

// Create global API instance
const api = new API();
