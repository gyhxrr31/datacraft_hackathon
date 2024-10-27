let chart; // Переменная для диаграммы Chart.js

async function generateReport() {
    const title = document.getElementById('reportTitle').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const reportType = document.getElementById('reportType').value;

    const reportData = {
        title: title,
        start_date: startDate,
        end_date: endDate,
        type: reportType
    };

    try {
        const response = await fetch('http://localhost:8000/generate_report/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reportData)
        });
        
        const data = await response.json();

        // Отображаем текстовую информацию отчета
        document.getElementById('result').innerText = 
            `Отчет: ${data.title}\nПериод: ${data.start_date} - ${data.end_date}\nТип: ${data.type}`;

        // Отображаем диаграмму на основе данных
        renderChart(data);
    } catch (error) {
        console.error('Ошибка:', error);
        document.getElementById('result').innerText = 'Ошибка при генерации отчета';
    }
}

// Функция для построения диаграммы с Chart.js
function renderChart(data) {
    // Очищаем предыдущую диаграмму, если она есть
    if (chart) {
        chart.destroy();
    }
    
    // Отображаем контейнер диаграммы
    document.getElementById('chartContainer').style.display = 'block';

    const ctx = document.getElementById('reportChart').getContext('2d');
    
    // Пример: на основе типа отчета выбираем тип диаграммы
    let chartType;
    let chartData;
    
    if (data.type === "sales") {
        chartType = 'bar';
        chartData = {
            labels: data.labels,
            datasets: [{
                label: 'Продажи',
                data: data.values,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        };
    } else if (data.type === "inventory") {
        chartType = 'pie';
        chartData = {
            labels: data.labels,
            datasets: [{
                label: 'Запасы',
                data: data.values,
                backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56'],
            }]
        };
    } else if (data.type === "performance") {
        chartType = 'line';
        chartData = {
            labels: data.labels,
            datasets: [{
                label: 'Производительность',
                data: data.values,
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 2
            }]
        };
    }

    chart = new Chart(ctx, {
        type: chartType,
        data: chartData,
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

document.getElementById("uploadForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const fileInput = document.getElementById("csvFileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Пожалуйста, выберите файл перед загрузкой.");
        return;
    }

    // Создаем FormData и добавляем файл
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://localhost:8000/api/upload-csv/", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Ошибка загрузки файла.");
        }

        const result = await response.json();
        console.log("Файл успешно загружен:", result);
        alert("Файл успешно загружен!");
    } catch (error) {
        console.error("Ошибка:", error);
        alert("Произошла ошибка при загрузке файла.");
    }
});