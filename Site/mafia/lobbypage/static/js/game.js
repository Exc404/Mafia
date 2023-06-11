var Rolenames = ["Мафия", "Доктор", "Комиссар", "Дневное обсуждение", "Дневное голосование"]
var chatlock = false
var votelock = true
var MyRole = ""
var PK_SET = new Map()
var turn = 999
var Roles = new Map()


let vote = function (e) {
    if (votelock === false){
        console.log("GAME: ГОЛОСОВАНИЕ", e.target.id)
        let votename = e.target.id
        votelock = true
        console.log("VOTE votename:",votename)
        testSocket.send(JSON.stringify({
            'vote_pk' : PK_SET[votename]
        }))
    }
    else {console.log("GAME: Сейчас не ваше время голосовать.")}
}
