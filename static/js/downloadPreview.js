document.addEventListener('DOMContentLoaded', function() {
    fetch('/get-csv')
    .then(response => response.json())
    .then(data => {
        const table = document.getElementById('csv-preview-table');
        const headers = ["발급번호", "성명", "주민등록번호", "유효기간", "세균성이질", "장티프스", "파라티푸스", "폐결핵", "남은기간"]; // 'KEY_MAP'에 정의된 헤더를 기반으로 수정
        createTableHeader(table, headers); // 테이블 헤더를 생성하는 함수 호출
        // JSON 데이터를 HTML 테이블 행으로 변환
        data.forEach(record => {
            let row = table.insertRow();
            headers.forEach(header => {
                let cell = row.insertCell();
                cell.textContent = record[header];
            });
        });
    })
    .catch(error => console.error('Error:', error));
});

function createTableHeader(table, headers) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    headers.forEach(header => {
        let th = document.createElement("th");
        let text = document.createTextNode(header);
        th.appendChild(text);
        row.appendChild(th);
    });
}
