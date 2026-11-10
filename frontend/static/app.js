document.addEventListener('DOMContentLoaded', function () {
    const scanForm = document.getElementById('scanForm');
    const scanMethod = document.getElementById('scanMethod');
    const uploadGroup = document.getElementById('uploadGroup');
    const pathGroup = document.getElementById('pathGroup');
    const submitBtn = document.getElementById('submitBtn');
    const filesInput = document.getElementById('files');
    const uploadArea = document.querySelector('.file-upload-area');
    const selectedFiles = document.getElementById('selectedFiles');
    const scanStatus = document.getElementById('scanStatus');
    const progressWrap = document.getElementById('uploadProgressWrap');
    const progressBar = document.getElementById('uploadProgressBar');
    const progressText = document.getElementById('uploadProgressText');
    const progressPercent = document.getElementById('uploadProgressPercent');

    const MAX_UPLOAD_SIZE = 10 * 1024 * 1024; // Must match backend's 10 MB limit.
    const ACCEPTED_EXTENSIONS = [
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.cpp',
        '.c', '.cs', '.rb', '.php', '.r', '.scala', '.yaml', '.yml', '.json',
        '.toml', '.ini', '.cfg', '.env', '.txt'
    ];

    function formatBytes(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    }

    function setStatus(message, type) {
        if (!scanStatus) return;
        scanStatus.textContent = message || '';
        scanStatus.style.color = type === 'error' ? '#B91C1C' : type === 'success' ? '#047857' : '#4B5563';
    }

    function setProgress(percent, message) {
        const safePercent = Math.max(0, Math.min(100, Math.round(percent)));
        if (progressWrap) progressWrap.classList.remove('hidden');
        if (progressBar) progressBar.style.width = safePercent + '%';
        if (progressPercent) progressPercent.textContent = safePercent + '%';
        if (progressText && message) progressText.textContent = message;
    }

    function resetProgress() {
        if (progressWrap) progressWrap.classList.add('hidden');
        if (progressBar) progressBar.style.width = '0%';
        if (progressPercent) progressPercent.textContent = '0%';
        if (progressText) progressText.textContent = 'Preparing upload...';
    }

    function showSelectedFiles() {
        if (!selectedFiles || !filesInput) return;
        const files = Array.from(filesInput.files || []);
        if (!files.length) {
            selectedFiles.textContent = 'No files selected.';
            return;
        }

        const totalSize = files.reduce((sum, file) => sum + file.size, 0);
        const list = document.createElement('ul');
        list.style.cssText = 'margin:8px 0 0;padding-left:20px;';

        files.forEach(function (file) {
            const item = document.createElement('li');
            item.textContent = file.name + ' (' + formatBytes(file.size) + ')';
            list.appendChild(item);
        });

        selectedFiles.replaceChildren();
        const summary = document.createElement('p');
        summary.style.margin = '0';
        summary.textContent = files.length + ' file(s) selected · ' + formatBytes(totalSize) + ' total';
        selectedFiles.append(summary, list);

        if (totalSize > MAX_UPLOAD_SIZE) {
            setStatus('The selected files total ' + formatBytes(totalSize) + '. The maximum allowed upload is 10 MB.', 'error');
        } else {
            setStatus('', '');
        }
    }

    function setFiles(fileList) {
        if (!filesInput || !fileList) return;
        const transfer = new DataTransfer();
        Array.from(fileList).forEach(function (file) {
            transfer.items.add(file);
        });
        filesInput.files = transfer.files;
        showSelectedFiles();
    }

    scanMethod.addEventListener('change', function () {
        const isUpload = this.value === 'upload';
        uploadGroup.classList.toggle('hidden', !isUpload);
        pathGroup.classList.toggle('hidden', isUpload);
        setStatus('', '');
        resetProgress();
    });

    if (filesInput) {
        filesInput.addEventListener('change', showSelectedFiles);
    }

    if (uploadArea) {
        ['dragenter', 'dragover'].forEach(function (eventName) {
            uploadArea.addEventListener(eventName, function (event) {
                event.preventDefault();
                event.stopPropagation();
                uploadArea.classList.add('drag-over');
            });
        });

        ['dragleave', 'drop'].forEach(function (eventName) {
            uploadArea.addEventListener(eventName, function (event) {
                event.preventDefault();
                event.stopPropagation();
                uploadArea.classList.remove('drag-over');
            });
        });

        uploadArea.addEventListener('drop', function (event) {
            if (event.dataTransfer && event.dataTransfer.files.length) {
                setFiles(event.dataTransfer.files);
            }
        });
    }

    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        submitBtn.classList.toggle('loading', isLoading);
        const normalText = submitBtn.querySelector('.btn-text');
        const loadingText = submitBtn.querySelector('.btn-loading');
        if (normalText) normalText.classList.toggle('hidden', isLoading);
        if (loadingText) {
            loadingText.classList.toggle('hidden', !isLoading);
            loadingText.textContent = scanMethod.value === 'upload' ? 'Uploading and scanning...' : 'Scanning your code...';
        }
    }

    function handleUpload(companyName, files) {
        return new Promise(function (resolve, reject) {
            const formData = new FormData();
            files.forEach(function (file) {
                formData.append('files', file, file.name);
            });

            const xhr = new XMLHttpRequest();
            const url = '/api/scan/upload?company_name=' + encodeURIComponent(companyName);
            xhr.open('POST', url, true);
            xhr.responseType = 'text';

            xhr.upload.addEventListener('progress', function (event) {
                if (event.lengthComputable) {
                    const percent = (event.loaded / event.total) * 100;
                    setProgress(percent, percent >= 100 ? 'Upload complete. Running compliance scan...' : 'Uploading files...');
                } else {
                    setProgress(0, 'Uploading files...');
                }
            });

            xhr.addEventListener('load', function () {
                let result;
                try {
                    result = JSON.parse(xhr.responseText || '{}');
                } catch (error) {
                    reject(new Error('The server returned an unreadable response (HTTP ' + xhr.status + ').'));
                    return;
                }

                if (xhr.status >= 200 && xhr.status < 300) {
                    setProgress(100, 'Scan complete. Opening your results...');
                    resolve(result);
                } else {
                    reject(new Error(result.detail || result.message || ('Upload failed with HTTP ' + xhr.status + '.')));
                }
            });

            xhr.addEventListener('error', function () {
                reject(new Error('Network error while uploading. Please check your connection and try again.'));
            });

            xhr.addEventListener('abort', function () {
                reject(new Error('The upload was cancelled.'));
            });

            xhr.send(formData);
        });
    }

    scanForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const companyName = document.getElementById('companyName').value.trim();
        const method = scanMethod.value;

        if (!companyName) {
            setStatus('Please enter your company name.', 'error');
            document.getElementById('companyName').focus();
            return;
        }

        setStatus('', '');
        resetProgress();
        setLoading(true);

        try {
            let result;

            if (method === 'upload') {
                const files = Array.from(filesInput.files || []);

                if (files.length === 0) {
                    throw new Error('Please select at least one project file to upload.');
                }

                const totalSize = files.reduce((sum, file) => sum + file.size, 0);
                if (totalSize > MAX_UPLOAD_SIZE) {
                    throw new Error('The total selected file size is ' + formatBytes(totalSize) + '. The maximum allowed upload is 10 MB.');
                }

                const unsupported = files.filter(function (file) {
                    const name = file.name.toLowerCase();
                    return !ACCEPTED_EXTENSIONS.some(function (extension) {
                        return name.endsWith(extension);
                    });
                });
                if (unsupported.length) {
                    throw new Error('Unsupported file type: ' + unsupported.map(function (file) { return file.name; }).join(', '));
                }

                setProgress(0, 'Starting upload...');
                result = await handleUpload(companyName, files);
            } else {
                const projectPath = document.getElementById('projectPath').value.trim();
                if (!projectPath) {
                    throw new Error('Please enter a project path.');
                }

                setStatus('Submitting scan request...', 'info');
                const response = await fetch('/api/scan/path', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        company_name: companyName,
                        project_path: projectPath
                    })
                });

                const responseText = await response.text();
                let body;
                try {
                    body = JSON.parse(responseText || '{}');
                } catch (error) {
                    throw new Error('The server returned an unreadable response (HTTP ' + response.status + ').');
                }

                if (!response.ok) {
                    throw new Error(body.detail || body.message || ('Scan failed with HTTP ' + response.status + '.'));
                }
                result = body;
            }

            if (!result || !result.dashboard_url) {
                throw new Error('The scan finished, but the server did not return a dashboard URL.');
            }

            setStatus('Scan completed successfully. Redirecting to your results...', 'success');
            window.location.href = result.dashboard_url;
        } catch (error) {
            setStatus(error.message || 'An unexpected error occurred.', 'error');
            resetProgress();
        } finally {
            setLoading(false);
        }
    });

    showSelectedFiles();
});
