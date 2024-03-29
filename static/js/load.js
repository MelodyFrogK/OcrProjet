// load.js 파일 내용
document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // 폼 제출 기본 동작 방지

    showLoadingScreen();

    const formData = new FormData(this);
    fetch('/files', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // 여기서 서버로부터 처리 완료 응답을 받는다고 가정
    })
    .then(data => {
        window.location.href = data.redirectURL; // 파일 처리 완료 후 결과 페이지로 전환
    })
    .catch(error => {
        console.error('Upload error:', error);
    });
});

function showLoadingScreen() {
    document.body.innerHTML += `
        <div class="loading-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255, 255, 255, 0.7); display: flex; justify-content: center; align-items: center; z-index: 1000;">
            <div class="loading-text" style="font-size: 2rem; display: flex; align-items: center;">
                PDF 분석중
                <span class="dot" style="animation: bounce 1s infinite; margin-left: 5px;">.</span>
                <span class="dot" style="animation: bounce 1s infinite; animation-delay: 0.1s;">.</span>
                <span class="dot" style="animation: bounce 1s infinite; animation-delay: 0.2s;">.</span>
                <span class="dot" style="animation: bounce 1s infinite; animation-delay: 0.3s;">.</span>
            </div>
        </div>
        <style>
            @keyframes bounce {
                0%, 80%, 100% { transform: translateY(0); }
                40% { transform: translateY(-10px); }
            }
        </style>
    `;
}

function hideLoadingScreen() {
    const loadingOverlay = document.querySelector('.loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.remove();
    }
}
