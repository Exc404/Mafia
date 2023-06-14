let urlTemp = window.location.host

let url = 'ws://' + urlTemp + '/ws/socket-server/' + room_name + '/'

console.log(url)

const testSocket = new WebSocket(url)

testSocket.onopen = function(){
    console.log("GAME: ROLES", Roles)
    console.log("GAME: PK", user_pk)
    if (is_game == 1){
        chatlock = true
        votelock = true
    } 
    testSocket.send(JSON.stringify({
        'username': user_name,
        'pk' : user_pk,
    }))
}

let inputForm = document.getElementById('messageInputForm')

inputForm.addEventListener('submit', (e) => {
    e.preventDefault()
    if (chatlock === false){
        let message = e.target.messageForm.value
        if (message === "iliveindarkness") {chatlock = false} // это надо удалить...
        if(message!="") {
            message = user_name + ":" + message
            testSocket.send(JSON.stringify({
                'message': message
            }))
        }
    }
    else {
        messages.insertAdjacentHTML('beforeend', '<div><p style="color:#1D943C"> У вас чатлок!</p></div>')
    }
    inputForm.reset()
})

window.onload = function () {
    let startButton = document.getElementById('startgame')
    startButton.onclick = function () {
        console.log("GAME: AMOUNT", UID_ARR.length + 1)
        if (UID_ARR.length + 1 < 1){//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!5
            alert("НЕДОСТАТОЧНО ПОЛЬЗОВАТЕЛЕЙ! МИНИМУМ - 5!")
        }
        else{
        testSocket.send(JSON.stringify({
            'are_you_host' : "are_you_host"
        }))
        }
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
        'uid' : UID,
        'pk' : user_pk
    })), 100)
    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()
    let player = `<div class="video-container" id = "user-container-${UID}">
                    <div class="user-name-wrapper"><span class="user-name">${user_name}</span></div>
                    <div class="video-player" id = "user-${UID}"></div>
                    <div class = "icon-wrapper">
                    <img class = "control-icon" id = "vote-${UID}" src = "/./static/img/votemark.jpg"/>
                    </div>
                </div>`+`<div class="video-container" id = "user-container-${UID}">
                <div class="user-name-wrapper"><span class="user-name">${user_name}</span></div>
                <div class="video-player" id = "user-${UID}"></div>
                <div class = "icon-wrapper">
                <img class = "control-icon" id = "vote-${UID}" src = "/./static/img/votemark.jpg"/>
                </div>
            </div>`
    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
    document.getElementById(`vote-${UID}`).onclick = vote
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
        document.getElementById(`vote-${user.uid}`).onclick = vote
        if(!is_game)
            user.videoTrack.play(`user-${user.uid}`)
    }
    if(mediaType === "audio") {
        if(!is_game)
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
    if(!is_game)
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

let FullMute = async () => {
    for(let i in remoteUsers) {
        remoteUsers[i].videoTrack.stop()
        remoteUsers[i].audioTrack.stop()
    }
    localTracks[1].stop()
}

let RoleUnMute = async () => {
    for(let i in remoteUsers) {
        if(Roles[PK_SET[`vote-${remoteUsers[i].uid}`]] != "spec"){
            if(Roles[PK_SET[`vote-${remoteUsers[i].uid}`]] === MyRole) {
                remoteUsers[i].audioTrack.play()
            }
            remoteUsers[i].videoTrack.play(`user-${remoteUsers[i].uid}`)
        }
    }
    localTracks[1].play(`user-${UID}`)
}

let FullUnMute = async () => {
    for(let i in remoteUsers) {
        if(Roles[PK_SET[`vote-${remoteUsers[i].uid}`]] != "spec") {
            remoteUsers[i].videoTrack.play(`user-${remoteUsers[i].uid}`)
            remoteUsers[i].audioTrack.play()
        }
    }
    localTracks[1].play(`user-${UID}`)
}


//таймер
timerId=null

function startTimer(duration, display) {
    if(timerId)clearInterval(timerId);
    duration*=100
    var timer = duration, minutes, seconds;
    console.log('starttick')
    
        timerId = setInterval(function () {
        minutes = parseInt(timer / 6000, 10);
        seconds = parseInt(timer % 6000/100, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;
        stripe = document.getElementById('time-stripe-progress');
        stripe.style.width=""+(1-timer/duration)*100+"%"

        timer-=1
        console.log('tick')
        if(timer == -1)clearInterval(timerId);
    }, 10);

}
// window.onload = function () {
//     var fiveMinutes = 60 * 5,
//         display = document.querySelector('#time');
//     startTimer(fiveMinutes, display);
// };


testSocket.onmessage = function (e) {
    let data = JSON.parse(e.data)
    if (data.type === 'chat') {
        if (chatlock === false){
            let messages = document.getElementById('messages')
            if (turn === 0 && MyRole==="mafia"){
                htmlAdding = '<div><p style="color:#FF0000">' + data.message + '</p></div>'
            }
            else{
                htmlAdding = '<div><p>' + data.message + '</p></div>'
            }
            console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
            messages.insertAdjacentHTML('beforeend', htmlAdding)
        }
    }
    if(data.type === 'user_info' && data.uid != UID.toString()) {
        if(UID_ARR.indexOf(data.uid) === -1) {
            UID_ARR.push(data.uid)
            console.log("GAME: GOT PK + UID", data.pk," ", data.uid, " ", data.user_name)
            PK_SET['vote-' + data.uid] = data.pk
            console.log("GAME:", PK_SET)
            IS_NICK_WRITTEN.push(false)
        }
        if(!IS_NICK_WRITTEN[UID_ARR.indexOf(data.uid)]) {
            let user_div = document.getElementById(`user-container-${data.uid}`)
            if(user_div != null) {
                user_div.insertAdjacentHTML("afterbegin", `<div class="user-name-wrapper"><span class="user-name">${data.user_name}</span></div>`)
                IS_NICK_WRITTEN[UID_ARR.indexOf(data.uid)] = true
            }
            let str = 'vote-' + data.uid
            let res_uid = ''
            for(let i in PK_SET) {
                if(PK_SET[i] === data.pk && i != str) {
                    res_uid = i.substring(5)
                    let el = document.getElementById(`user-container-${res_uid}`)
                    if(el != null)
                        document.getElementById(`user-container-${res_uid}`).remove()
                    delete PK_SET[i]
                }
            }
        }
    }
    if(data.type === 'start_info') {
        Roles = data.rolelist
        is_game = true
        console.log("GAME: ROLES", Roles)
        MyRole = Roles[user_pk]
        //id="блок роль" class = MyRole
        console.log("GAME: UID", UID)
        PK_SET['vote-'+UID] = user_pk
        let warning = '<div><p style="color:#1D943C"> Ваша роль:  ' + Roles[user_pk] +'</p></div>'
        messages.insertAdjacentHTML('beforeend', warning)
    }
    if (data.type === 'update_roles'){
        Roles = data.rolelist
        MyRole = data.rolelist[user_pk]
    }

    if (data.type === "am_i_host"){
        if (data.is_host === true){
            alert("Вы запустили игру")
            testSocket.send(JSON.stringify({
                'start' : 'ЗАРАБОТАЛО БЛЯТЬ'
            }))
        }
        else alert("Вы не являетесь создателем комнаты")
        return false
    }

    if(data.type === 'turn_info'){
        //60 сек - 3 4, 20 - 0 1 2 
        //вывод имя фазы
        var div = document.getElementById('name-event');
        div.innerHTML = Rolenames[data.turnnumber];

        //запуск таймера
     
        var time=20
        if(data.turnnumber<3)time=20
        display = document.querySelector('#time');
        startTimer(time-1, display);
        
        


        turn = data.turnnumber // - идекс фазы
        console.log("GAME STAGE: ", turn)
        chatlock = data.chatlock
        votelock = data.votelock
        if(chatlock && Roles[user_pk] != "spec") {
            console.log("GAME: MUTE", turn)
            FullMute()
        }
        else if(chatlock && Roles[user_pk] === "spec" && (turn === 3 || turn === 4)) {
            console.log("GAME: SPEC", turn)
            FullUnMute()
        }
        else if(!chatlock) {
            console.log("GAME: UNMUTE", turn)
            FullMute()
            if(turn != 3 && turn != 4)
                RoleUnMute()
            else
                FullUnMute()
        }
        else {
            FullMute()
        }
        console.log("CHATLOCK:", data.chatlock)
        let warning = '<div><p style="color:#1D943C"> ТЕКУЩИЙ ХОД: ' + Rolenames[turn] +'</p></div>'
        messages.insertAdjacentHTML('beforeend', warning)
    }

    if(data.type === 'vote_result'){
        let resultname = data.resultname
        let warning = '<div><p style="color:#1D943C"> Результат голосования: ' + resultname +'</p></div>'
        resultname = ""
        messages.insertAdjacentHTML('beforeend', warning)
    }

    if(data.type === 'morning_results'){
        let killed = data.killtarget
        let dead_name = data.targetname
        let if_saved = data.healresult
        let check = data.checked
        if (killed === ""){
            let warning = '<div><p style="color:#1D943C"> УБИЙСТВА НЕ ПРОИЗОШЛО! ВСЕ ЖИВЫ!</p></div>'
            messages.insertAdjacentHTML('beforeend', warning)
        }
        else {
            if (if_saved) {
                let warning = '<div><p style="color:#1D943C"> ДОКТОРУ УДАЛОСЬ ПРЕДОТВРАТИТЬ УБИЙСТВО! ВСЕ ЖИВЫ!</p></div>'
                messages.insertAdjacentHTML('beforeend', warning)
            }
            else{
                console.log('GAME: rolelist', Roles)
                console.log('GAME: killed', killed)
                let warning = '<div><p style="color:#1D943C"> ДОКТОРУ НЕ УДАЛОСЬ ПРЕДОТВРАТИТЬ УБИЙСТВО! Был убит игрок '+ dead_name +'. Его роль - ' + Roles[killed] + '</p></div>'
                Roles[killed] = "spec"
                messages.insertAdjacentHTML('beforeend', warning)
            }
        }
        if (check != ""){
            let warning = '<div><p style="color:#1D943C">КОМИССАР ПРОВЁЛ РАССЛЕДОВАНИЕ И УЗНАЛ, ЧТО ЕГО ПОДОЗРЕВАЕМЫЙ - ' + check + '</p></div>'
            messages.insertAdjacentHTML('beforeend', warning)
        }
        else {
            let warning = '<div><p style="color:#1D943C">КОМИССАР ПРОСПАЛ СВОЮ СМЕНУ. ПРОВЕРОК НЕ БЫЛО!</p></div>'
            messages.insertAdjacentHTML('beforeend', warning)
        }
        killed = ""
        dead_name = ""
        if_saved = 0
        check = ""
    }

    if(data.type === "night_results"){
        let killed = data.votetarget
        let killed_name = data.targetname
        let warning = '<div><p style="color:#1D943C"> В результате дневного голосования был убит игрок '+ killed_name +'. Его роль - ' + Roles[killed] + '</p></div>'
        Roles[killed] = "spec"
        messages.insertAdjacentHTML('beforeend', warning)
    }
}

joinAndDisplayLocalStream()

document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream)
document.getElementById('camera-btn').addEventListener('click', toggleCamera)
document.getElementById('mic-btn').addEventListener('click', toggleMic)