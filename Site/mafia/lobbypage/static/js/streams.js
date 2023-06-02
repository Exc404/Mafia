let urlTemp = window.location.host
let url = 'ws://' + urlTemp + '/ws/socket-server/' + room_name + '/'
console.log(url)
const testSocket = new WebSocket(url)
testSocket.onopen = () => testSocket.send(JSON.stringify({
    'username': user_name
}))
testSocket.onmessage = function (e) {
    let data = JSON.parse(e.data)
    if (data.type === 'chat') {
        let messages = document.getElementById('messages')
        let htmlAdding = '<div><p>' + data.message + '</p></div>'
        messages.insertAdjacentHTML('beforeend', htmlAdding)
    }
}
let inputForm = document.getElementById('messageInputForm')
inputForm.addEventListener('submit', (e) => {
    e.preventDefault()
    let message = e.target.messageForm.value
    testSocket.send(JSON.stringify({
        'message': message
    }))
    inputForm.reset()
})
window.onload = function () {
    let startButton = document.getElementById('startgame')
    startButton.onclick = function () {
        if (is_host) alert("Вы запустили игру")
        else alert("Вы не являетесь создателем комнаты")
        return false
    }
}

const APP_ID = '55fba11738094971a032a7ac307e10ed'
const CHANNEL = 'main'
const TOKEN = '007eJxTYHizIqOJ2dBymtO61SurDvFdMnrQuHvhnsBJpbdiHrwJaKtXYDA1TUtKNDQ0N7YwsDSxNDdMNDA2SjRPTDY2ME81NEhNmcNeldIQyMigdiaBmZEBAkF8FobcxMw8BgYAmVUf8w=='
let UID

const client = AgoraRTC.createClient({mode: 'rtc', codec: 'vp8'})

let localTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async () => {
    client.on('user-published', handleUserJoined)
    alert("Начался шпионаж за твоей жопой!")
    UID = await client.join(APP_ID, CHANNEL, TOKEN, null)

    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()
    let player = `<div class="video-container" id = "user-container-${UID}">
                    <div class="user-name-wrapper"><span class="user-name">Имя пользователя</span></div>
                    <div class="video-player" id = "user-${UID}"></div>
                </div>`
    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
    localTracks[1].play(`user-${UID}`)
    await client.publish([localTracks[0], localTracks[1]])
}

let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user
    console.log("AJSNCOANJS")
    console.log(mediaType)
    await client.subscribe(user, mediaType)
    if(mediaType === "video") {
        let player = document.getElementById(`user-container-${user.uid}`)
        if(player != null){
            player.remove()
        }
        player = `<div class="video-container" id = "user-container-${user.uid}">
                    <div class="user-name-wrapper"><span class="user-name">Имя пользователя</span></div>
                    <div class="video-player" id = "user-${user.uid}"></div>
                </div>`
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
        user.videoTrack.play(`user-${user.uid}`)
    }
    if(mediaType === "audio") {
        user.audioTrack.play()
    }
}

joinAndDisplayLocalStream()