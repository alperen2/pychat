$(function () {

    var socket = io();

    let a = window.location.href.split('/')
    if (a[a.length - 1] == '') {
        socket.emit('connected')
        socket.on('connected', (data) => {
            $('#alert').html(`
            <div class="ui container">
            <div class="ui message">
            ${data}
            </div>
            </div>
            `)
            setTimeout(() => {
                $('#alert').fadeOut()
            }, 1500)
        })
    }
    if (a[a.length - 1] == 'logout') {
        socket.emit('logout')
    }



    // socket.emit('session_control')
    // socket.on('session_control', () => {
    //     $('#login').hide()
    //     $("#message_container").fadeIn();
    // })

    // $("#loginForm").submit(function (e) {
    //     e.preventDefault()

    //     let username = $("[name=username]").val()
    //     let password = $("[name=password]").val()
    //   

    //     
    //     socket.on('loginFailed', msg => {
    //         $("#alert").fadeIn();
    //         $("#alert p").html(msg)
    //         setTimeout((e) => {
    //             $("#alert").fadeOut()
    //         }, 2000)
    //     })
    // })

    $("#message_input").keydown(e => {
        socket.emit('typing')
    })

    $("#message_input").keyup(e => {
        let z = setTimeout((e) => {
            socket.emit('notyping')
        }, 2000)
    })

    socket.on('typing', msg => {
        $('#typing').html(msg)
    })

    socket.on('notyping', msg => {
        $('#typing').html(msg)
    })


    $('#btnSend').click(function (e) {
        e.preventDefault()
        let msg = $('#message_input').val()
        socket.emit('send', msg)
        $('#messages').append(`
            <div class="item">
                <div class="content" style="text-align:right">
                    <a class="header">You</a>
                    <div class="description">${msg}</div>
                </div>
            </div>
        `)
        $('#message_input').val('')
    })

    socket.on('send', (data) => {
        $('#messages').append(`
        <div class="item">
            <div class="content">
                <a class="header">${data.username}</a>
                <div class="description">${data.msg}</div>
            </div>
        </div>
    `)
    })


});