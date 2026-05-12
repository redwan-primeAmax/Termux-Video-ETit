function uploadFiles() {
    const fileInput = document.getElementById('fileInput');
    const status = document.getElementById('status');
    const uploadBtn = document.getElementById('uploadBtn');

    if (fileInput.files.length === 0) {
        status.innerHTML = '<span style="color: #ff4d4d;">ভিডিও সিলেক্ট করুন!</span>';
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < fileInput.files.length; i++) {
        formData.append('files', fileInput.files[i]);
    }

    uploadBtn.disabled = true;
    uploadBtn.innerText = "Uploading...";
    status.innerHTML = '<span style="color: #00d2ff;">লোকাল ট্রান্সফার হচ্ছে...</span>';

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            status.innerHTML = '<span style="color: #00ff88;">✓ ' + data.message + '</span>';
            fileInput.value = ''; 
        } else {
            status.innerHTML = '<span style="color: #ff4d4d;">ভুল: ' + data.message + '</span>';
        }
    })
    .catch(() => {
        status.innerHTML = '<span style="color: #ff4d4d;">সার্ভারে কানেক্ট করা যাচ্ছে না!</span>';
    })
    .finally(() => {
        uploadBtn.disabled = false;
        uploadBtn.innerText = "Upload Videos";
    });
}
