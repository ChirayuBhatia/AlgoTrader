
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('new_log', function(data) {
    var logList = document.getElementById('log-list');
    var newLog = document.createElement('li');
    newLog.appendChild(document.createTextNode(data));
    logList.appendChild(newLog);
});
function updateClock() {
    var now = new Date();
    var hours = now.getHours().toString().padStart(2, '0');
    var minutes = now.getMinutes().toString().padStart(2, '0');
    var seconds = now.getSeconds().toString().padStart(2, '0');
    var formattedTime = hours + ':' + minutes + ':' + seconds;

    var clockElement = document.getElementById('clock');
    clockElement.textContent = formattedTime;
}

// Update the clock every second
setInterval(updateClock, 1000);

// Initial clock update
updateClock();
