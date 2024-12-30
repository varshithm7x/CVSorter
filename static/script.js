// Simplified skill list
const skillCategories = {
    'Programming Languages': [
        'Python', 'Java', 'JavaScript', 'C++', 'C#', 'Ruby', 'PHP', 'Swift', 'Go',
        'TypeScript', 'Kotlin', 'R', 'MATLAB', 'Scala'
    ],
    'Web Development': [
        'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask',
        'Spring Boot', 'ASP.NET', 'Express.js'
    ],
    'Databases': [
        'MySQL', 'PostgreSQL', 'MongoDB', 'SQLite', 'Oracle', 'Redis',
        'Cassandra', 'DynamoDB'
    ],
    'Cloud & DevOps': [
        'AWS', 'Azure', 'Docker', 'Kubernetes', 'Git', 'Jenkins',
        'GitHub Actions', 'Terraform'
    ],
    'AI & ML': [
        'TensorFlow', 'PyTorch', 'Scikit-learn', 'OpenCV', 'NLP',
        'Machine Learning', 'Deep Learning'
    ],
    'Mobile Development': [
        'Android', 'iOS', 'React Native', 'Flutter', 'Xamarin',
        'Mobile App Development'
    ],
    'Tools & IDEs': [
        'VS Code', 'IntelliJ IDEA', 'Eclipse', 'Git', 'Docker',
        'Postman', 'Jira'
    ],
    'Testing': [
        'JUnit', 'Selenium', 'Jest', 'PyTest', 'Mocha',
        'Testing Libraries'
    ]
};

// Initialize the skill dropdown
function initializeSkillDropdown() {
    const dropdown = document.getElementById('skillDropdown');
    
    // Create grid container for categories
    const categoriesContainer = document.createElement('div');
    categoriesContainer.className = 'skill-categories';
    
    // Add categories to the grid
    Object.entries(skillCategories).forEach(([category, skills]) => {
        const categoryDiv = document.createElement('div');
        categoryDiv.className = 'skill-category';
        categoryDiv.innerHTML = `
            <h4>${category}</h4>
            <div class="skill-list">
                ${skills.map(skill => `
                    <label class="skill-checkbox">
                        <input type="checkbox" value="${skill}">
                        <span>${skill}</span>
                    </label>
                `).join('')}
            </div>
        `;
        categoriesContainer.appendChild(categoryDiv);
    });
    
    // Clear and append to dropdown
    dropdown.innerHTML = '';
    dropdown.appendChild(categoriesContainer);

    // Add event listeners for checkboxes
    document.querySelectorAll('.skill-checkbox input').forEach(checkbox => {
        checkbox.addEventListener('change', updateSelectedSkills);
    });
}

// Filter skills based on search
function filterSkills() {
    const searchText = document.getElementById('skillSearch').value.toLowerCase();
    const categories = document.querySelectorAll('.skill-category');
    
    categories.forEach(category => {
        let hasVisibleSkills = false;
        const skills = category.querySelectorAll('.skill-checkbox');
        
        skills.forEach(checkbox => {
            const skillText = checkbox.querySelector('span').textContent.toLowerCase();
            if (skillText.includes(searchText)) {
                checkbox.style.display = 'flex';
                hasVisibleSkills = true;
            } else {
                checkbox.style.display = 'none';
            }
        });
        
        // Show/hide the entire category based on whether it has matching skills
        category.style.display = hasVisibleSkills ? 'block' : 'none';
    });
}

// Update selected skills display
function updateSelectedSkills() {
    const selectedSkillsDiv = document.getElementById('selectedSkills');
    const selectedCheckboxes = document.querySelectorAll('.skill-checkbox input:checked');
    
    selectedSkillsDiv.innerHTML = Array.from(selectedCheckboxes).map(checkbox => `
        <div class="selected-skill">
            <span>${checkbox.value}</span>
            <button type="button" onclick="removeSkill('${checkbox.value}')">&times;</button>
        </div>
    `).join('');
}

// Remove a selected skill
function removeSkill(skillName) {
    const checkbox = document.querySelector(`.skill-checkbox input[value="${skillName}"]`);
    if (checkbox) {
        checkbox.checked = false;
        updateSelectedSkills();
    }
}

// Show/hide dropdown
function showSkillDropdown() {
    const dropdown = document.getElementById('skillDropdown');
    dropdown.style.display = 'block';
}

function hideSkillDropdown() {
    const dropdown = document.getElementById('skillDropdown');
    dropdown.style.display = 'none';
}

// Function to handle custom skill addition from the dedicated input
function handleCustomSkillAdd() {
    const input = document.getElementById('customSkillInput');
    const customSkill = input.value.trim();
    
    if (customSkill) {
        // Check if skill already exists
        const existingSkills = Array.from(document.querySelectorAll('.selected-skill'))
            .map(skill => skill.textContent.replace('×', '').trim().toLowerCase());
        
        if (existingSkills.includes(customSkill.toLowerCase())) {
            alert('This skill is already added!');
            return;
        }
        
        addSkillToSelection(customSkill, true);
        input.value = '';
    }
}

// Function to handle skill addition from search
function handleSearchSkillAdd(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        const input = document.getElementById('skillSearch');
        const skill = input.value.trim();
        
        if (skill) {
            addSkillToSelection(skill, false);
            input.value = '';
            hideSkillDropdown();
        }
    }
}

// Helper function to add skills to selection
function addSkillToSelection(skillName, isCustom) {
    const selectedSkills = document.getElementById('selectedSkills');
    const skillElement = document.createElement('div');
    skillElement.className = `selected-skill${isCustom ? ' custom' : ''}`;
    skillElement.innerHTML = `${skillName} <span class="remove-skill">×</span>`;
    
    // Add remove functionality
    skillElement.querySelector('.remove-skill').addEventListener('click', function() {
        skillElement.remove();
    });
    
    selectedSkills.appendChild(skillElement);
}

// Form submission handler
async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Show loading indicator
    toggleLoading(true);
    
    const formData = new FormData();
    
    // Add selected skills
    const selectedSkills = Array.from(document.querySelectorAll('.selected-skill'))
        .map(skill => skill.textContent.replace('×', '').trim());
    formData.append('skills', JSON.stringify(selectedSkills));
    
    // Add experience
    const experience = document.getElementById('experience').value;
    formData.append('experience', experience);
    
    // Add files
    const fileInput = document.getElementById('cvFiles');
    for (let file of fileInput.files) {
        formData.append('resumes', file);
    }
    
    try {
        const response = await fetch('/screen', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            displayResults(data.results);
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while screening CVs');
    } finally {
        toggleLoading(false);
    }
}

// Add this function to show/hide loading indicator if not already defined
function toggleLoading(show) {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (show) {
        loadingOverlay.classList.remove('hidden');
    } else {
        loadingOverlay.classList.add('hidden');
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Initialize skill dropdown
    initializeSkillDropdown();
    hideSkillDropdown();

    // Add event listeners for search input
    const searchInput = document.getElementById('skillSearch');
    searchInput.addEventListener('focus', showSkillDropdown);
    searchInput.addEventListener('keyup', filterSkills);
    searchInput.addEventListener('keypress', handleSearchSkillAdd);
    
    // Add back the close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        const dropdown = document.getElementById('skillDropdown');
        const searchContainer = document.querySelector('.skill-search-container');
        
        if (!searchContainer.contains(e.target)) {
            hideSkillDropdown();
        }
    });

    // Add custom skill button handler
    const addCustomSkillBtn = document.getElementById('addCustomSkillBtn');
    addCustomSkillBtn.addEventListener('click', handleCustomSkillAdd);

    // Add Enter key handler for custom skill input
    const customSkillInput = document.getElementById('customSkillInput');
    customSkillInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            handleCustomSkillAdd();
        }
    });

    // Add form submission handler
    const form = document.getElementById('screeningForm');
    form.addEventListener('submit', handleFormSubmit);

    // Mobile menu handler
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    const navAuth = document.querySelector('.nav-auth');

    mobileMenuBtn?.addEventListener('click', () => {
        navLinks?.classList.toggle('active');
        navAuth?.classList.toggle('active');
    });

    // Add file input handler
    const fileInput = document.querySelector('input[type="file"]');
    fileInput.addEventListener('change', handleFileInput);
});

// Update the displayResults function to show selected skills
function displayResults(results) {
    const resultsList = document.getElementById('resultsList');
    const selectedSkills = Array.from(document.querySelectorAll('.selected-skill'))
        .map(skill => skill.textContent.replace('×', '').trim());
    
    resultsList.innerHTML = results.map(result => `
        <div class="result-item collapsed">
            <div class="result-header" onclick="toggleResultView(this)">
                <div class="result-summary">
                    <h3>Rank #${result.rank}</h3>
                    <p>Candidate: ${result.name}</p>
                    <p class="score">Match Score: ${(parseFloat(result.score) * 100).toFixed(1)}%</p>
                </div>
                <button class="expand-btn">
                    <span class="expand-icon">▼</span>
                </button>
            </div>
            <div class="result-details">
                <div class="skill-matches">
                    <h4>Required Skills:</h4>
                    <div class="skill-list">
                        ${selectedSkills.map(skill => `
                            <span class="skill-tag ${result.matched_skills?.includes(skill) ? 'matched' : 'missing'}">
                                ${skill}
                            </span>
                        `).join('')}
                    </div>
                </div>
            </div>
        </div>
    `).join('');
    
    document.getElementById('results').classList.remove('hidden');
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

// Add this function to toggle the expanded view
function toggleResultView(header) {
    const resultItem = header.closest('.result-item');
    const expandIcon = header.querySelector('.expand-icon');
    
    resultItem.classList.toggle('collapsed');
    expandIcon.textContent = resultItem.classList.contains('collapsed') ? '▼' : '▲';
} 