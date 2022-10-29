console.log('haha')

var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    const chatBox = document.querySelector('#chat');
    socket.on('connect', function() {
        socket.emit('join', {});
    });
    socket.on('user-connected', function(data) {
        console.log(data)
        $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    socket.on('user-disconnected', function(data) {
        console.log(data)
        $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    socket.on('message', function(data) {
        console.log(data)
        $('#chat').val($('#chat').val() + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    $('#send').click(function(e) {
            text = $('#text').val();
            $('#text').val('');
            socket.emit('text', {msg: text});
    });


});
function leaveRoom() {
    socket.emit('left', {}, function() {
        socket.disconnect();

        window.location.href = "{{ url_for('index') }}";
    });
}