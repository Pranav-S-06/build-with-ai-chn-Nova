document.addEventListener('DOMContentLoaded', () => {
    // Tab Switching Logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.add('hidden'));
            
            btn.classList.add('active');
            document.getElementById(btn.dataset.tab).classList.remove('hidden');
        });
    });

    // Image Upload Preview Logic
    const dropZone = document.getElementById('drop-zone');
    const imageUpload = document.getElementById('image-upload');
    const imagePreview = document.getElementById('image-preview');
    const placeholder = document.querySelector('.upload-placeholder');
    let selectedFile = null;

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    imageUpload.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file.');
            return;
        }
        selectedFile = file;
        
        // Update input element files manually if needed (for form submission)
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        imageUpload.files = dataTransfer.files;

        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.classList.remove('hidden');
            placeholder.classList.add('hidden');
        };
        reader.readAsDataURL(file);
    }

    // Predict Disease Form Submission
    const predictForm = document.getElementById('predict-form');
    const predictBtn = document.getElementById('predict-btn');
    const predictResult = document.getElementById('predict-result');
    const btnText = predictBtn.querySelector('.btn-text');
    const spinner = predictBtn.querySelector('.spinner');

    predictForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!selectedFile) {
            alert('Please upload an image first.');
            return;
        }

        // UI Loading State
        btnText.classList.add('hidden');
        spinner.classList.remove('hidden');
        predictBtn.disabled = true;
        predictResult.classList.add('hidden');

        try {
            const formData = new FormData(predictForm);
            
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Prediction failed');
            }

            const data = await response.json();
            displayPredictionResult(data);

        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
            predictBtn.disabled = false;
        }
    });

    function displayPredictionResult(data) {
        const { weather, adjusted_result } = data;
        
        // Update Disease
        document.getElementById('disease-name').textContent = adjusted_result.final_prediction;
        
        // Update Confidence
        const confPercent = Math.round(adjusted_result.confidence * 100);
        document.getElementById('confidence-text').textContent = `${confPercent}%`;
        document.getElementById('confidence-bar').style.width = '0%';
        setTimeout(() => {
            document.getElementById('confidence-bar').style.width = `${confPercent}%`;
        }, 100);

        // Update Weather Context
        document.getElementById('w-temp').textContent = Math.round(weather.temperature);
        document.getElementById('w-humidity').textContent = weather.humidity;

        // Update Heuristics List
        const hList = document.getElementById('heuristics-list');
        hList.innerHTML = '';
        if (adjusted_result.heuristics_applied && adjusted_result.heuristics_applied.length > 0) {
            adjusted_result.heuristics_applied.forEach(h => {
                const li = document.createElement('li');
                li.textContent = h;
                hList.appendChild(li);
            });
        } else {
            hList.innerHTML = '<li>No weather heuristics significantly altered this prediction.</li>';
        }

        predictResult.classList.remove('hidden');
        predictResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Suggest Crop Form Submission
    const suggestForm = document.getElementById('suggest-form');
    const suggestBtn = document.getElementById('suggest-btn');
    const suggestResult = document.getElementById('suggest-result');
    const sBtnText = suggestBtn.querySelector('.btn-text');
    const sSpinner = suggestBtn.querySelector('.spinner');

    suggestForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // UI Loading State
        sBtnText.classList.add('hidden');
        sSpinner.classList.remove('hidden');
        suggestBtn.disabled = true;
        suggestResult.classList.add('hidden');

        try {
            const location = document.getElementById('s-location').value;
            
            const response = await fetch(`/suggest?location=${encodeURIComponent(location)}`);

            if (!response.ok) {
                throw new Error('Suggestion failed');
            }

            const data = await response.json();
            displaySuggestResult(data);

        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            sBtnText.classList.remove('hidden');
            sSpinner.classList.add('hidden');
            suggestBtn.disabled = false;
        }
    });

    function displaySuggestResult(data) {
        const { suggestion } = data;
        
        document.getElementById('s-crop-name').textContent = suggestion.suggested_crop;
        document.getElementById('s-reasoning').textContent = suggestion.reasoning;
        
        document.getElementById('s-demand').textContent = suggestion.details.market_demand;
        document.getElementById('s-profit').textContent = suggestion.details.profit_margin;
        
        const idealT = suggestion.details.ideal_temp;
        document.getElementById('s-temp-range').textContent = `${idealT[0]}-${idealT[1]}°C`;

        suggestResult.classList.remove('hidden');
        suggestResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});
