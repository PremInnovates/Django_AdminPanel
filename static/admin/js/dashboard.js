const ctx = document.getElementById('usersChart');

new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Users', 'Operators'],
        datasets: [{
            data: [8, 3],
            backgroundColor: ['#00ffcc', '#3399ff']
        }]
    }
});
