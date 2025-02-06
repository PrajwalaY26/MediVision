document.addEventListener('DOMContentLoaded', function() {
    // Tab Switching Functionality
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Mobile Menu Toggle
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    const authButtons = document.querySelector('.auth-buttons');

    menuBtn.addEventListener('click', () => {
        navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
        authButtons.style.display = authButtons.style.display === 'flex' ? 'none' : 'flex';
    });

    // Emergency Button Functionality
    const emergencyBtn = document.querySelector('.emergency-btn');
    let emergencyTimer;
    let isEmergencyActive = false;

    emergencyBtn.addEventListener('click', () => {
        if (!isEmergencyActive) {
            startEmergencyCall();
        } else {
            cancelEmergencyCall();
        }
    });

    function startEmergencyCall() {
        isEmergencyActive = true;
        let countDown = 3;
        
        emergencyBtn.innerHTML = `Calling in ${countDown}s... (Click to cancel)`;
        emergencyBtn.style.backgroundColor = '#991b1b';

        emergencyTimer = setInterval(() => {
            countDown--;
            if (countDown > 0) {
                emergencyBtn.innerHTML = `Calling in ${countDown}s... (Click to cancel)`;
            } else {
                clearInterval(emergencyTimer);
                // In a real application, this would trigger emergency services
                alert('Emergency services have been notified.');
                resetEmergencyButton();
            }
        }, 1000);
    }

    function cancelEmergencyCall() {
        clearInterval(emergencyTimer);
        resetEmergencyButton();
    }

    function resetEmergencyButton() {
        isEmergencyActive = false;
        emergencyBtn.innerHTML = '<i class="fas fa-phone"></i><span>Emergency</span>';
        emergencyBtn.style.backgroundColor = '#dc2626';
    }

    // File Upload Handling
    const uploadSections = document.querySelectorAll('.upload-section');

    uploadSections.forEach(section => {
        const button = section.querySelector('button');
        
        // Drag and drop functionality
        section.addEventListener('dragover', (e) => {
            e.preventDefault();
            section.style.backgroundColor = '#e5e7eb';
        });

        section.addEventListener('dragleave', () => {
            section.style.backgroundColor = '#f3f4f6';
        });

        section.addEventListener('drop', (e) => {
            e.preventDefault();
            section.style.backgroundColor = '#f3f4f6';
            handleFiles(e.dataTransfer.files);
        });

        // Click to upload
        button.addEventListener('click', () => {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = 'image/*';
            
            input.onchange = (e) => handleFiles(e.target.files);
            input.click();
        });
    });

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    // In a real application, send this to server
                    showUploadSuccess(file.name);
                };
                reader.readAsDataURL(file);
            } else {
                alert('Please upload an image file.');
            }
        }
    }

    function showUploadSuccess(fileName) {
        const toast = document.createElement('div');
        toast.className = 'upload-toast';
        toast.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <span>${fileName} uploaded successfully!</span>
        `;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    // Medicine Tracker Functionality
    const addMedicineBtn = document.querySelector('.btn-icon');
    
    if (addMedicineBtn) {
        addMedicineBtn.addEventListener('click', () => {
            showAddMedicineModal();
        });
    }

    function showAddMedicineModal() {
        const modal = document.createElement('div');
        modal.className = 'medicine-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h3>Add New Medicine</h3>
                <form id="add-medicine-form">
                    <div class="form-group">
                        <label>Medicine Name</label>
                        <input type="text" required name="medicine" placeholder="Enter medicine name">
                    </div>
                    <div class="form-group">
                        <label>Dosage</label>
                        <input type="text" required name="dosage" placeholder="Enter dosage">
                    </div>
                    <div class="form-group">
                        <label>Time</label>
                        <select required name="time">
                            <option value="breakfast">Breakfast</option>
                            <option value="lunch">Lunch</option>
                            <option value="dinner">Dinner</option>
                        </select>
                    </div>
                    <div class="button-group">
                        <button type="button" class="btn-secondary" onclick="this.closest('.medicine-modal').remove()">Cancel</button>
                        <button type="submit" class="btn-primary">Add Medicine</button>
                    </div>
                </form>
            </div>
        `;

        document.body.appendChild(modal);

        const form = modal.querySelector('form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            addMedicineToSchedule(
                formData.get('medicine'),
                formData.get('dosage'),
                formData.get('time')
            );
            modal.remove();
        });
    }

    function addMedicineToSchedule(medicine, dosage, time) {
        const scheduleCard = document.querySelector(`.schedule-card:has(h4:contains('${capitalize(time)}')`);
        if (scheduleCard) {
            const medicineList = scheduleCard.querySelector('.medicine-list');
            const medicineItem = document.createElement('div');
            medicineItem.className = 'medicine-item';
            medicineItem.innerHTML = `
                <span>${medicine}</span>
                <span class="dosage">${dosage}</span>
            `;
            medicineList.appendChild(medicineItem);
        }
    }

    function capitalize(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    // Add some CSS for the new elements
    const style = document.createElement('style');
    style.textContent = `
        .upload-toast {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #10b981;
            color: white;
            padding: 1rem 2rem;
            border-radius: 9999px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }

        .medicine-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }

        .modal-content {
            background: white;
            padding: 2rem;
            border-radius: 1rem;
            width: 90%;
            max-width: 500px;
        }

        .form-group {
            margin-bottom: 1rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
        }

        .form-group input,
        .form-group select {
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #e5e7eb;
            border-radius: 0.5rem;
        }

        .button-group {
            display: flex;
            justify-content: flex-end;
            gap: 1rem;
            margin-top: 2rem;
        }
    `;
    document.head.appendChild(style);
});



