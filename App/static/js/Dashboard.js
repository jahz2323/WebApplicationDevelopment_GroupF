function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


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
    });
});

// listen on click on the button for form
// add machine
// delete machine
// update machine
// and submit the form
$(document).ready(function () {
    let add_machine = document.getElementById('add-machine-form')
    let delete_machine = document.getElementById('delete-machine-form')
    let update_machine = document.getElementById('update-machine-form')

    add_machine.addEventListener("submit", function (event) {
        event.preventDefault()
        const machine_name = document.getElementById("machine_name").value;
        const machine_description = document.getElementById("description").value;
        const machine_status = document.getElementById("status").value;
        const importanceRadios = document.getElementsByName("Importance");
        let machine_importance = null;
        for (const radio of importanceRadios) {
            if (radio.checked) {
                machine_importance = radio.value;
                break;
            }
        }
        /*
            query selector all for the checkboxes allows for multiple selections input,
            an Array object is created storing the checked values
         */

        const technicianCheckboxes = document.querySelectorAll('input[name="assigned-technicians"]:checked');
        const assigned_technicians = Array.from(technicianCheckboxes).map(cb => cb.value);
        const repairCheckboxes = document.querySelectorAll('input[name="assigned-repair"]:checked');
        const assigned_repairs = Array.from(repairCheckboxes).map(cb => cb.value);
        const collectionCheckboxes = document.querySelectorAll('input[name="collections"]:checked');
        const assigned_collections = Array.from(collectionCheckboxes).map(cb => cb.value);

        if (assigned_technicians.length === 0) {
            alert("Please assign at least one technician.");
            return;
        }
        if (assigned_repairs.length === 0) {
            alert("Please assign at least one repair person.");
            return;
        }
        if (assigned_collections.length === 0) {
            alert("Please assign at least one collection person.");
            return;
        }

        console.log("Machine Name", machine_name);
        console.log("Machine Description", machine_description);
        console.log("Machine Status", machine_status);
        console.log("Machine Importance", machine_importance);
        console.log("Assigned Technician", assigned_technicians);
        console.log("Assigned Repair", assigned_repairs);
        console.log("Assigned Collections", assigned_collections);
        // Validate if all fields are filled

        if (!machine_name || !machine_description || !machine_status || !machine_importance || !assigned_technicians || !assigned_repairs || !assigned_collections) {
            alert("Please fill in all fields.");
            return;
        }
    })
    $('#add-machine-form').validate({
        rules: {
            machine_name: {
                required: true,
                minlength: 3
            },
            description: {
                required: true,
                minlength: 3
            },
            status: {
                required: true
            },
            Importance: {
                required: true
            },
            assigned_technicians: {
                required: true
            },
            assigned_repair: {
                required: true
            },
            collections: {
                required: true
            }
        },
        messages: {
            machine_name: {
                required: "Please enter a machine name",
                minlength: "Machine name must be at least 3 characters"
            },
            description: {
                required: "Please enter a description",
                minlength: "Description must be at least 3 characters"
            },
            status: {
                required: "Please select a status"
            },
            Importance: {
                required: "Please select an importance level"
            },
            assigned_technicians: {
                required: "Please select a technician"
            },
            assigned_repair: {
                required: "Please select a repair person"
            },
            collections: {
                required: "Please select a collection"
            }
        },
        submitHandler: function (form) {
            //submit the form
            $.ajax({
                type: "POST",
                headers: {
                    "X-CSRFToken": csrftoken
                },
                url: "/Dashboard/Add_Machinery/",
                data: $(form).serialize(),
                success: function (response) {
                    alert("Machine added successfully");
                    location.reload();
                },
                error: function (error) {
                    alert("Error adding machine");
                }
            });
        }
    })
    delete_machine.addEventListener("submit", function (event) {
        event.preventDefault()
    })
    $('#delete-machine-form').validate({
        rules: {
            delete_machine: {
                required: true
            }
        },
        messages: {
            delete_machine: {
                required: "Please select a machine to delete"
            }
        },
        submitHandler: function (form) {
            //submit the form
            const machine_name = document.querySelectorAll('input[name="delete-machine"]:checked');
            const assigned_machine = Array.from(machine_name).map(cb => cb.value);
            if (assigned_machine.length == 0) {
                alert("Please select a machine to delete.");
                return;
            }
            console.log("Machine to delete ", assigned_machine);

            $.ajax({
                type: "POST",
                headers: {
                    "X-CSRFToken": csrftoken
                },
                url: "/Dashboard/delete_Machinery/",
                data: {
                    'machinery_id': assigned_machine
                },
                traditional: true, // This is important for sending an array for multiple or individual machines to delete

                success: function (response) {
                    alert("Machine deleted successfully");
                    location.reload();
                },
                error: function (error) {
                    alert("Error deleting machine");
                }
            });
        }
    }),
    update_machine.addEventListener("submit", function (event) {
        event.preventDefault()
    })
    $('#update-machine-form').validate({
        rules: {
            update_machine: {
                required: true
            },
            report: {
                required: true,
                minlength: 10
            }
        },
        messages: {
            update_machine: {
                required: "Please select a machine to update"
            }
        },
        submitHandler: function (form) {
            //submit the form
            const machine_name = document.querySelectorAll('input[name="update-machine"]:checked');
            const assigned_machine = Array.from(machine_name).map(cb => cb.value);
            console.log("Assigned_machine arr",assigned_machine )
            if (assigned_machine.length == 0) {
                alert("Please select a machine to update.");
                return;
            }
            const Report = document.getElementById("text-box").value;
            if (!Report) {
                alert("Please fill in the report.");
                return;
            }

            console.log("Machine to update ", assigned_machine);
            console.log("Report: ", Report);
            $.ajax({
                type: "POST",
                headers: {
                    "X-CSRFToken": csrftoken
                },
                traditional: true, // This is important for sending an array for multiple or individual machines to update

                url: "/Dashboard/update_Machinery/",
                data: {
                    "machinery_id": assigned_machine,
                    "Report": Report
                },
                success: function (response) {
                    alert("Machine updated successfully");
                    alert("report stored in media as: ", response);
                    location.reload();
                },
                error: function (error) {
                    alert("Error updating machine");
                }
            });
        }
    })
});

