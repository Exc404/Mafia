let urlTemp = window.location.host

let url = 'ws://' + urlTemp + '/ws/socket-server/' + room_name + '/'

console.log(url)

const testSocket = new WebSocket(url)

testSocket.onopen = () => testSocket.send(JSON.stringify({
    'username': user_name
}))

let inputForm = document.getElementById('messageInputForm')

inputForm.addEventListener('submit', (e) => {
    e.preventDefault()
    let message = e.target.messageForm.value
    if (message === "iliveindarkness") {chatlock = false} // это надо удалить...
    testSocket.send(JSON.stringify({
        'message': message
    }))
    inputForm.reset()
})

window.onload = function () {
    let startButton = document.getElementById('startgame')
    startButton.onclick = function () {
        if (is_host) {
            alert("Вы запустили игру")
        }
        else alert("Вы не являетесь создателем комнаты")
        return false
    }
}

const APP_ID = '55fba11738094971a032a7ac307e10ed'
let CHANNEL = room_name
let TOKEN = token
let UID
let UID_ARR = []
let IS_NICK_WRITTEN = []

const client = AgoraRTC.createClient({mode: 'rtc', codec: 'vp8'})

let localTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async () => {
    document.getElementById('room-name').innerText = CHANNEL
    client.on('user-published', handleUserJoined)
    client.on('user-left', handleUserLeft)
    alert("Начался шпионаж за твоей жопой!")
    UID = await client.join(APP_ID, CHANNEL, TOKEN, null)
    setInterval(() => testSocket.send(JSON.stringify({
        'user_name' : user_name,
        'uid' : UID
    })), 100)
    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()
    let player = `<div class="video-container" id = "user-container-${UID}">
                    <div class="user-name-wrapper"><span class="user-name">${user_name}</span></div>
                    <div class="video-player" id = "user-${UID}"></div>
                    <div class = "icon-wrapper">
                    <img class = "control-icon" id = "vote-${UID}" src = "/./static/img/votemark.jpg"/>
                    </div>
                </div>`
    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
    //document.getElementById(`vote-${UID}`).onclick = vote
    localTracks[1].play(`user-${UID}`)
    await client.publish([localTracks[0], localTracks[1]])
}

let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user
    await client.subscribe(user, mediaType)
    if(mediaType === "video") {
        let player = document.getElementById(`user-container-${user.uid}`)
        if(player != null){
            IS_NICK_WRITTEN[UID_ARR.indexOf(user.uid.toString())] = false
            player.remove()
        }
        player = `<div class="video-container" id = "user-container-${user.uid}">
                    <div class="video-player" id = "user-${user.uid}"></div>
                    <div class = "icon-wrapper">
                    <img class = "control-icon" id = "vote-${user.uid}" src = "/./static/img/votemark.jpg"/>
                    </div>
                </div>`
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
        //document.getElementById(`vote-${user.uid}`).onclick = vote
        user.videoTrack.play(`user-${user.uid}`)
    }
    if(mediaType === "audio") {
        user.audioTrack.play()
    }
}

let handleUserLeft = async (user) => {
    UID_ARR = UID_ARR.map(el => el === user.uid.toString() ? 0 : el)
    for(let i = 0; i < UID_ARR.length; i++)
        if(UID_ARR[i] === 0)
            IS_NICK_WRITTEN[i] = 0
    UID_ARR = UID_ARR.filter(el => el === 0 ? false : true)
    IS_NICK_WRITTEN = IS_NICK_WRITTEN.filter(el => el === 0 ? false : true)
    delete remoteUsers[user.uid]
    document.getElementById(`user-container-${user.uid}`).remove()
}

let leaveAndRemoveLocalStream = async () => {
    for (let i = 0; localTracks.length > i; i++) {
        localTracks[i].stop()
        localTracks[i].close()
    }
    await client.leave()
    window.close()
    window.open('/', '_self')
}

let toggleCamera = async (e) => {
    if(localTracks[1].muted) {
        await localTracks[1].setMuted(false)
        e.target.style.backgroundColor = '#fff'
    }
    else {
        await localTracks[1].setMuted(true)
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
    }
}

let toggleMic = async (e) => {
    if(localTracks[0].muted) {
        await localTracks[0].setMuted(false)
        e.target.style.backgroundColor = '#fff'
    }
    else {
        await localTracks[0].setMuted(true)
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
    }
}

// let vote = function (e) {
//     if (votelock === false){
//         console.log("VOTE: ГОЛОСОВАНИЕ")
//         let votename = e.target.id
//         votelock = true
//         console.log("VOTE votename:",votename)
//         testSocket.send(JSON.stringify({
//             'vote_uid' : votename
//         }))
//     }
//     else {console.log("VOTE: Сейчас не ваше время голосовать.")}
// }


testSocket.onmessage = function (e) {
    let data = JSON.parse(e.data)
    if (data.type === 'chat') {
        let messages = document.getElementById('messages')
        htmlAdding = '<div><p>' + data.message + '</p></div>'
        messages.insertAdjacentHTML('beforeend', htmlAdding)
    }
    if(data.type === 'user_info' && data.uid != UID.toString()) {
        if(UID_ARR.indexOf(data.uid) === -1) {
            UID_ARR.push(data.uid)
            IS_NICK_WRITTEN.push(false)
        }
        if(!IS_NICK_WRITTEN[UID_ARR.indexOf(data.uid)]) {
            let user_div = document.getElementById(`user-container-${data.uid}`)
            if(user_div != null) {
                user_div.insertAdjacentHTML("afterbegin", `<div class="user-name-wrapper"><span class="user-name">${data.user_name}</span></div>`)
                IS_NICK_WRITTEN[UID_ARR.indexOf(data.uid)] = true
            }
        }
    }
}

joinAndDisplayLocalStream()

document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream)
document.getElementById('camera-btn').addEventListener('click', toggleCamera)
document.getElementById('mic-btn').addEventListener('click', toggleMic)