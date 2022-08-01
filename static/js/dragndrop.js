$(document).ready( function () {
    $('.answer-box, .lines-box').droppable({
        // tolerance: 'fit'
        tolerance: "intersect",
        drop: function (event, ui) {
            var ob = ui.draggable;
            $(this).append(ob.css({position: 'static'}));
        }
    });
    $('.line').draggable({ 
        revert: 'invalid',
        helper: 'clone',
        refreshPositions: true,
        opacity: 0.5,
    });
    $('input[name=train_1]').val('');
    $('input[name=train_2]').val('');
    $('input[name=train_3]').val('');
});

$("form").on("submit", function () {
    $('input[name=train_1]').val($('.answer-box[id=first]').children(".line").text());
    $('input[name=train_2]').val($('.answer-box[id=second]').children(".line").text());
    $('input[name=train_3]').val($('.answer-box[id=third]').children(".line").text());
});