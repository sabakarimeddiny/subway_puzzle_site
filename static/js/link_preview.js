// $(document).ready(function() {
//     $("input[name*='link-preview-link']").each( function () {
//         var target = $(this).val();
//         var grid = $(this).parent();
//         $.ajax({
//             url: "https://api.linkpreview.net",
//             dataType: 'jsonp',
//             data: {q: target, key: '188bebe40291832604a104f9423f3dac'},
//             async: false,
//             success: function (response, target) {
//                 grid.append('<div class=link-preview><img src="'+response.image+'"><a href="'+response.url+'">'+response.title+'</a></div>');
//             }
//         });
//     });
// });
// $(document).ready(function() {
//     $('.link-preview')
//     .on('mouseenter', function(){
//         $(this).animate({ margin: -10, width: "+=20", height: "+=20" });
//     })
//     .on('mouseleave', function(){
//         $(this).animate({ margin: 0, width: "-=20", height: "-=20" });
//     })​
// });
// $('.link-preview')
//     .on('mouseenter', function(){
//         $(this).animate({ margin: -10, width: "+=20", height: "+=20" });
//     })
//     .on('mouseleave', function(){
//         $(this).animate({ margin: 0, width: "-=20", height: "-=20" });
//     })