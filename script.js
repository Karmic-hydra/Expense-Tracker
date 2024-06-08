document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('expense-form');
    const expensesTableBody = document.querySelector('#expenses-table tbody');
    const expensesChart = document.getElementById('expenses-chart');
    const tipsDiv = document.getElementById('tips');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const response = await fetch('/add_expense', {
            method: 'POST',
            body: formData
        });
        if (response.ok) {
            form.reset();
            loadExpenses();
        }
    });

    document.getElementById('get-tips').addEventListener('click', async () => {
        const response = await fetch('/get_tips');
        const tips = await response.text();
        tipsDiv.textContent = tips;
    });

    async function loadExpenses() {
        const response = await fetch('/expenses');
        const expenses = await response.json();
        expensesTableBody.innerHTML = '';
        expenses.forEach(expense => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${expense.expense_type}</td>
                <td>${expense.name}</td>
                <td>${expense.amount}</td>
            `;
            expensesTableBody.appendChild(row);
        });
        renderChart(expenses);
    }

    function renderChart(expenses) {
        const ctx = expensesChart.getContext('2d');
        const labels = expenses.map(expense => expense.name);
        const data = expenses.map(expense => expense.amount);
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56'],
                }]
            }
        });
    }

    loadExpenses();
});
