mapboxgl.accessToken = 'pk.eyJ1Ijoid2Vmd2ZlIiwiYSI6ImNreWthZ2ZlcjFvYm4ydm12NG02MzZldjcifQ.RsNTWvO3jnJv5nbkdkWf0w';
    
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [103.8451, 1.3817],
    zoom: 14
});

const marker1 = new mapboxgl.Marker().setLngLat([103.8489, 1.3800]).addTo(map);


$('#table').bootstrapTable({
    url: '/support/retrive',
    loadingTemplate: loadingTemplate
});


function loadingTemplate(message) {
    return '<i class="fa fa-spinner fa-spin fa-fw fa-2x"></i>';
}


function customViewFormatter(data) {
    var template = $('#questions').html();
    var view = '';

    $.each(data, function (i, row) {
        view += template.replace('%QUESTION%', row.Q)
            .replace('%ANSWER%', row.A)
    })

    return `<div class="row">${view}</div>`;
}