document.addEventListener('DOMContentLoaded', () => {
    const configBtn = document.getElementById('config-btn');
    const jsonParamsBtn = document.getElementById('json-params-btn');
    const deployBtn = document.getElementById('deploy-btn');
    const analyticsBtn = document.getElementById('analytics-btn');
    const analyticsListBtn = document.getElementById('analytics-list-btn');

    const configResponse = document.getElementById('config-response');
    const jsonParamsResponse = document.getElementById('json-params-response');
    const deployResponse = document.getElementById('deploy-response');
    const analyticsResponse = document.getElementById('analytics-response');
    const analyticsListResponse = document.getElementById('analytics-list-response');

    configBtn.addEventListener('click', () => {
        window.location.href = 'https://edumat7.onrender.com/configuracao-atividade';
    });

    jsonParamsBtn.addEventListener('click', async () => {
        const response = await fetch('/json-params-atividade');
        const data = await response.json();
        jsonParamsResponse.textContent = JSON.stringify(data, null, 2);
    });

    deployBtn.addEventListener('click', async () => {
        const response = await fetch('/deploy-atividade');
        const data = await response.json();
        deployResponse.textContent = JSON.stringify(data, null, 2);
    });

    analyticsBtn.addEventListener('click', async () => {
        const response = await fetch('/analytics-atividade');
        const data = await response.json();
        analyticsResponse.textContent = JSON.stringify(data, null, 2);
    });

    analyticsListBtn.addEventListener('click', async () => {
        const response = await fetch('/lista-analytics-atividade');
        const data = await response.json();
        analyticsListResponse.textContent = JSON.stringify(data, null, 2);
    });
});
