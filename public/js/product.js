window.onload = function() {
    if (getCookie('show_filters') == 'true') {
        document.getElementById('showFilter').innerHTML = 'Filters&nbsp;&nbsp;<i class="fas fa-minus"></i>';
        document.getElementById('allFilters').style.display = 'flex';
    }
    else {
        document.getElementById('showFilter').innerHTML = 'Filters&nbsp;&nbsp;<i class="fas fa-plus"></i>';
        document.getElementById('allFilters').style.display = 'none';
    }

    var query = decodeURI(window.location.search);

    if (query.includes('A to Z')) {
        document.getElementById('sortBtnParent').classList.remove('col-md-3');
        document.getElementById('sortBtnParent').classList.add('col-md-4');
        document.getElementById('sortBtn').innerHTML = 'Sort: A to Z&nbsp;';
    } 
    else if (query.includes('price low to high')) {
        document.getElementById('sortBtnParent').classList.remove('col-md-3');
        document.getElementById('sortBtnParent').classList.add('col-md-6');
        document.getElementById('sortBtn').innerHTML = 'Sort: Price (low - high)&nbsp;';
    }
    else if (query.includes('price high to low')) {
        document.getElementById('sortBtnParent').classList.remove('col-md-3');
        document.getElementById('sortBtnParent').classList.add('col-md-6');
        document.getElementById('sortBtn').innerHTML = 'Sort: Price (high - low)&nbsp;';
    }
    else if (query.includes('newest')) {
        document.getElementById('sortBtnParent').classList.remove('col-md-3');
        document.getElementById('sortBtnParent').classList.add('col-md-4');
        document.getElementById('sortBtn').innerHTML = 'Sort: Newest&nbsp;';
    }

}


function showfilters() {
    if (getCookie('show_filters') == 'true') {
        document.getElementById('showFilter').innerHTML = 'Filters&nbsp;&nbsp;<i class="fas fa-plus"></i>';
        document.getElementById('allFilters').style.display = 'none';
        document.cookie = 'show_filters=false';
    }
    else {
        document.getElementById('showFilter').innerHTML = 'Filters&nbsp;&nbsp;<i class="fas fa-minus"></i>';
        document.getElementById('allFilters').style.display = 'flex';
        document.cookie = 'show_filters=true';
    }
}


function sortProduct(sortBy) {
    var query = window.location.search;

    if (query == '' || query.includes('?sort=')) {
        location.replace(window.location.pathname  + '?sort=' + sortBy);
    }

}


var category = document.getElementById('category').value;

function tableURL() {
    var query = decodeURI(window.location.search);

    if (query.includes('A to Z')) {
        return '/products/retrive?category=' + category + '&sort=A to Z';
    }
    else if (query.includes('price low to high')) {
        return '/products/retrive?category=' + category + '&sort=price low to high';
    }
    else if (query.includes('price high to low')) {
        return '/products/retrive?category=' + category + '&sort=price high to low';
    }
    else if (query.includes('newest')) {
        return '/products/retrive?category=' + category + '&sort=newest';
    }
    else {
        return '/products/retrive?category=' + category;
    }

}


$('#table').bootstrapTable({
    url: tableURL(),
    loadingTemplate: loadingTemplate,
    pagination: true,
    paginationLoop: false
});


function loadingTemplate(message) {
    return '<i class="fa fa-spinner fa-spin fa-fw fa-2x"></i>';
}


function customViewFormatter(data) {
    var template = $('#productCards').html();
    var view = '';

    $.each(data, function (i, row) {
        view += template.replace('%NAME%', row.name)
            .replace('%CATEGORY%', row.category)
            .replace('%PRICE%', row.price)
            .replace('%IMAGE%', row.image)
            .replace('%ID%', row.id);
    })

    var pageLinks = document.getElementsByClassName('page-link');

    document.getElementsByClassName('pagination')[0].classList.add('justify-content-center');
    pageLinks[0].innerHTML = 'Previous';
    pageLinks[pageLinks.length - 1].innerHTML = 'Next';
    return `<div class="row">${view}</div>`;
}