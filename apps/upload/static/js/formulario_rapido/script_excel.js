document.getElementById('pdfInput').addEventListener('change', function(event) {
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = '';
    for (let file of event.target.files) {
        let li = document.createElement('li');
        li.textContent = file.name;
        fileList.appendChild(li);
    }
});

document.getElementById('excelInput').addEventListener('change', function(event) {
    const excelList = document.getElementById('excelList');
    excelList.innerHTML = '';
    for (let file of event.target.files) {
        let li = document.createElement('li');
        li.textContent = file.name;
        excelList.appendChild(li);
    }
});