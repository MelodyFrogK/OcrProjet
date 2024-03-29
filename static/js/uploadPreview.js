import { getDocument } from '/static/js/build/pdf.mjs';

// Set the workerSrc to the correct location
pdfjsLib.GlobalWorkerOptions.workerSrc = '/static/js/build/pdf.worker.mjs';

async function renderPDF(pdfData, canvasContainer) {
    const pdf = await getDocument({ data: pdfData }).promise;
    const page = await pdf.getPage(1);
    let viewport = page.getViewport({ scale: 1 });
    const containerWidth = canvasContainer.clientWidth;

    // Calculate the scale required to fit the PDF inside the container
    const scale = canvasContainer.offsetWidth / viewport.width;
    viewport = page.getViewport({ scale: scale });

    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.height = viewport.height;
    canvas.width = viewport.width;
    canvasContainer.appendChild(canvas);

    const renderContext = {
        canvasContext: context,
        viewport: viewport,
    };

    await page.render(renderContext).promise;
    console.log('Page rendered');
}

window.uploadImgPreview = async function uploadImgPreview() {
    const fileInput = document.getElementById('upImgFile');
    const pdfPreviewContainer = document.getElementById('pdf-preview');

    pdfPreviewContainer.innerHTML = ''; // 새 업로드를 위해 미리보기 컨테이너 초기화

    if (fileInput.files) {
        for (let file of fileInput.files) {
            if (file.type === 'application/pdf') {
                const fileReader = new FileReader();

                fileReader.onload = async function(e) {
                    try {
                        const typedArray = new Uint8Array(this.result);

                        // 각 PDF를 위한 컨테이너 생성
                        const pdfContainer = document.createElement('div');
                        pdfContainer.className = 'pdf-container'; // 스타일링을 위한 클래스 추가
                        pdfPreviewContainer.appendChild(pdfContainer);

                        await renderPDF(typedArray, pdfContainer);
                    } catch (error) {
                        console.error('PDF 렌더링 중 오류 발생', error);
                    }
                };

                fileReader.readAsArrayBuffer(file);
            }
        }
    }
}

