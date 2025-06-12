// Main JavaScript file for AI Resume Analyzer

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize file upload validation
    initializeFileUpload();
    
    // Initialize job selection
    initializeJobSelection();
    
    // Initialize progress animations
    initializeProgressAnimations();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
}

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializeFileUpload() {
    const fileInput = document.getElementById('resume');
    if (!fileInput) return;
    
    fileInput.addEventListener('change', function(e) {
        validateFile(e.target);
    });
    
    // Drag and drop functionality
    const uploadArea = fileInput.parentElement;
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        uploadArea.classList.add('drag-over');
    }
    
    function unhighlight() {
        uploadArea.classList.remove('drag-over');
    }
    
    uploadArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            fileInput.files = files;
            validateFile(fileInput);
        }
    }
}

function validateFile(input) {
    const file = input.files[0];
    if (!file) return;
    
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['application/pdf', 'text/plain'];
    
    // Reset previous validation
    input.classList.remove('is-invalid', 'is-valid');
    
    if (file.size > maxSize) {
        showValidationError(input, 'File size too large. Please select a file smaller than 16MB.');
        return false;
    }
    
    if (!allowedTypes.includes(file.type)) {
        showValidationError(input, 'Invalid file type. Please upload a PDF or TXT file.');
        return false;
    }
    
    // File is valid
    input.classList.add('is-valid');
    showValidationSuccess(input, `File "${file.name}" is ready for upload.`);
    return true;
}

function showValidationError(input, message) {
    input.classList.add('is-invalid');
    input.value = '';
    
    // Remove existing feedback
    const existingFeedback = input.parentElement.querySelector('.invalid-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    // Add error feedback
    const feedback = document.createElement('div');
    feedback.className = 'invalid-feedback';
    feedback.textContent = message;
    input.parentElement.appendChild(feedback);
}

function showValidationSuccess(input, message) {
    // Remove existing feedback
    const existingFeedback = input.parentElement.querySelector('.valid-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    // Add success feedback
    const feedback = document.createElement('div');
    feedback.className = 'valid-feedback';
    feedback.textContent = message;
    input.parentElement.appendChild(feedback);
}

function initializeJobSelection() {
    const checkboxes = document.querySelectorAll('input[name="jobs"]');
    if (checkboxes.length === 0) return;
    
    // Add select all functionality
    addSelectAllButton(checkboxes);
    
    // Add visual feedback for selection
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const card = this.closest('.card');
            if (this.checked) {
                card.classList.add('border-primary');
            } else {
                card.classList.remove('border-primary');
            }
        });
    });
}

function addSelectAllButton(checkboxes) {
    const firstCheckbox = checkboxes[0];
    const container = firstCheckbox.closest('.row').parentElement;
    
    // Create select all button
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'mb-3 text-end';
    
    const selectAllBtn = document.createElement('button');
    selectAllBtn.type = 'button';
    selectAllBtn.className = 'btn btn-outline-secondary btn-sm me-2';
    selectAllBtn.innerHTML = '<i class="fas fa-check-square me-1"></i>Select All';
    
    const clearAllBtn = document.createElement('button');
    clearAllBtn.type = 'button';
    clearAllBtn.className = 'btn btn-outline-secondary btn-sm';
    clearAllBtn.innerHTML = '<i class="fas fa-square me-1"></i>Clear All';
    
    buttonContainer.appendChild(selectAllBtn);
    buttonContainer.appendChild(clearAllBtn);
    
    // Insert before the jobs grid
    const jobsGrid = container.querySelector('.row');
    container.insertBefore(buttonContainer, jobsGrid);
    
    // Add event listeners
    selectAllBtn.addEventListener('click', function() {
        checkboxes.forEach(cb => {
            cb.checked = true;
            cb.dispatchEvent(new Event('change'));
        });
    });
    
    clearAllBtn.addEventListener('click', function() {
        checkboxes.forEach(cb => {
            cb.checked = false;
            cb.dispatchEvent(new Event('change'));
        });
    });
}

function initializeProgressAnimations() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    // Animate progress bars when they come into view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.style.width;
                progressBar.style.width = '0%';
                
                setTimeout(() => {
                    progressBar.style.width = width;
                }, 100);
            }
        });
    });
    
    progressBars.forEach(bar => {
        observer.observe(bar);
    });
}

function initializeSmoothScrolling() {
    // Smooth scroll to results section
    const hash = window.location.hash;
    if (hash) {
        const target = document.querySelector(hash);
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
}

// Utility functions

function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    if (!alertContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alert, alertContainer.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alert.parentElement) {
            alert.remove();
        }
    }, 5000);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for use in other scripts
window.ResumeAnalyzer = {
    showAlert,
    formatFileSize,
    debounce,
    validateFile
};
