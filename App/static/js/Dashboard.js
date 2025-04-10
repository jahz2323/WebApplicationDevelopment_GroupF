$(document).ready(function () {
    /**
     AJAX POST - GET MACHINERY, MachineryWarning
     # Authors  Jahziel
     */
    let names = [];
    let ticket_Date = [];
    let current_time = [];
    $('chartjs-canvas').ready(function () {
        $.ajax({
            type: 'GET',
            url: 'PerformanceChart/',
            dataType: 'json',
            error: function (error) {
                alert("Cannot fetch data")
            },
            success: function (response) {
                data = response;
                console.log("recieved items", data.items);
                // two canvas Chart and Legent
                /*
                 chart plot the date time from when created and to current date time
                 */
                names = data.items.map(item => item.name);
                ticket_Date = data.items.map(item => item.created_at);
                current_time = data.items.map(item => item.current_time);
                console.log("names", names);
                console.log("ticket_Date", ticket_Date);
                console.log("current_time", current_time);

                data.items.forEach(item => {
                    $('#legendlist').append(`
                <li>
                     ${item.name} - ${item.status}
                </li>
                    `);
                });
                let downtime = () => {
                    let calcdowntime = [];
                    for (let i = 0; i < ticket_Date.length; i++) {
                        let startDate = new Date(ticket_Date[i]);
                        let endDate = new Date(current_time[i]);
                        let diffInMs = endDate - startDate;
                        let diffInDays = diffInMs / (1000 * 60 * 60 * 24);
                        calcdowntime.push(diffInDays);
                    }
                    return calcdowntime;
                }
                console.log("downtime", downtime());
                // Chart
                const ctx = document.getElementById('downtimechart').getContext('2d');
                /*
                * Chart.js Bar chart
                * This chart displays the downtime of each machine in days
                * The x-axis represents the machine names
                * The y-axis represents the downtime in days
                * Downtime is calculated by days with params, ticket_Date and current_time
                 */
                const FaultChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: names,
                        datasets: [{
                            label: 'Downtime (Days)',
                            data: downtime(),
                            backgroundColor: 'rgba(20, 100, 100, 0.7)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Downtime Chart'
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Downtime (Days)'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: 'Machine name'
                                }
                            }
                        }
                    }
                })
            },
        })
    })
})

