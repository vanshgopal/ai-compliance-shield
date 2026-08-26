document.addEventListener('DOMContentLoaded', function() {
    const scanForm = document.getElementById('scanForm');
    const scanMethod = document.getElementById('scanMethod');
    const uploadGroup = document.getElementById('uploadGroup');
    const pathGroup = document.getElementById('pathGroup');
    const submitBtn = document.getElementById('submitBtn');

    scanMethod.addEventListener('change', function() {
        if (this.value === 'upload') {
            uploadGroup.classList.remove('hidden');
            pathGroup.classList.add('hidden');
        } else {
            uploadGroup.classList.add('hidden');
            pathGroup.classList.remove('hidden');
        }
    });

    scanForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const companyName = document.getElementById('companyName').value;
        const method = scanMethod.value;

        submitBtn.classList.add('loading');
        submitBtn.disabled = true;

        try {
            let response;

            if (method === 'upload') {
                const filesInput = document.getElementById('files');
                const files = filesInput.files;

                if (files.length === 0) {
                    alert('Please select files to upload');
                    submitBtn.classList.remove('loading');
                    submitBtn.disabled = false;
                    return;
                }

                const formData = new FormData();
                formData.append('company_name', companyName);

                for (let i = 0; i < files.length; i++) {
                    formData.append('files', files[i]);
                }

                response = await fetch('/api/scan/upload', {
                    method: 'POST',
                    body: formData,
                });
            } else {
                const projectPath = document.getElementById('projectPath').value;

                if (!projectPath) {
                    alert('Please enter a project path');
                    submitBtn.classList.remove('loading');
                    submitBtn.disabled = false;
                    return;
                }

                response = await fetch('/api/scan/path', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        company_name: companyName,
                        project_path: projectPath,
                    }),
                });
            }

            const result = await response.json();

            if (response.ok) {
                window.location.href = result.dashboard_url;
            } else {
                alert('Scan failed: ' + (result.detail || 'Unknown error'));
            }
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    });
});
