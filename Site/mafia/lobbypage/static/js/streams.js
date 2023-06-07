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
let IS_NICK_WRITTEN = []
let chatlock = false
let votelock = false
let voted_for = ""
var votelist = new Map()


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
    setInterval(() => testSocket.send(JSON.stringify({
        'user_name' : user_name,
        'uid' : UID
    })), 100)
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

let FullMute = async (e) => {
    await localTracks[0].setMuted(true)
    await localTracks[1].setMuted(true)
}

let FullUnMute = async (e) => {
    await localTracks[0].setMuted(false)
    await localTracks[1].setMuted(false)
}

let vote = function (e) {
    if (votelock === false){
        console.log("VOTE: ГОЛОСОВАНИЕ")
        let votename = e.target.id
        votelock = true
        console.log("VOTE votename:",votename)
        testSocket.send(JSON.stringify({
            'vote_uid' : votename
        }))
    }
    else {console.log("VOTE: Сейчас не ваше время голосовать.")}
}


testSocket.onmessage = function (e) {
    let data = JSON.parse(e.data)
    if (data.type === 'chat') {
        let messages = document.getElementById('messages')
        let htmlAdding = '<div><p>' + data.message + '</p></div>'
        messages.insertAdjacentHTML('beforeend', htmlAdding)
    }
    if(data.type === 'user_info') {
        if(UID_ARR.indexOf(data.uid) === -1 && data.uid != UID) {
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
    if (data.type === 'game_roles') {               //Рассылаем роли игрокам
        let roles = data.roleslist
        testSocket.send(JSON.stringify({
            'roleslist' : roles,
            'socket_uid' : UID
        }))
        GameProcess(roles)
    }
    if (data.type === 'vote_sending') {               //Принимаем голоса
        let vote = data.vote
        console.log("VOTE: GOT", vote)
        votelist[vote]++
        console.log("VOTE votelist:", votelist)
    }
}

//я понял что игра в отдельном классе это буллщит.... так что.... она будет здесть... простите...


let GameProcess = async (players) => {
    let playerlist = players
    for (let a in playerlist){
        votelist[a] = 0
    }
    console.log("VOTE votelist: ", votelist)
    let voteresult = ""
    let killresult = ""
    let healresult = ""
    let checkresult = ""
    let rolespath = ["mafia", "doc", "com", "civil"]
    let rolesnames = ["мафия", "доктор", "комиссар", "гражданские"]
    let turn = -1;
    console.log(playerlist)
    let htmlAdding = '<div><p>Ваша роль - ' + playerlist[UID] + '</p></div>'
    messages.insertAdjacentHTML('beforeend', htmlAdding)
    htmlAdding = '<div><p>Начинается ночь! Город засыпает...</p></div>'
    messages.insertAdjacentHTML('beforeend', htmlAdding)
    let gametimer = setInterval(function(){
        voteresult = ""
        for (let i =0; i<UID_ARR.length;i++){
            console.log("VOTE button:", document.getElementById(`vote-${UID_ARR[i]}`))
        }
        if (turn!=-1)
        {
            let tempresult = ""
            let tempvalue = 0
            let amount_of_max = 0
            for(let userid in votelist){
                if (votelist[userid] > tempvalue) 
                {
                    tempvalue = votelist[userid]
                    tempresult = userid
                }
            }
            console.log("VOTE: tempvalue", tempvalue)
            for(let userid in votelist){
                if (votelist[userid] === tempvalue) 
                {
                    amount_of_max++
                }
            }
            console.log("VOTE: amount", amount_of_max)
            if (amount_of_max===1)
            { 
                
                switch(turn) {
                    case 0: 
                        killresult = tempresult;
                        messages.insertAdjacentHTML('beforeend', "<div><p>Мафия выбрала свою цель!</p></div>");
                        break;
                    case 1:
                         healresult = tempresult;
                         messages.insertAdjacentHTML('beforeend', "<div><p>Доктор выбрал, кого спасать!</p></div>");
                         break;
                    case 2: 
                        checkresult = tempresult;
                        messages.insertAdjacentHTML('beforeend', "<div><p>Комиссар выбрал, кого проверить этой ночью</p></div>");
                        break;
                    case 3:
                         voteresult = tempresult;
                         messages.insertAdjacentHTML('beforeend', "<div><p>Голосование проведено! Выбранный будет убит!</p></div>");
                         break;
                }
            }
            else {
                messages.insertAdjacentHTML('beforeend', "<div><p>Голосование сорвано! Одинаковое количество голосов!</p></div>");
            }
            for (let i in votelist) {votelist[i]=0}
            };
        turn+=1
        if (turn === 4) {
            turn = 0
            messages.insertAdjacentHTML('beforeend', "<div><p>На дневном голосовании убили игрока " + voteresult + ". Его роль - " + playerlist[voteresult] + "</p></div>");
            voteresult = ""
        }
        if (turn === 3){
            if (killresult!="")
            {
                if (killresult === healresult){
                    messages.insertAdjacentHTML('beforeend', "<div><p>Доктор успешно предотвратил убийство! Все живы!</p></div>");
                }
                else {
                    messages.insertAdjacentHTML('beforeend', "<div><p>Мафия убила игрока " + killresult + ". Его роль - " + playerlist[killresult] + "</p></div>");
                }
            }
            else {
                messages.insertAdjacentHTML('beforeend', "<div><p>Мафия сегодня более благосклонна к жителям... все остались целы</p></div>");
            }
            if (checkresult!="")
            {
                messages.insertAdjacentHTML('beforeend', "<div><p>Комиссар сделал проверку и выяснил, что роль его подозреваемого - " + playerlist[checkresult] + "</p></div>");  //добавить результат проверки
            }
            else{
                messages.insertAdjacentHTML('beforeend', "<div><p>Комиссар проспал свою смену... проверок не было</p></div>");
            }
            killresult = ""
            healresult = ""
            checkresult = ""
        } 
        console.log("TURN: ", turn, rolespath[turn])
        messages.insertAdjacentHTML('beforeend', '<div><p>сейчас ход: ' + rolesnames[turn] + '</p></div>')
        if (playerlist[UID] != rolespath[turn] && turn !=3){
            chatlock = true
            FullMute()
            votelock = true
        }
        else {
            chatlock = false
            FullUnMute()
            votelock = false
        }
    },7000)
}


joinAndDisplayLocalStream()

document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream)
document.getElementById('camera-btn').addEventListener('click', toggleCamera)
document.getElementById('mic-btn').addEventListener('click', toggleMic)