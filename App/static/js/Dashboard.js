$(document).ready(function () {
    /**
     AJAX POST - GET MACHINERY, MachineryWarning
     */
    let dataset = [];
    $('chartjs-canvas').ready(function () {
        $.ajax({
            type: 'GET',
            url: 'PerformanceChart/',
            dataType: 'json',
            success: function (response) {
                data = response;
                console.log("recieved items", data.items);
                // two canvas Chart and Legent
                /*
                 chart plot the date time from when created and to current date time
                 */
                const names = data.items.map(item => item.name);
                const ticket_Date = data.items.map(item => item.created_at);
                console.log("names", names);
                console.log("ticket_Date", ticket_Date);
                dataset.push(ticket_Date);
                dataset.push(data.items.map(item => item.current_time));
                dataset.push(names);

                for (name in names) {
                    $('#legendlist').append(`
                <li>
                     ${names[name]} - ${data.items.map(item => item.status)}
                </li>
                `);
                }
            },
            error: function (error) {
                alert("Cannot fetch data")
            }
        })
        console.log("dataset", dataset);

        // Chart
        const ctx = document.getElementById('downtimechart').getContext('2d');
        const FaultChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dataset[0],
                datasets: [{
                    label: 'Downtime Chart',
                    data: dataset[1],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        })
    })


})

