/**
 * Created with PyCharm.
 * User: vampire
 * Date: 01.01.14
 * Time: 23:47
 * To change this template use File | Settings | File Templates.
 */
$(function()
{
    $('select#id_competences').selectize({
        plugins: ['remove_button'],
        create: function(input) {
            var txt, val;
            $.ajax({
                url: '/competence/add/',
                type: 'POST',
                data: {'competence': input, 'csrfmiddlewaretoken':$.cookie('csrftoken')},
                success: function(resp){
                    txt = resp[1];
                    val = resp[0];
                }
            });
            return {
                value: input,
                text: input
            }
        }
    });
    $('select#id_businesstypes').selectize({
        plugins: ['remove_button'],
        create: function(input) {
            var txt, val;
            $.ajax({
                url: '/btype/add/',
                type: 'POST',
                data: {'btype': input, 'csrfmiddlewaretoken':$.cookie('csrftoken')},
                success: function(resp){
                    txt = resp[1];
                    val = resp[0];
                }
            });
            return {
                value: input,
                text: input
            }
        }
    });
    $('select#id_tags').selectize({
        plugins: ['remove_button'],
        create: function(input) {
            var txt, val;
            $.ajax({
                url: '/tag/add/',
                type: 'POST',
                data: {'tag': input, 'csrfmiddlewaretoken':$.cookie('csrftoken')},
                success: function(resp){
                    txt = resp[1];
                    val = resp[0];
                }
            });
            return {
                value: input,
                text: input
            }
        }
    });
});