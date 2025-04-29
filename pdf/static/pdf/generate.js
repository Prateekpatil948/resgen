// Initialize counters based on existing items
let educationCounter = document.querySelectorAll('[name^="education_"]').length > 0 ? 
    Math.ceil(document.querySelectorAll('[name^="education_"]').length / 5) : 1;
let experienceCounter = document.querySelectorAll('[name^="experience_"]').length > 0 ? 
    Math.ceil(document.querySelectorAll('[name^="experience_"]').length / 5) : 1;
let projectCounter = document.querySelectorAll('[name^="project_"]').length > 0 ? 
    Math.ceil(document.querySelectorAll('[name^="project_"]').length / 3) : 1;

// Form navigation
function nextStep(current, next) {
    if(validateStep(current)) {
        document.getElementById(`step${current}`).classList.remove('active');
        document.getElementById(`step${next}`).classList.add('active');
        document.getElementById(`step${current}-indicator`).classList.remove('active');
        document.getElementById(`step${next}-indicator`).classList.add('active');
        window.scrollTo(0, 0);
        updatePreview();
    }
}

function prevStep(current, prev) {
    document.getElementById(`step${current}`).classList.remove('active');
    document.getElementById(`step${prev}`).classList.add('active');
    document.getElementById(`step${current}-indicator`).classList.remove('active');
    document.getElementById(`step${prev}-indicator`).classList.add('active');
    window.scrollTo(0, 0);
}

// Form validation
function validateStep(step) {
    let isValid = true;
    const currentStep = document.getElementById(`step${step}`);
    
    // Basic validation for required fields
    const requiredFields = currentStep.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    if (!isValid) {
        currentStep.querySelector('.is-invalid').focus();
    }

    return isValid;
}

// Dynamic sections
function addEducation() {
    const section = document.createElement('div');
    section.className = 'dynamic-item mb-2';
    section.innerHTML = `
        <button type="button" class="remove-btn" onclick="removeSection(this)">
            <i class="fas fa-times"></i>
        </button>
        <div class="row g-2">
            <div class="col-md-6">
                <label class="form-label">Institution</label>
                <input type="text" class="form-control" name="education_${educationCounter}_school_college" oninput="updatePreview()">
            </div>
            <div class="col-md-6">
                <label class="form-label">Degree</label>
                <input type="text" class="form-control" name="education_${educationCounter}_degree" oninput="updatePreview()">
            </div>
            <div class="col-md-4">
                <label class="form-label">Start Date</label>
                <input type="text" class="form-control" name="education_${educationCounter}_start_date" placeholder="YYYY" oninput="updatePreview()">
            </div>
            <div class="col-md-4">
                <label class="form-label">End Date</label>
                <input type="text" class="form-control" name="education_${educationCounter}_end_date" placeholder="YYYY or Present" oninput="updatePreview()">
            </div>
            <div class="col-md-4">
                <label class="form-label">GPA/Score</label>
                <input type="text" class="form-control" name="education_${educationCounter}_percentage_cgpa" oninput="updatePreview()">
            </div>
        </div>
    `;
    document.getElementById('education-section').appendChild(section);
    educationCounter++;
}

function addExperience() {
    const section = document.createElement('div');
    section.className = 'dynamic-item mb-2';
    section.innerHTML = `
        <button type="button" class="remove-btn" onclick="removeSection(this)">
            <i class="fas fa-times"></i>
        </button>
        <div class="row g-2">
            <div class="col-md-6">
                <label class="form-label">Company</label>
                <input type="text" class="form-control" name="experience_${experienceCounter}_company_name" oninput="updatePreview()">
            </div>
            <div class="col-md-6">
                <label class="form-label">Position</label>
                <input type="text" class="form-control" name="experience_${experienceCounter}_role" oninput="updatePreview()">
            </div>
            <div class="col-md-6">
                <label class="form-label">Start Date</label>
                <input type="text" class="form-control" name="experience_${experienceCounter}_start_date" placeholder="MM/YYYY" oninput="updatePreview()">
            </div>
            <div class="col-md-6">
                <label class="form-label">End Date</label>
                <input type="text" class="form-control" name="experience_${experienceCounter}_end_date" placeholder="MM/YYYY or Present" oninput="updatePreview()">
            </div>
            <div class="col-12">
                <label class="form-label">Description</label>
                <textarea class="form-control" name="experience_${experienceCounter}_description" rows="2" oninput="updatePreview()"></textarea>
            </div>
        </div>
    `;
    document.getElementById('experience-section').appendChild(section);
    experienceCounter++;
}

function addProject() {
    const section = document.createElement('div');
    section.className = 'dynamic-item mb-2';
    section.innerHTML = `
        <button type="button" class="remove-btn" onclick="removeSection(this)">
            <i class="fas fa-times"></i>
        </button>
        <div class="row g-2">
            <div class="col-12">
                <label class="form-label">Project Name</label>
                <input type="text" class="form-control" name="project_${projectCounter}_project_name" oninput="updatePreview()">
            </div>
            <div class="col-12">
                <label class="form-label">Technologies Used</label>
                <input type="text" class="form-control" name="project_${projectCounter}_tech_stack" placeholder="Python, Django, React, etc." oninput="updatePreview()">
            </div>
            <div class="col-12">
                <label class="form-label">Description</label>
                <textarea class="form-control" name="project_${projectCounter}_description" rows="2" oninput="updatePreview()"></textarea>
            </div>
        </div>
    `;
    document.getElementById('project-section').appendChild(section);
    projectCounter++;
}

function removeSection(button) {
    const container = button.closest('.section-body');
    const sections = container.querySelectorAll('.dynamic-item');
    if (sections.length > 1) {
        button.closest('.dynamic-item').remove();
        updatePreview();
    } else {
        alert("You need at least one entry in this section.");
    }
}

// Preview update function
function updatePreview() {
    const template = new URLSearchParams(window.location.search).get('template') || '1';
    
    // Basic Information
    const firstName = document.querySelector('input[name="first_name"]')?.value || '';
    const lastName = document.querySelector('input[name="last_name"]')?.value || '';
    document.getElementById('preview-name').textContent = `${firstName} ${lastName}`.trim() || '[Your Name]';
    
    const email = document.querySelector('input[name="email"]')?.value || '';
    const phone = document.querySelector('input[name="phone"]')?.value || '';
    const linkedin = document.querySelector('input[name="linkedin"]')?.value || '';
    
    // Update contact info based on template
    if (template === '2') {
        // Template 2 (Modern) specific updates
        document.getElementById('preview-contact').innerHTML = `
            ${phone ? `<div class="contact-item"><i class="fas fa-phone me-2"></i> <span id="preview-phone">${phone}</span></div>` : ''}
            ${email ? `<div class="contact-item"><i class="fas fa-envelope me-2"></i> <span id="preview-email">${email}</span></div>` : ''}
            ${linkedin ? `<div class="contact-item"><i class="fab fa-linkedin me-2"></i> <span id="preview-linkedin">${linkedin}</span></div>` : ''}
        `;
    } else if (template === '3') {
        // Template 3 (Professional) specific updates
        const contactHTML = `
            <div>${phone || '[Phone]'} | ${email || '[Email]'}</div>
            <div class="social-links">
                ${linkedin ? `<a href="https://linkedin.com/in/${linkedin}" class="social-link" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn</a>` : '<span>[LinkedIn]</span>'}
                ${github ? `<a href="https://github.com/${github}" class="social-link" target="_blank"><i class="fab fa-github"></i> GitHub</a>` : '<span>[GitHub]</span>'}
            </div>
        `;
        document.getElementById('preview-contact').innerHTML = contactHTML;
    } else if (template === '4') {
        // Template 4 (Academic) specific updates
        document.getElementById('preview-contact').innerHTML = `
            ${phone ? `<span id="preview-phone">${phone}</span> | ` : ''}
            ${email ? `<span id="preview-email">${email}</span>${linkedin ? ' | ' : ''}` : ''}
            ${linkedin ? `<a href="https://linkedin.com/in/${linkedin}" target="_blank" id="preview-linkedin">${linkedin}</a>` : ''}
        `.trim() || '[Contact Information]';
    } else if (template === '5') {
        // Template 5 (Two-column) specific updates
        document.getElementById('preview-contact').innerHTML = `
            ${phone ? `<div class="contact-item"><span class="icon"><i class="fas fa-phone"></i></span>${phone}</div>` : ''}
            ${email ? `<div class="contact-item"><span class="icon"><i class="fas fa-envelope"></i></span>${email}</div>` : ''}
            ${linkedin ? `<div class="contact-item"><span class="icon"><i class="fab fa-linkedin"></i></span>linkedin.com/in/${linkedin}</div>` : ''}
        `;
    } else {
        // Template 1 (Classic) specific updates
        document.getElementById('preview-contact').innerHTML = `
            ${phone ? `<span id="preview-phone">${phone}</span> | ` : ''}
            ${email ? `<span id="preview-email">${email}</span>${linkedin ? ' | ' : ''}` : ''}
            ${linkedin ? `<span id="preview-linkedin">${linkedin}</span>` : ''}
        `.trim() || '[Contact Information]';
    }

    // Professional Summary
    const objective = document.querySelector('textarea[name="objective"]')?.value || '[Your professional summary]';
    document.getElementById('preview-objective').textContent = objective;

    // Education
    const educationSection = document.getElementById('preview-education');
    educationSection.innerHTML = '';
    const educationInputs = document.querySelectorAll('[name^="education_"]');
    const educationCount = Math.max(1, Math.ceil(educationInputs.length / 5));
    
    for (let i = 0; i < educationCount; i++) {
        const degree = document.querySelector(`input[name="education_${i}_degree"]`)?.value || '[Degree]';
        const school = document.querySelector(`input[name="education_${i}_school_college"]`)?.value || '[Institution]';
        const start = document.querySelector(`input[name="education_${i}_start_date"]`)?.value || '[Start]';
        const end = document.querySelector(`input[name="education_${i}_end_date"]`)?.value || '[End]';
        const gpa = document.querySelector(`input[name="education_${i}_percentage_cgpa"]`)?.value || '';
        
        if (template === '2') {
            const educationItem = document.createElement('div');
            educationItem.className = 'item';
            educationItem.innerHTML = `
                <div class="item-header">
                    <div class="item-title">${degree}</div>
                    <div class="item-dates">${start} - ${end}</div>
                </div>
                <div class="item-subtitle">${school}</div>
                ${gpa ? `<div class="item-subtitle">${gpa}</div>` : ''}
            `;
            educationSection.appendChild(educationItem);
        } else if (template === '3') {
            const educationItem = document.createElement('div');
            educationItem.className = 'preview-item';
            educationItem.innerHTML = `
                <div class="preview-item-header">
                    <span class="preview-item-title">${degree}</span>
                    <span class="preview-item-date">${start} – ${end}</span>
                </div>
                <div class="preview-item-subtitle">${school}</div>
                ${gpa ? `<div class="preview-item-content">GPA: ${gpa}</div>` : ''}
            `;
            educationSection.appendChild(educationItem);
        } else if (template === '4') {
            const educationItem = document.createElement('div');
            educationItem.className = 'education-title';
            educationItem.innerHTML = `
                <span>${school}</span>
                <span>${start} – ${end}</span>
            `;
            educationSection.appendChild(educationItem);
            
            const detail = document.createElement('div');
            detail.className = 'education-detail';
            detail.textContent = degree;
            educationSection.appendChild(detail);
            
            if (gpa) {
                const score = document.createElement('div');
                score.textContent = `Score: ${gpa}${parseFloat(gpa) <= 10 ? ' CGPA' : '%'}`;
                educationSection.appendChild(score);
            }
            
            const br = document.createElement('br');
            educationSection.appendChild(br);
        } else if (template === '5') {
            const educationItem = document.createElement('div');
            educationItem.className = 'education-item';
            educationItem.innerHTML = `
                <div class="job-title">
                    <span>${degree}</span>
                    <span>${start} – ${end}</span>
                </div>
                <div class="company">${school}</div>
                ${gpa ? `<div>Score: ${gpa}${parseFloat(gpa) <= 10 ? ' CGPA' : '%'}</div>` : ''}
                ${i < educationCount - 1 ? '<br>' : ''}
            `;
            educationSection.appendChild(educationItem);
        } else {
            const educationItem = document.createElement('div');
            educationItem.className = 'item';
            educationItem.innerHTML = `
                <div class="item-header">
                    <div class="item-title">${degree}</div>
                    <div class="item-dates">${start} - ${end}</div>
                </div>
                <div class="item-subtitle">${school}</div>
                ${gpa ? `<div class="item-subtitle">Score: ${gpa}</div>` : ''}
            `;
            educationSection.appendChild(educationItem);
        }
    }

    // Experience
    const experienceSection = document.getElementById('preview-experience');
    experienceSection.innerHTML = '';
    const experienceInputs = document.querySelectorAll('[name^="experience_"]');
    const experienceCount = Math.max(1, Math.ceil(experienceInputs.length / 5));
    
    for (let i = 0; i < experienceCount; i++) {
        const company = document.querySelector(`input[name="experience_${i}_company_name"]`)?.value || '[Company]';
        const position = document.querySelector(`input[name="experience_${i}_role"]`)?.value || '[Position]';
        const start = document.querySelector(`input[name="experience_${i}_start_date"]`)?.value || '[Start]';
        const end = document.querySelector(`input[name="experience_${i}_end_date"]`)?.value || '[End]';
        const description = document.querySelector(`textarea[name="experience_${i}_description"]`)?.value || '';
        
        if (template === '2') {
            const experienceItem = document.createElement('div');
            experienceItem.className = 'item';
            experienceItem.innerHTML = `
                <div class="item-title">${position}</div>
                <div class="item-subtitle">${company}</div>
                <div class="item-dates">${start} - ${end}</div>
                ${description ? `<div class="item-description">${description}</div>` : ''}
            `;
            experienceSection.appendChild(experienceItem);
        } else if (template === '3') {
            const experienceItem = document.createElement('div');
            experienceItem.className = 'preview-item';
            experienceItem.innerHTML = `
                <div class="preview-item-header">
                    <span class="preview-item-title">${position}</span>
                    <span class="preview-item-date">${start} – ${end}</span>
                </div>
                <div class="preview-item-subtitle">${company}</div>
                <div class="preview-item-content">
                    <ul>
                        ${description ? description.split('\n').filter(b => b.trim()).map(b => `<li>${b}</li>`).join('') : '<li>[Description]</li>'}
                    </ul>
                </div>
            `;
            experienceSection.appendChild(experienceItem);
        } else if (template === '4') {
            const companyDiv = document.createElement('div');
            companyDiv.className = 'company';
            companyDiv.textContent = `${company}, [Location]`;
            experienceSection.appendChild(companyDiv);
            
            const jobTitle = document.createElement('div');
            jobTitle.className = 'job-title';
            jobTitle.innerHTML = `
                <span>${position}</span>
                <span>${start} – ${end}</span>
            `;
            experienceSection.appendChild(jobTitle);
            
            const ul = document.createElement('ul');
            if (description) {
                description.split('\n').filter(b => b.trim()).forEach(b => {
                    const li = document.createElement('li');
                    li.textContent = b;
                    ul.appendChild(li);
                });
            } else {
                const li = document.createElement('li');
                li.textContent = '[Description]';
                ul.appendChild(li);
            }
            experienceSection.appendChild(ul);
        } else if (template === '5') {
            const experienceItem = document.createElement('div');
            experienceItem.className = 'experience-item';
            experienceItem.innerHTML = `
                <div class="job-title">
                    <span>${position}, ${company}</span>
                    <span>${start} – ${end}</span>
                </div>
                <ul>
                    ${description ? description.split('\n').filter(b => b.trim()).map(b => `<li>${b}</li>`).join('') : '<li>[Description]</li>'}
                </ul>
            `;
            experienceSection.appendChild(experienceItem);
        } else {
            const experienceItem = document.createElement('div');
            experienceItem.className = 'item';
            experienceItem.innerHTML = `
                <div class="item-header">
                    <div class="item-title">${position} at ${company}</div>
                    <div class="item-dates">${start} - ${end}</div>
                </div>
                ${description ? `<div class="item-description">${description}</div>` : ''}
            `;
            experienceSection.appendChild(experienceItem);
        }
    }

    // Projects
    const projectSection = document.getElementById('preview-projects');
    projectSection.innerHTML = '';
    const projectInputs = document.querySelectorAll('[name^="project_"]');
    const projectCount = Math.max(1, Math.ceil(projectInputs.length / 3));
    
    for (let i = 0; i < projectCount; i++) {
        const name = document.querySelector(`input[name="project_${i}_project_name"]`)?.value || '[Project Name]';
        const tech = document.querySelector(`input[name="project_${i}_tech_stack"]`)?.value || '';
        const description = document.querySelector(`textarea[name="project_${i}_description"]`)?.value || '';
        
        if (template === '3') {
            const projectItem = document.createElement('div');
            projectItem.className = 'preview-item';
            projectItem.innerHTML = `
                <div class="preview-item-header">
                    <span class="preview-item-title">${name}</span>
                </div>
                ${tech ? `<div class="preview-item-subtitle">Tech: ${tech}</div>` : ''}
                <div class="preview-item-content">
                    <ul>
                        ${description ? description.split('\n').filter(b => b.trim()).map(b => `<li>${b}</li>`).join('') : '<li>[Description]</li>'}
                    </ul>
                </div>
            `;
            projectSection.appendChild(projectItem);
        } else if (template === '4') {
            const projectTitle = document.createElement('div');
            projectTitle.className = 'job-title';
            projectTitle.innerHTML = `
                <span>${name}</span>
                <span>[Start] – [End]</span>
            `;
            projectSection.appendChild(projectTitle);
            
            if (tech) {
                const techDiv = document.createElement('div');
                techDiv.className = 'company';
                techDiv.textContent = `Technologies: ${tech}`;
                projectSection.appendChild(techDiv);
            }
            
            const ul = document.createElement('ul');
            if (description) {
                description.split('\n').filter(b => b.trim()).forEach(b => {
                    const li = document.createElement('li');
                    li.textContent = b;
                    ul.appendChild(li);
                });
            } else {
                const li = document.createElement('li');
                li.textContent = '[Description]';
                ul.appendChild(li);
            }
            projectSection.appendChild(ul);
        } else if (template === '5') {
            const projectItem = document.createElement('div');
            projectItem.className = 'project-item';
            projectItem.innerHTML = `
                <div class="job-title">
                    <span>${name}</span>
                    ${start || end ? `<span>${start} – ${end}</span>` : ''}
                </div>
                ${tech ? `<div>Tech: ${tech}</div>` : ''}
                <ul>
                    ${description ? description.split('\n').filter(b => b.trim()).map(b => `<li>${b}</li>`).join('') : '<li>[Description]</li>'}
                </ul>
            `;
            projectSection.appendChild(projectItem);
        } else {
            const projectItem = document.createElement('div');
            projectItem.className = 'item';
            projectItem.innerHTML = `
                <div class="item-title">${name}</div>
                ${tech ? `<div class="item-subtitle">${tech}</div>` : ''}
                ${description ? `<div class="item-description">${description}</div>` : ''}
            `;
            projectSection.appendChild(projectItem);
        }
    }

    // Skills
    const skills = document.querySelector('textarea[name="skills"]')?.value || '';
    if (template === '3') {
        const skillsContainer = document.getElementById('preview-skills');
        skillsContainer.innerHTML = '';
        if (skills) {
            skills.split('\n').forEach(skill => {
                if (skill.trim()) {
                    const skillTag = document.createElement('span');
                    skillTag.className = 'skill-tag';
                    skillTag.textContent = skill.trim();
                    skillsContainer.appendChild(skillTag);
                }
            });
        } else {
            const skillTag = document.createElement('span');
            skillTag.className = 'skill-tag';
            skillTag.textContent = '[Your skills]';
            skillsContainer.appendChild(skillTag);
        }
    } else if (template === '4') {
        const skillsContainer = document.getElementById('preview-skills');
        skillsContainer.innerHTML = '';
        if (skills) {
            skills.split('\n').forEach(skill => {
                if (skill.trim()) {
                    const li = document.createElement('li');
                    li.textContent = skill.trim();
                    skillsContainer.appendChild(li);
                }
            });
        } else {
            const li = document.createElement('li');
            li.textContent = '[Your skills]';
            skillsContainer.appendChild(li);
        }
    } else if (template === '5') {
        const skillsList = document.createElement('ul');
        if (skills) {
            skills.split('\n').forEach(skill => {
                if (skill.trim()) {
                    const li = document.createElement('li');
                    li.textContent = skill.trim();
                    skillsList.appendChild(li);
                }
            });
        } else {
            const li = document.createElement('li');
            li.textContent = '[Your skills]';
            skillsList.appendChild(li);
        }
        document.getElementById('preview-skills').innerHTML = '';
        document.getElementById('preview-skills').appendChild(skillsList);
    } else {
        document.getElementById('preview-skills').textContent = skills.replace(/\n/g, ', ') || '[Your skills]';
    }

    // Languages
    const languages = document.querySelector('textarea[name="languages"]')?.value || '';
    if (template === '3') {
        const languagesContainer = document.getElementById('preview-languages');
        languagesContainer.innerHTML = '';
        if (languages) {
            languages.split('\n').forEach(lang => {
                if (lang.trim()) {
                    const langTag = document.createElement('span');
                    langTag.className = 'skill-tag';
                    langTag.textContent = lang.trim();
                    languagesContainer.appendChild(langTag);
                }
            });
        } else {
            const langTag = document.createElement('span');
            langTag.className = 'skill-tag';
            langTag.textContent = '[Your languages]';
            languagesContainer.appendChild(langTag);
        }
    } else if (template === '4' || template === '5') {
        const languagesContainer = document.getElementById('preview-languages');
        languagesContainer.innerHTML = '';
        const languagesUl = document.createElement('ul');
        if (languages) {
            languages.split('\n').forEach(lang => {
                if (lang.trim()) {
                    const li = document.createElement('li');
                    li.textContent = lang.trim();
                    languagesUl.appendChild(li);
                }
            });
        } else {
            const li = document.createElement('li');
            li.textContent = '[Your languages]';
            languagesUl.appendChild(li);
        }
        languagesContainer.appendChild(languagesUl);
    } else {
        document.getElementById('preview-languages').textContent = languages.replace(/\n/g, ', ') || '[Your languages]';
    }

    // Hobbies
    const hobbies = document.querySelector('textarea[name="hobbies"]')?.value || '';
    if (template === '3') {
        const hobbiesContainer = document.getElementById('preview-hobbies');
        hobbiesContainer.innerHTML = '';
        if (hobbies) {
            hobbies.split('\n').forEach(hobby => {
                if (hobby.trim()) {
                    const hobbyTag = document.createElement('span');
                    hobbyTag.className = 'skill-tag';
                    hobbyTag.textContent = hobby.trim();
                    hobbiesContainer.appendChild(hobbyTag);
                }
            });
        } else {
            const hobbyTag = document.createElement('span');
            hobbyTag.className = 'skill-tag';
            hobbyTag.textContent = '[Your hobbies]';
            hobbiesContainer.appendChild(hobbyTag);
        }
    } else if (template === '4' || template === '5') {
        const hobbiesContainer = document.getElementById('preview-hobbies');
        hobbiesContainer.innerHTML = '';
        const hobbiesUl = document.createElement('ul');
        if (hobbies) {
            hobbies.split('\n').forEach(hobby => {
                if (hobby.trim()) {
                    const li = document.createElement('li');
                    li.textContent = hobby.trim();
                    hobbiesUl.appendChild(li);
                }
            });
        } else {
            const li = document.createElement('li');
            li.textContent = '[Your hobbies]';
            hobbiesUl.appendChild(li);
        }
        hobbiesContainer.appendChild(hobbiesUl);
    } else {
        document.getElementById('preview-hobbies').textContent = hobbies.replace(/\n/g, ', ') || '[Your hobbies]';
    }

    // Certifications
    const certifications = document.querySelector('textarea[name="certifications"]')?.value || '';
    if (template === '3') {
        const certsContainer = document.getElementById('preview-certifications');
        certsContainer.innerHTML = '';
        if (certifications) {
            const ul = document.createElement('ul');
            certifications.split('\n').forEach(cert => {
                if (cert.trim()) {
                    const li = document.createElement('li');
                    li.textContent = cert.trim();
                    ul.appendChild(li);
                }
            });
            certsContainer.appendChild(ul);
        } else {
            const ul = document.createElement('ul');
            const li = document.createElement('li');
            li.textContent = '[Your certifications]';
            ul.appendChild(li);
            certsContainer.appendChild(ul);
        }
    } else if (template === '4' || template === '5') {
        const certsContainer = document.getElementById('preview-certifications');
        certsContainer.innerHTML = '';
        const certsUl = document.createElement('ul');
        if (certifications) {
            certifications.split('\n').forEach(cert => {
                if (cert.trim()) {
                    const li = document.createElement('li');
                    li.textContent = cert.trim();
                    certsUl.appendChild(li);
                }
            });
        } else {
            const li = document.createElement('li');
            li.textContent = '[Your certifications]';
            certsUl.appendChild(li);
        }
        certsContainer.appendChild(certsUl);
    } else {
        document.getElementById('preview-certifications').textContent = certifications.replace(/\n/g, ', ') || '[Your certifications]';
    }
}

// Form submission handler
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('resumeForm');
    const submitBtn = document.getElementById('submitBtn');
    const closeButton = document.querySelector('[data-bs-dismiss="modal"]');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Processing...
        `;
        
        // Collect form data
        const formData = new FormData(form);
        const template = new URLSearchParams(window.location.search).get('template') || '1';
        
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => Promise.reject(err));
            }
            return response.json();
        })
        .then(responseData => {
            if (responseData.success) {
                // Load the preview content
                const previewContent = document.getElementById('previewContent');
                
                // Clone the current preview section
                const previewClone = document.querySelector('.resume-preview > div').cloneNode(true);
                previewContent.innerHTML = '';
                previewContent.appendChild(previewClone);
                
                // Set up modal buttons
                document.getElementById('downloadBtn').href = 
                    `/download/${responseData.profile_id}/?template=${template}`;
                document.getElementById('editBtn').href = 
                    `/generate/resume/?profile_id=${responseData.profile_id}&template=${template}`;
                
                // Show modal
                const previewModal = new bootstrap.Modal(document.getElementById('previewModal'));
                previewModal.show();
            } else {
                throw new Error(responseData.message || 'Failed to save resume');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error.message);
        })
        .finally(() => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = `
                {% if is_edit %}Update{% else %}Generate{% endif %} 
                <i class="fas fa-file-pdf ms-1"></i>
            `;
        });

        if (closeButton) {
            closeButton.addEventListener('click', function() {
                setTimeout(function() {
                    window.location.href = "{% url 'list' %}";
                }, 300); // Wait for modal to finish closing
            });
        }
    });
});