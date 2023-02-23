$(`input[name^="rating-"]`)
    .change(function () {
        const urlhash = $(this)[0].name.split('-')[1];
        $(`#rating-${urlhash}`).attr('user_rate', $(this).val());
        CreateRating(urlhash);
    })
    .click(function () {
        const urlhash = $(this)[0].name.split('-')[1];
        if ($(this).val() === $(`#rating-${urlhash}`).attr('user_rate')) {
            $(`input[name="rating-${urlhash}"][value="-1"]`).prop('checked', true);
            $(`#rating-${urlhash}`).attr('user_rate', "-1");
            CreateRating(urlhash);
        }
    });


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function CreateRating(urlhash) {
    let form = $(`#rating-${urlhash}`);
    let method = form.prop('method');
    let action = form.prop('action');
    let formData = {
        //OBJECT INPUTS
        app_name: $("[name='app_name']", form).val(),
        model_name: $("[name='model_name']", form).val(),
        content_type: $("[name='content_type']", form).val(),
        object_id: $("[name='object_id']", form).val(),
        settings_slug: $("[name='settings_slug']", form).val(),
        rate: form.attr('user_rate')
    };
    $.ajax({
        type: method,
        url: action,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        data: formData,
        success: function (urlhash) {
            const template = $(`#rating-info-${urlhash}`).attr('template');
            $(`#rating-info-${urlhash}`).load(
                `/rating/info/${urlhash}?custom_template=${template}`
            );
        },
        error: function () {
            alert('ERROR in Creating Comment!')
        }
    });
}