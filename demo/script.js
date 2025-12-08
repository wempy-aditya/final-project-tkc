// Sample data for demo
const sampleImages = [
    {
        url: 'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400',
        caption: 'A golden retriever playing with a ball in a sunny park',
        score: 0.94
    },
    {
        url: 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400',
        caption: 'A happy dog running through green grass',
        score: 0.89
    },
    {
        url: 'https://images.unsplash.com/photo-1558788353-f76d92427f16?w=400',
        caption: 'A playful puppy in an outdoor setting',
        score: 0.87
    },
    {
        url: 'https://images.unsplash.com/photo-1477884213360-7e9d7dcc1e48?w=400',
        caption: 'A dog enjoying time in a park with trees',
        score: 0.85
    },
    {
        url: 'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=400',
        caption: 'A brown dog playing outdoors on a sunny day',
        score: 0.82
    }
];

const sampleGeneratedText = "A joyful golden retriever plays energetically in a vibrant park setting. The dog's coat gleams in the sunlight as it bounds across the lush green grass, chasing after a bright red ball. The scene captures the pure happiness and playful nature of dogs enjoying outdoor activities. Tall trees provide shade in the background, while the clear blue sky suggests a perfect day for outdoor play. The dog's tail wags enthusiastically, embodying the carefree spirit of canine companionship.";

const sampleGeneratedImage = 'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=600';

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all tabs
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

        // Add active class to clicked tab
        btn.classList.add('active');
        const tabId = btn.dataset.tab + '-tab';
        document.getElementById(tabId).classList.add('active');
    });
});

// Image upload handling
const uploadArea = document.getElementById('upload-area');
const imageUpload = document.getElementById('image-upload');
const imageSearchBtn = document.getElementById('image-search-btn');

imageUpload.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        const file = e.target.files[0];
        const reader = new FileReader();

        reader.onload = (event) => {
            uploadArea.innerHTML = `
                <img src="${event.target.result}" style="max-width: 100%; max-height: 300px; border-radius: 0.5rem;">
                <p style="margin-top: 1rem; font-weight: 600;">Image uploaded successfully!</p>
            `;
            imageSearchBtn.style.display = 'block';
        };

        reader.readAsDataURL(file);
    }
});

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--primary)';
    uploadArea.style.background = 'rgba(102, 126, 234, 0.05)';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.borderColor = 'var(--border)';
    uploadArea.style.background = 'transparent';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--border)';
    uploadArea.style.background = 'transparent';

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (event) => {
            uploadArea.innerHTML = `
                <img src="${event.target.result}" style="max-width: 100%; max-height: 300px; border-radius: 0.5rem;">
                <p style="margin-top: 1rem; font-weight: 600;">Image uploaded successfully!</p>
            `;
            imageSearchBtn.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

// Search function
function performSearch() {
    const query = document.getElementById('text-query').value;

    if (!query.trim()) {
        alert('Please enter a search query');
        return;
    }

    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';

    // Simulate API call
    setTimeout(() => {
        displayResults();
    }, 2000);
}

function performImageSearch() {
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';

    // Simulate API call
    setTimeout(() => {
        displayResults();
    }, 2000);
}

function displayResults() {
    // Hide loading
    document.getElementById('loading').style.display = 'none';
    document.getElementById('results').style.display = 'block';

    // Display retrieved images
    const imageGrid = document.getElementById('retrieved-images');
    imageGrid.innerHTML = '';

    sampleImages.forEach((img, index) => {
        const card = document.createElement('div');
        card.className = 'image-card';
        card.style.animationDelay = `${index * 0.1}s`;
        card.innerHTML = `
            <img src="${img.url}" alt="Retrieved image ${index + 1}">
            <div class="image-info">
                <span class="image-rank">Rank ${index + 1}</span>
                <span class="image-score">Score: ${img.score.toFixed(2)}</span>
                <p class="image-caption">${img.caption}</p>
            </div>
        `;
        imageGrid.appendChild(card);
    });

    // Display generated text if enabled
    const generateText = document.getElementById('generate-text').checked;
    const textSection = document.getElementById('generated-text-section');

    if (generateText) {
        textSection.style.display = 'block';
        const textDiv = document.getElementById('generated-text');
        textDiv.textContent = '';

        // Typing effect
        let i = 0;
        const typeWriter = () => {
            if (i < sampleGeneratedText.length) {
                textDiv.textContent += sampleGeneratedText.charAt(i);
                i++;
                setTimeout(typeWriter, 20);
            }
        };
        setTimeout(typeWriter, 500);
    } else {
        textSection.style.display = 'none';
    }

    // Display generated image if enabled
    const generateImage = document.getElementById('generate-image').checked;
    const imageSection = document.getElementById('generated-image-section');

    if (generateImage) {
        imageSection.style.display = 'block';
        setTimeout(() => {
            document.getElementById('generated-image').src = sampleGeneratedImage;
            document.getElementById('image-prompt').textContent =
                'Prompt: A joyful golden retriever playing in a vibrant park, sunny day, photorealistic';
        }, 3000);
    } else {
        imageSection.style.display = 'none';
    }

    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Enter key to search
document.getElementById('text-query').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        performSearch();
    }
});

// Add some interactivity to feature cards
document.querySelectorAll('.feature-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%)';
    });

    card.addEventListener('mouseleave', () => {
        card.style.background = 'var(--white)';
    });
});

// Animate elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe feature cards and architecture elements
document.querySelectorAll('.feature-card, .arch-step, .tech-item').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(el);
});
