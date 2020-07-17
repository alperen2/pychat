$(function () {
    $("#chat").hide();
    var socket = io();
    $("#formJoin").submit(function (e) {
        e.preventDefault()
        let username = $("[name=username]").val()
        socket.emit('join', username)
        $('#login').fadeOut()
        $("#chat").fadeIn();
        socket.on('joined', msg => {
            $(".modal").fadeIn().css('display', 'flex').html(msg)
            setTimeout((e) => {
                $(".modal").fadeOut()
            }, 1000)
        })
    })

    $("#m").keydown(e => {
        socket.emit('typing')
    })

    $("#m").keyup(e => {
        let z = setTimeout((e) => {
            socket.emit('notyping')
        }, 2000)
    })

    socket.on('typing', msg => {
        $('.typing').html(msg)
    })

    socket.on('notyping', msg => {
        $('.typing').html(msg)
    })


    $('#chatForm').submit(function (e) {
        e.preventDefault()
        let msg = $('#m').val()
        socket.emit('send', msg)
        $('#messages').append(`<li style="text-align:right">${msg}</li>`)
        $('#m').val('')
    })

    socket.on('send', (data) => {
        $('#messages').append(`<li><b>${data.username}</b>: ${data.msg}</li>`)
    })


});