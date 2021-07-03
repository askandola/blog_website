tinymce.init({
    selector: '#inputPostContent',
    plugins: [
        'advlist autolink link image imagetools lists charmap print preview hr anchor pagebreak spellchecker',
        'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
        'save table emoticons contextmenu directionality template paste textcolor codesample paste help'
    ],      
    imagetools_toolbar: "rotateleft rotateright | flipv fliph | editimage imageoptions",
    toolbar: 'insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media fullpage | forecolor backcolor emoticons | codesample',
    images_upload_url: '/post/imageuploader',
    automatic_uploads: true,
    images_reuse_filename: false,
    images_upload_base_path: '/static/user_uploads/post',
    audio_template_callback: function(data) {
        return '<audio controls>' + '\n<source src="' + data.source + '"' + (data.sourcemime ? ' type="' + data.sourcemime + '"' : '') + ' />\n' + (data.altsource ? '<source src="' + data.altsource + '"' + (data.altsourcemime ? ' type="' + data.altsourcemime + '"' : '') + ' />\n' : '') + '</audio>';
    },
    codesample_languages: [
        { text: 'HTML/XML', value: 'markup' },
        { text: 'JavaScript', value: 'javascript' },
        { text: 'CSS', value: 'css' },
        { text: 'Processing', value: 'processing' },
        { text: 'Python', value: 'python' }
    ],
    width: "100%",
});
const content=document.getElementsByClassName("postContent");
for (let c in content) {
    content[c].innerHTML=content[c].innerText;
}
const cardContent=document.getElementsByClassName("card-text");
for(let c in cardContent) {
    if(typeof cardContent[c] == 'object') {
        var cardImg=cardContent[c].getElementsByTagName("img");
        var cardVideo=cardContent[c].getElementsByTagName("video");
        var cardAudio=cardContent[c].getElementsByTagName("audio");
        var cardFrame=cardContent[c].getElementsByTagName("iframe");
        for(let d in cardImg) {
            if(typeof cardImg[d] == 'object') {
                cardImg[d].style.display='none';
            }
        }
        for(let d in cardVideo) {
            if(typeof cardVideo[d] == 'object') {
                cardVideo[d].style.display='none';
            }
        }
        for(let d in cardAudio) {
            if(typeof cardAudio[d] == 'object') {
                cardAudio[d].style.display='none';
            }
        }
        for(let d in cardFrame) {
            if(typeof cardFrame[d] == 'object') {
                cardFrame[d].style.display='none';
            }
        }
    }
}