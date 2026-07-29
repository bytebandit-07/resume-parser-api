let selectedFile = null;

// Drag and drop functionality
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#764ba2';
    dropZone.style.background = '#f0f2ff';
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#667eea';
    dropZone.style.background = '#f8f9ff';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#667eea';
    dropZone.style.background = '#f8f9ff';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

function handleFile(file) {
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const validExtensions = ['.pdf', '.docx'];
    
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!validExtensions.includes(fileExtension)) {
        showError('Please upload a PDF or DOCX file');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
        showError('File size must be less than 10MB');
        return;
    }
    
    selectedFile = file;
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileInfo').style.display = 'block';
    document.getElementById('dropZone').style.display = 'none';
}

{
  "rewrites": [
    { "source": "/(.*)", "destination": "/api/index.py" }
  ],
  "functions": {
    "api/index.py": {
      "maxDuration": 60
    }
  }
}
async function parseText() {
    const text = document.getElementById('resumeText').value.trim();
    
    if (!text) {
        showError('Please paste some resume text');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/resume/parse-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `text=${encodeURIComponent(text)}`
        });
        
        const responseText = await response.text();
        
        if (!response.ok) {
            let errorMsg = `Server error (${response.status})`;
            try {
                const errorJson = JSON.parse(responseText);
                errorMsg = errorJson.detail || errorMsg;
            } catch {
                errorMsg = responseText.substring(0, 200) || errorMsg;
            }
            throw new Error(errorMsg);
        }
        
        const data = JSON.parse(responseText);
        displayResult(data);
    } catch (error) {
        showError(error.message || 'Something went wrong');
    }
}
function displayResult(data) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('resultSection').style.display = 'block';
    
    // Personal Info
    document.getElementById('resName').textContent = data.parsed_data.name || 'Not found';
    document.getElementById('resEmail').textContent = data.parsed_data.email || 'Not found';
    document.getElementById('resPhone').textContent = data.parsed_data.phone || 'Not found';
    
    // Experience
    document.getElementById('resExperience').textContent = data.parsed_data.experience_years ? 
        data.parsed_data.experience_years + ' years' : 'Not found';
    document.getElementById('resSummary').textContent = data.parsed_data.summary || 'Not found';
    
    // Skills
    const skillsContainer = document.getElementById('resSkills');
    skillsContainer.innerHTML = '';
    if (data.parsed_data.skills && data.parsed_data.skills.length > 0) {
        data.parsed_data.skills.forEach(skill => {
            const tag = document.createElement('span');
            tag.className = 'skill-tag';
            tag.textContent = skill;
            skillsContainer.appendChild(tag);
        });
    } else {
        skillsContainer.innerHTML = '<p>No skills found</p>';
    }
    
    // Education
    const educationList = document.getElementById('resEducation');
    educationList.innerHTML = '';
    if (data.parsed_data.education && data.parsed_data.education.length > 0) {
        data.parsed_data.education.forEach(edu => {
            const li = document.createElement('li');
            li.textContent = edu;
            educationList.appendChild(li);
        });
    } else {
        educationList.innerHTML = '<li>No education found</li>';
    }
    
    // Raw JSON
    document.getElementById('rawJson').textContent = JSON.stringify(data.parsed_data, null, 2);
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
}

function showError(message) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('errorSection').style.display = 'block';
    document.getElementById('errorMessage').textContent = message;
}

function resetUpload() {
    selectedFile = null;
    fileInput.value = '';
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('dropZone').style.display = 'block';
}

function resetError() {
    document.getElementById('errorSection').style.display = 'none';
}

function resetAll() {
    resetUpload();
    document.getElementById('resumeText').value = '';
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
}

function copyJson() {
    const jsonText = document.getElementById('rawJson').textContent;
    navigator.clipboard.writeText(jsonText).then(() => {
        alert('JSON copied to clipboard!');
    });
}