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
    if (chatlock==false){ 
        testSocket.send(JSON.stringify({
            'message': message
        }))
    }
    else 
    {
        message = "<div><p>На данный момент чат вам недоступен! Дождитесь своей очереди!</p></div>"
        messages.insertAdjacentHTML('beforeend', message)
    }
    inputForm.reset()
})
window.onload = function () {
    let startButton = document.getElementById('startgame')          //СТАРТУЮ ИГРУ, отсылаю список юзеров-хуюзеров
    startButton.onclick = function () {
        if (is_host) {
            alert("Вы запустили игру")
            testSocket.send(JSON.stringify({    
                'users': UID_ARR,
                'hostuid': UID
            }))
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
let chatlock = false
let votelock = false

const client = AgoraRTC.createClient({mode: 'rtc', codec: 'vp8'})

let localTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async () => {
    document.getElementById('room-name').innerText = CHANNEL
    client.on('user-published', handleUserJoined)
    client.on('user-left', handleUserLeft)
    alert("Начался шпионаж за твоей жопой!")
    UID = await client.join(APP_ID, CHANNEL, TOKEN, null)
    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()
    let player = `<div class="video-container" id = "user-container-${UID}">
                    <div class="user-name-wrapper"><span class="user-name">${user_name}</span></div>
                    <div class="video-player" id = "user-${UID}"></div>
                    <div class = "icon-wrapper" id = "vote-${UID}">
                    <img class = "control-icon" id = "vote-btn" src = "/./static/img/votemark.jpg"/>
                    </div>
                    </div>`
    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
    localTracks[1].play(`user-${UID}`)
    await client.publish([localTracks[0], localTracks[1]])
}

let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user
    await client.subscribe(user, mediaType)
    if(mediaType === "video") {
        let player = document.getElementById(`user-container-${user.uid}`)
        if(player != null){
            player.remove()
        }
        player = `<div class="video-container" id = "user-container-${user.uid}">
                    <div class="video-player" id = "user-${user.uid}"></div>
                    <div class = "icon-wrapper">
                    <img class = "control-icon" id = "vote-${user.uid}" src = "/./static/img/votemark.jpg"/>
                    </div>
                </div>`
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
        user.videoTrack.play(`user-${user.uid}`)
        setInterval(function() {testSocket.send(JSON.stringify({
            'user_name' : user_name,
            'uid' : UID
        }))}, 2000)
    }
    if(mediaType === "audio") {
        user.audioTrack.play()
    }
}

let handleUserLeft = async (user) => {
    UID_ARR = UID_ARR.map(el => el === user.uid ? 0 : el)
    UID_ARR = UID_ARR.filter(el => el === 0 ? false : true)
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

let vote = async (e) => {
    console.log("VOTE: ГОЛОСОВАНИЕ")
    let votename = e.target.id
    console.log("VOTE:",votename)
    testSocket.send(JSON.stringify({
        'vote_uid' : votename
    }))
}


testSocket.onmessage = function (e) {
    let data = JSON.parse(e.data)
    console.log("DATA:", data)
    if (data.type === 'chat') {
        let messages = document.getElementById('messages')
        let htmlAdding = '<div><p>' + data.message + '</p></div>'
        messages.insertAdjacentHTML('beforeend', htmlAdding)
    }
    if(data.type === 'user_info') {
        let super_test = document.getElementById(`user-container-${data.uid}`)
        if(`user-container-${data.uid}` != `user-container-${UID}` && UID_ARR.indexOf(data.uid) === -1) {
            super_test.insertAdjacentHTML('afterbegin', `<div class="user-name-wrapper"><span class="user-name">${data.user_name}</span></div>`)
            UID_ARR.push(data.uid)
        }
    }
    if (data.type === 'game_roles') {               //Рассылаем роли игрокам
        let roles = data.roleslist
        testSocket.send(JSON.stringify({
            'roleslist' : roles,
            'socket_uid' : UID
        }))
        GameProcess(roles)
    }
}

//я понял что игра в отдельном классе это буллщит.... так что.... она будет здесть... простите...


let GameProcess = async (players) => {
    let playerlist = players
    let rolespath = ["mafia", "doc", "com", "civil"]
    let rolesnames = ["мафия", "доктор", "комиссар", "гражданские"]
    let turn = -1;
    console.log(playerlist)
    for (let i = 0; i<UID_ARR.length; i++){
        let temp = document.getElementById(`vote-${UID_ARR[i]}`)
        console.log("VOTE: temp", temp)
        document.getElementById(`vote-${UID_ARR[i]}`).addEventListener('click',vote)
    }
    document.getElementById(`vote-${UID}`).addEventListener('click',vote)
    let htmlAdding = '<div><p>Ваша роль - ' + playerlist[UID] + '</p></div>'
    messages.insertAdjacentHTML('beforeend', htmlAdding)
    htmlAdding = '<div><p>Начинается ночь! Город засыпает...</p></div>'
    messages.insertAdjacentHTML('beforeend', htmlAdding)
    let gametimer = setInterval(function(){
        turn+=1
        if (turn == 4) {turn = 0}
        console.log("TURN: ", turn, rolespath[turn])
        messages.insertAdjacentHTML('beforeend', '<div><p>сейчас ход: ' + rolesnames[turn] + '</p></div>')
        if (playerlist[UID] != rolespath[turn] && turn !=3){
            chatlock = true
            localTracks[0].setMuted(true)
            localTracks[1].setMuted(true)
        }
        else {
            chatlock = false
            localTracks[0].setMuted(false)
            localTracks[1].setMuted(false)
        }
    },5000)
}






joinAndDisplayLocalStream()

document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream)
document.getElementById('camera-btn').addEventListener('click', toggleCamera)
document.getElementById('mic-btn').addEventListener('click', toggleMic)