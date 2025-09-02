// DOM Elements
const jobSearchForm = document.getElementById('jobSearchForm');
const experienceSelect = document.getElementById('experience');
const jobTitleInput = document.getElementById('jobTitle');
const jobResults = document.getElementById('jobResults');

// Backend API will supply job results

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    initializePage();
});

function initializePage() {
    // Add smooth scrolling for navigation links
    addSmoothScrolling();
    
    // Add form event listeners
    addFormEventListeners();
    
    // Add scroll effects
    addScrollEffects();
    
    // Initialize floating shapes animation
    initializeFloatingShapes();
}

function addSmoothScrolling() {
    const navLinks = document.querySelectorAll('.nav-link, .footer-links a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function addFormEventListeners() {
    jobSearchForm.addEventListener('submit', handleJobSearch);
    
    // Add real-time validation
    experienceSelect.addEventListener('change', validateForm);
    jobTitleInput.addEventListener('input', validateForm);
}

function validateForm() {
    const experience = experienceSelect.value;
    const title = jobTitleInput.value.trim();
    const searchBtn = document.querySelector('.search-btn');
    
    if (experience && title) {
        searchBtn.disabled = false;
        searchBtn.style.opacity = '1';
        searchBtn.style.cursor = 'pointer';
    } else {
        searchBtn.disabled = true;
        searchBtn.style.opacity = '0.6';
        searchBtn.style.cursor = 'not-allowed';
    }
}

function handleJobSearch(e) {
    e.preventDefault();
    
    const experience = experienceSelect.value; // LinkedIn exp code 1-6
    const title = jobTitleInput.value.trim();
    
    if (!experience || !title) {
        showNotification('Please fill in all fields', 'error');
        return;
    }
    
    // Show loading state
    showLoading();
    
    // Call backend API
    fetch('/api/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, experience })
    })
    .then(async (res) => {
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.error || 'Failed to fetch jobs');
        }
        return res.json();
    })
    .then((data) => {
        const jobs = data.jobs || [];
        displayJobResults(jobs, title, experience);
    })
    .catch((error) => {
        showNotification(error.message, 'error');
        jobResults.innerHTML = '';
    })
    .finally(() => {
        hideLoading();
        document.getElementById('recommendations').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
}

// Backend handles searching; keep stub for compatibility
function searchJobs() { return []; }

function displayJobResults(jobs, title, experience) {
    if (jobs.length === 0) {
        jobResults.innerHTML = `
            <div class="no-results">
                <i class="fas fa-search"></i>
                <h3>No jobs found</h3>
                <p>No jobs match your criteria. Try adjusting your experience level or job title.</p>
            </div>
        `;
        return;
    }
    
    const experienceLabels = {
        '1': 'Internship',
        '2': 'Entry level',
        '3': 'Associate',
        '4': 'Mid-Senior',
        '5': 'Director',
        '6': 'Executive'
    };
    
    const resultsHTML = `
        <div class="search-summary">
            <h3>Showing ${jobs.length} jobs for "${title}" at ${experienceLabels[experience]} level</h3>
        </div>
        <div class="jobs-grid">
            ${jobs.map(job => `
                <div class="job-card" data-aos="fade-up">
                    <div class="job-company">${job.company || 'Company'}</div>
                    <a class="job-title" href="${job.link}" target="_blank" rel="noopener">View Job</a>
                    <div class="job-actions">
                        <a class="btn-apply" href="${job.link}" target="_blank" rel="noopener">Apply Now</a>
                        <button class="btn-save" onclick="saveJob('${job.company || ''}', '${job.link || ''}')">
                            <i class="fas fa-bookmark"></i>
                        </button>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    
    jobResults.innerHTML = resultsHTML;
    
    // Add animation classes
    const jobCards = document.querySelectorAll('.job-card');
    jobCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });
}

function showLoading() {
    jobResults.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Searching for jobs...</p>
        </div>
    `;
}

function hideLoading() {
    // Loading will be replaced by results
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
}

function applyToJob(title, company) {
    // This is where you'll connect your application system
    showNotification(`Application submitted for ${title} at ${company}!`, 'success');
}

function saveJob(title, company) {
    // This is where you'll connect your job saving system
    showNotification(`Job saved: ${title} at ${company}`, 'success');
}

function addScrollEffects() {
    // Add scroll-triggered animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animateElements = document.querySelectorAll('.feature-card, .contact-item, .section-title');
    animateElements.forEach(el => observer.observe(el));
}

function initializeFloatingShapes() {
    // Add parallax effect to floating shapes
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const shapes = document.querySelectorAll('.shape');
        
        shapes.forEach((shape, index) => {
            const speed = 0.5 + (index * 0.1);
            const yPos = -(scrolled * speed);
            shape.style.transform = `translateY(${yPos}px)`;
        });
    });
}

// Add CSS for additional elements
const additionalStyles = `
    .search-summary {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 10px;
        color: #667eea;
    }
    
    .jobs-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 1.5rem;
    }
    
    .job-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.5rem;
    }
    
    .job-badge {
        background: #667eea;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .job-actions {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
    }
    
    .btn-apply {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        flex: 1;
    }
    
    .btn-apply:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .btn-save {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
        padding: 0.75rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 50px;
    }
    
    .btn-save:hover {
        background: #667eea;
        color: white;
    }
    
    .no-results {
        text-align: center;
        padding: 3rem;
        color: #666;
    }
    
    .no-results i {
        font-size: 4rem;
        color: #ddd;
        margin-bottom: 1rem;
    }
    
    .notification {
        position: fixed;
        top: 100px;
        right: 20px;
        background: white;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        z-index: 10000;
        max-width: 350px;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-success {
        border-left: 4px solid #28a745;
    }
    
    .notification-error {
        border-left: 4px solid #dc3545;
    }
    
    .notification-info {
        border-left: 4px solid #17a2b8;
    }
    
    .notification button {
        background: none;
        border: none;
        color: #666;
        cursor: pointer;
        margin-left: auto;
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out forwards;
        opacity: 0;
        transform: translateY(30px);
    }
    
    .animate-in {
        animation: fadeInUp 0.8s ease-out forwards;
    }
    
    @media (max-width: 768px) {
        .jobs-grid {
            grid-template-columns: 1fr;
        }
        
        .job-actions {
            flex-direction: column;
        }
        
        .notification {
            right: 10px;
            left: 10px;
            max-width: none;
        }
    }
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet); 