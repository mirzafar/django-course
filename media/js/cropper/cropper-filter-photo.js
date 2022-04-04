$(document).ready(function (){
    $('.inputBox input').on('input',function (){
        var grayscale = $('#grayscale').val();
        var sepia = $('#sepia').val();
        var blur = $('#blur').val();
        var invert = $('#invert').val();
        var opacity = $('#opacity').val();
        var brightness = $('#brightness').val();
        var contrast = $('#contrast').val();
        var saturate = $('#saturate').val();

        $('.col-md-8 img,.col-md-4 .preview img').css('filter','grayscale('+ grayscale +'%) sepia('+ sepia +'%) blur('+ blur +'px) invert('+ invert +'%) opacity('+ opacity +'%) brightness('+ brightness +'%) contrast('+ contrast +'%) saturate('+ saturate +'%)');
    });


})