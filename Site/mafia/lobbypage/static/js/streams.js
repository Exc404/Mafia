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
        if(message!="") {
            message = user_name + ": " + message
            testSocket.send(JSON.stringify({
                'message': message
            }))
        }
    }
    else {
        messages.insertAdjacentHTML('beforeend', '<div><p style="color:#1D943C"> У вас чатлок!</p></div>')
        messages.scrollTop = messages.scrollHeight
    }
    inputForm.reset()
})

window.onload = function () {
    let startButton = document.getElementById('startgame')
    startButton.onclick = function () {
        console.log("GAME: AMOUNT", UID_ARR.length + 1)
        if (UID_ARR.length + 1 < 5){//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!5
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
    let player = `<div class="video-container" id = "user-container-${UID}" style="background-image: url('/./static/img/cat.jpg');">
                    <div class="user-name-wrapper"><span class="user-name">${user_name}</span></div>
                    <div class="video-player" id = "user-${UID}"></div>
                    <div id = "vote-visible-${UID}" slyle="display: block;" class="vote-visib" ><div class = "vote-control" id = "${UID}" style=""/><p class="p-vote">Выбрать</p></div></div>`+``
    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
    document.getElementById(`${UID}`).onclick = vote
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
        player =`<div class="video-container" id = "user-container-${user.uid}" style="background-image: url('/./static/img/cat.jpg');">
        <div class="video-player" id = "user-${user.uid}"></div>
        <div id = "vote-visible-${user.uid}" slyle="display: block;" class="vote-visib" ><div class = "vote-control" id = "${user.uid}" style=""/><p class="p-vote">Выбрать</p></div></div>`
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
        document.getElementById(`${user.uid}`).onclick = vote
        if(!is_game)
            user.videoTrack.play(`user-${user.uid}`)
        else    
            if(Roles[PK_SET[user.uid]]==="spec"){
                document.getElementById("user-container-"+user.uid).style = "background-image: url('/./static/img/card/spec.jpg');"
                document.getElementById("vote-visible-"+user.uid).style = "display: none;"
                
            }
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
        if(Roles[PK_SET[`${remoteUsers[i].uid}`]] != "spec"){
            if(Roles[PK_SET[`${remoteUsers[i].uid}`]] === MyRole) {
                remoteUsers[i].audioTrack.play()
            }
            remoteUsers[i].videoTrack.play(`user-${remoteUsers[i].uid}`)
        }
    }
    localTracks[1].play(`user-${UID}`)
}

let FullUnMute = async () => {
    for(let i in remoteUsers) {
        if(Roles[PK_SET[`${remoteUsers[i].uid}`]] != "spec") {
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
            messages.scrollTop = messages.scrollHeight
        }
    }
    if(data.type === 'user_info' && data.uid != UID.toString()) {
        if(UID_ARR.indexOf(data.uid) === -1) {
            UID_ARR.push(data.uid)
            console.log("GAME: GOT PK + UID", data.pk," ", data.uid, " ", data.user_name)
            PK_SET[data.uid] = data.pk
            console.log("GAME:", PK_SET)
            IS_NICK_WRITTEN.push(false)
        }
        if(!IS_NICK_WRITTEN[UID_ARR.indexOf(data.uid)]) {
            let user_div = document.getElementById(`user-container-${data.uid}`)
            if(user_div != null) {
                user_div.insertAdjacentHTML("afterbegin", `<div class="user-name-wrapper"><span class="user-name">${data.user_name}</span></div>`)
                IS_NICK_WRITTEN[UID_ARR.indexOf(data.uid)] = true
            }
            let str = data.uid
            let res_uid = ''
            for(let i in PK_SET) {
                if(PK_SET[i] === data.pk && i != str) {
                    res_uid = i
                    let el = document.getElementById(`user-container-${res_uid}`)
                    if(el != null)
                        document.getElementById(`user-container-${res_uid}`).remove()
                    console.log("GAME DEL UID :", i)    
                    delete PK_SET[i]
    
                }
            }
        }
    }
    if(data.type === 'start_info') {

        for(let i in UID_ARR)
        {
            document.getElementById("user-container-"+UID_ARR[i]).style = "background-image: url('/./static/img/cat.jpg');"
            document.getElementById("vote-visible-"+UID_ARR[i]).style = "display: block;"
        }
        document.getElementById("user-container-"+UID).style = "background-image: url('/./static/img/cat.jpg');"
        document.getElementById("vote-visible-"+UID).style = "display: block;"
        

            
        Roles = data.rolelist
        is_game = true
        console.log("GAME: ROLES", Roles)
        MyRole = Roles[user_pk]

        document.getElementById('startgame').style.display="none"
        //id="блок роль" class = MyRole
        document.getElementById('invate').style.display="none"
        document.getElementById('info-card').style.display="block"
        if(MyRole == "mafia")
        {
            document.getElementById('myrole').innerHTML="Роль: Мафия"
            document.getElementById('card').innerHTML='<img class="card-img" src = "/./static/img/card/mafiozi.jpg" width="100%"/> '
        }
        else if(MyRole == "doc")
        {
            document.getElementById('myrole').innerHTML="Роль: Доктор"
            document.getElementById('card').innerHTML='<img class="card-img" src = "/./static/img/card/dok.jpg" width="100%"/> '
        }
        else if(MyRole == "com")
        {
            document.getElementById('myrole').innerHTML="Роль: Комиссар"
            document.getElementById('card').innerHTML='<img class="card-img" src = "/./static/img/card/com.jpg" width="100%"/> '
        }     
        else if(MyRole == "civil")
        {
            document.getElementById('myrole').innerHTML="Роль: Гражданин"
        if(Math.floor(Math.random() * 2))
            document.getElementById('card').innerHTML='<img class="card-img" src = "/./static/img/card/mirn_1.jpg" width="100%"/> '
        else
            document.getElementById('card').innerHTML='<img class="card-img" src = "/./static/img/card/mirn_2.jpg" width="100%"/> '
        }
        
        console.log("GAME: UID", UID)
        PK_SET[UID] = user_pk
        let warning = '<div><p style="color:#1D943C"> Ваша роль:  ' + Roles[user_pk] +'</p></div>'
        messages.insertAdjacentHTML('beforeend', warning)
        messages.scrollTop = messages.scrollHeight
    }
    
    if (data.type === 'update_roles'){
        TempRol=data.rolelist
        for(let i in TempRol)
        {
            if(TempRol[i]!=Roles[i] && TempRol[i] === "spec")
            {
                for(let j in PK_SET)
                {
                    if(PK_SET[j] === i)
                    {
                        document.getElementById("user-container-"+j).style = "background-image: url('/./static/img/card/spec.jpg');"
                        document.getElementById("vote-visible-"+j).style = "display: none;"
                    }
                }
            }
        }
        Roles = data.rolelist
        console.log("GAME: MyRole", MyRole)
        if(MyRole==="")
        {

            console.log("GAME: MyRole-2", MyRole)
            MyRole = data.rolelist[user_pk]
            document.getElementById('invate').style.display="none"
            document.getElementById('info-card').style.display="block"
            if(MyRole == "mafia")
            {
                document.getElementById('myrole').innerHTML="Роль: Мафия"
                document.getElementById('card').innerHTML='<img class="card-img" src = "/./static/img/card/mafiozi.jpg" width="100%"/> '
            }
            else if(MyRole == "doc")
            {
                document.getElementById('myrole').innerHTML="Роль: Доктор"
                document.getElementById('card').innerHTML='<img class="card-img" src = "/./static/img/card/dok.jpg" width="100%"/> '
            }
            else if(MyRole == "com")
            {
                document.getElementById('myrole').innerHTML="Роль: Комиссар"
                document.getElementById('card').innerHTML='<img class="card-img" src = "/./static/img/card/com.jpg" width="100%"/> '
            }     
            else if(MyRole == "civil")
            {
                document.getElementById('myrole').innerHTML="Роль: Гражданин"
            if(Math.floor(Math.random() * 2))
                document.getElementById('card').innerHTML='<img class="card-img" src = "/./static/img/card/mirn_1.jpg" width="100%"/> '
            else
                document.getElementById('card').innerHTML='<img class="card-img" src = "/./static/img/card/mirn_2.jpg" width="100%"/> '
            }
            else if(MyRole == "spec")
            {
                document.getElementById('myrole').innerHTML="Роль: Наблюдател "
                document.getElementById('card').innerHTML='<img class="card-img" src = "/./static/img/card/spec.jpg" width="100%"/> '
            }
        }
        
    }

    if (data.type === "am_i_host"){
        if (data.is_host === true){
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
        
        if(votelock)
            for(let i in PK_SET)document.getElementById(i).style.display="none"
        else
            for(let i in PK_SET)if(document.getElementById(i)!=null)document.getElementById(i).style.display="flex"
        

        

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
        messages.scrollTop = messages.scrollHeight
    }
    
    // if(data.type === 'vote_result'){
    //     let resultname = data.resultname
    //     let warning = '<div><p style="color:#1D943C"> Результат голосования: ' + resultname +'</p></div>'
    //     resultname = ""
    //     messages.insertAdjacentHTML('beforeend', warning)
    // }


    if(data.type === 'morning_results'){
        let killed = data.killtarget
        let dead_name = data.targetname
        let if_saved = data.healresult
        let check = data.checked
        if (killed === ""){
            let warning = '<div><p style="color:#1D943C"> УБИЙСТВА НЕ ПРОИЗОШЛО! ВСЕ ЖИВЫ!</p></div>'
            messages.insertAdjacentHTML('beforeend', warning)
            messages.scrollTop = messages.scrollHeight
        }
        else {
            if (if_saved) {
                let warning = '<div><p style="color:#1D943C"> ДОКТОРУ УДАЛОСЬ ПРЕДОТВРАТИТЬ УБИЙСТВО! ВСЕ ЖИВЫ!</p></div>'
                messages.insertAdjacentHTML('beforeend', warning)
                messages.scrollTop = messages.scrollHeight
            }
            else{
                console.log('GAME: rolelist', Roles)
                console.log('GAME: killed', killed)
                let warning = '<div><p style="color:#1D943C"> ДОКТОРУ НЕ УДАЛОСЬ ПРЕДОТВРАТИТЬ УБИЙСТВО! Был убит игрок '+ dead_name +'. Его роль - ' + Roles[killed] + '</p></div>'
                Roles[killed] = "spec"
                if(Roles[killed]===Roles[user_pk.toString()]){

                    document.getElementById('myrole').innerHTML="Роль: Наблюдатель ("+MyRole+")"
                    document.getElementById('card').innerHTML='<img class="card-img" src = "/./static/img/card/spec.jpg" width="100%"/> '
                }
                for(let i in PK_SET) {
                    if(PK_SET[i].toString() === killed) {
                        document.getElementById("user-container-"+i).style = "background-image: url('/./static/img/card/spec.jpg');"
                        document.getElementById("vote-visible-"+i).style = "display: none;"
                    }
                }
                if(killed === user_pk.toString()) {
                    document.getElementById('my-role').remove()
                    document.getElementById('role-name-wrapper').insertAdjacentHTML('beforeend', `<span id = "my-role">ВЫ МЕРТВЫ(${MyRole})</span>`)
                }
                messages.insertAdjacentHTML('beforeend', warning)
                messages.scrollTop = messages.scrollHeight
            }
        }
        if (check != ""){
            let warning = '<div><p style="color:#1D943C">КОМИССАР ПРОВЁЛ РАССЛЕДОВАНИЕ И УЗНАЛ, ЧТО ЕГО ПОДОЗРЕВАЕМЫЙ - ' + check + '</p></div>'
            messages.insertAdjacentHTML('beforeend', warning)
            messages.scrollTop = messages.scrollHeight
        }
        else {
            let warning = '<div><p style="color:#1D943C">КОМИССАР ПРОСПАЛ СВОЮ СМЕНУ. ПРОВЕРОК НЕ БЫЛО!</p></div>'
            messages.insertAdjacentHTML('beforeend', warning)
            messages.scrollTop = messages.scrollHeight
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
        if(killed === user_pk.toString()){
            
           
            document.getElementById('myrole').innerHTML="Роль: Наблюдатель ("+MyRole+")"
            document.getElementById('card').innerHTML='<img class="card-img" src = "/./static/img/card/spec.jpg" width="100%"/> '
        }
        for(let i in PK_SET) {
            if(PK_SET[i].toString() === killed) {
                document.getElementById("user-container-"+i).style = "background-image: url('/./static/img/card/spec.jpg');"
                document.getElementById("vote-visible-"+i).style = "display: none;"
            }
        }
        if(killed === user_pk.toString()) {
            document.getElementById('my-role').remove()
            document.getElementById('role-name-wrapper').insertAdjacentHTML('beforeend', `<span id = "my-role">ВЫ МЕРТВЫ(${MyRole})</span>`)
        }
        messages.insertAdjacentHTML('beforeend', warning)
        messages.scrollTop = messages.scrollHeight
    }

    if (data.type === "end_game"){
        let winner = ""
        if (data.winner === "0"){
            winner = "мафии"
        }
        else{
            winner = "мирных"
        }
        chatlock = false
        votelock = true
        MyRole = ""
        turn = 924
        Roles = {}
        FullUnMute()
        is_game = false
        document.getElementById('my-role').remove()
        let warning = '<div><p style="color:#1D943C">ИГРА ОКОНЧЕНА! Победу одержала сторона ' + winner + '!</p></div>'
        for(let i in PK_SET) {
            document.getElementById(i).src = '/./static/img/votemark.jpg'
            let user_uid = i
            if(UID_ARR.find(el => el === user_uid) === undefined && user_uid != UID.toString()) {
                document.getElementById(`user-container-${user_uid}`).remove()
                delete PK_SET[i]
            }
        }
        messages.insertAdjacentHTML('beforeend', warning)
    }

}

joinAndDisplayLocalStream()

document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream)
//document.getElementById('camera-btn').addEventListener('click', toggleCamera)
//document.getElementById('mic-btn').addEventListener('click', toggleMic)