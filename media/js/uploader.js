function uploadImage(sId){
    return new Promise(function(resolve, reject){
        var formData = new FormData();
        formData.append("file", $('#'+sId).prop('files')[0]);
        formData.append('csrfmiddlewaretoken', $('[name="csrfmiddlewaretoken"]').val());
        var url = "/api/upload/";
        $.ajax({
           type: "POST",
           url: url,
           data: formData,
           processData: false,
           contentType: false
        }).done(function(data){
            resolve(data);
        }).fail(function(data){
            reject(data);
        });
    });
}

$(document).ready(function(){

    $('[type="file"]').change(function(){
            var input_name = $(this).attr('data-name');
            var active_input = $(this).closest('tr').find('[name="'+ input_name +'"]');
            var active_image = $(this).closest('tr').find('img');
                uploadImage($(this).attr('id')).then(function(data){
                    active_input.val('upload/' + data['file_name']);
                    active_image.attr('src', '/media/upload/' + data['file_name']);
                }, function(data){
                    alert('error');
                });
        })
});