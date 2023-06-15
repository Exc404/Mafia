var Rolenames = ["Мафия", "Доктор", "Комиссар", "Дневное обсуждение", "Дневное голосование"]
var chatlock = false
var votelock = true
var MyRole = ""
var PK_SET = new Map()
var turn = 999
var Roles = new Map()


let vote = function (e) {
    if (votelock === false){
        let votename = e.target.id
        if (Roles[PK_SET[votename]]!="spec"){
            votelock = true
            console.log("VOTE votename:",votename)
            for(let i in PK_SET)document.getElementById(i).style.display="none"
            testSocket.send(JSON.stringify({
                'vote_pk' : PK_SET[votename]
            }))
        }
        else {
            alert("Нельзя голосовать за усопшего!")
        }

    }
}
