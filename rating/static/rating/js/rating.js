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

function load(element, url) {
    let xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
    }

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState === XMLHttpRequest.DONE) {
            if (xmlhttp.status === 200) {
                element.innerHTML = xmlhttp.responseText;
                const allScripts = element.getElementsByTagName('script');
                for (let n = 0; n < allScripts.length; n++) {
                    eval(allScripts [n].innerHTML)//run script inside div generally not a good idea but these scripts are anyways intended to be executed.
                }
            } else {
                alert('Error');
            }
        }
    }

    xmlhttp.open('GET', url, true);
    xmlhttp.send();
}

function CreateRating(urlhash) {
    let form = document.querySelector(`#rating-${urlhash}`);
    let method = form.getAttribute('method');
    let action = form.getAttribute('action');
    let data = {
        //OBJECT INPUTS
        app_name: form.querySelector(`[name='app_name']`).value,
        model_name: form.querySelector(`[name='model_name']`).value,
        content_type: form.querySelector(`[name='content_type']`).value,
        object_id: form.querySelector(`[name='object_id']`).value,
        settings_slug: form.querySelector(`[name='settings_slug']`).value,
        rate: form.getAttribute('user_rate')
    };

    // AJAX
    let http = new XMLHttpRequest();
    http.open(method, action, true);

    http.setRequestHeader('Content-type', 'application/json');
    http.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    http.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

    http.onreadystatechange = function () {
        if (http.readyState === XMLHttpRequest.DONE) {
            if (http.status === 200) {
                const template_info = document.querySelector(`#rating-info-${urlhash}`);
                if (template_info) {
                    load(
                        document.querySelector(`#rating-info-${urlhash}`),
                        `/rating/info/${urlhash}?custom_template=${template_info.getAttribute('template')}`
                    );
                }
            } else {
                alert('ERROR in Submitting Rate!')
            }
        }
    }
    http.send(JSON.stringify(data));
}

const rating_items = document.querySelectorAll(`input[name^='rating-']`)

rating_items.forEach(function (item) {
    const urlhash = item.name.split('-')[1];
    item.addEventListener('change', function () {
        document.querySelector(`#rating-${urlhash}`).setAttribute('user_rate', this.value);
        CreateRating(urlhash);
    });
    item.addEventListener('click', function () {
        if (this.value === document.querySelector(`#rating-${urlhash}`).getAttribute('user_rate')) {
            document.querySelector(`input[name='rating-${urlhash}'][value='-1']`).checked = true;
            document.querySelector(`#rating-${urlhash}`).setAttribute('user_rate', '-1');
            CreateRating(urlhash);
        }
    })
});
