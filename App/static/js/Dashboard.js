$(document).ready(function () {
    /**
     AJAX POST - GET MACHINERY, MachineryWarning
     */
    $('chartjs-canvas').ready(function () {
        $.ajax({
            type: 'GET',
            url: 'PerformanceChart/',
            dataType: 'json',
            success: function (response) {
                Machinery = response;
                console("Machinery ID", Machinery.id)
            },
            error: function (error) {
                alert("Cannot fetch data")
            }
        })
    })
})
