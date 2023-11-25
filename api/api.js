const { error } = require('console')
const express = require('express')
const app = express()
const port = 3000
const USERS = 'data_files/users.json'
const MESSAGES = 'data_files/messages.json'
const MESSAGES_SENT = 'data_files/messages_sent.json'

let fs = require("fs")
cors = require('cors')
app.use(cors());
app.use(express.json())

app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*")
    res.header("Content-Type","application/json; charset=utf-8")
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Accept")
    next();
});


function getObjFromJsonFile(fileName) {
    return JSON.parse(fs.readFileSync(fileName, 'utf8'))
}

app.get('/', (req, res) => {
    res.header("Content-Type", "text/html; charset=utf-8")
    html = fs.readFileSync('index.html', 'utf8')
    res.send(html)
})
app.get('/stuff', (req, res) => {
    res.header("Content-Type", "text/html; charset=utf-8")
    html = fs.readFileSync('stuff.html', 'utf8')
    res.send(html)
})

app.get('/api/users', (req, res) => {
    data = getObjFromJsonFile(USERS)
    res.send(data)
})
app.get('/api/users/:id', (req, res) => {
    const UID = req.params.id; // get the actual id from part of the url :id save it as UID 
    users = getObjFromJsonFile(USERS) // get all the users.json as a js object, an aray of users
    user = users.filter(x => x.id == UID); // filter the users that have an 'id' of the url UID, the x is simply a temp name for the users array while inside the filter operation, we can call it whatever we like x , stuff blah
    // there should be exactly one record found, anything else is treated as garbage
    if(user.length == 1) {
        res.status(200).send(user)
    } else { 
        res.status(400).send('item not found')
    }
})
app.post('/api/users/add', (req, res) => {
    users = getObjFromJsonFile(USERS)
    console.log(req.body)
    //users.push()
    //res.status(200).send({'stuff': 'some api response'})
})

///////////
app.get('/api/messages', (req, res) => {
    data = getObjFromJsonFile(MESSAGES)
    res.send(data)
})
app.post('/api/message', (req, res) => {
    msgs = getObjFromJsonFile(MESSAGES)
    msgs.push(req.body)
    json = JSON.stringify(msgs, null, 4) 
    fs.writeFile(MESSAGES, json, (error) => {
        if (error) {
            console.error('eeeeeerrrrr', error);  
            throw error;
        } else {
            console.log('File saved OK')
        }

    })
    res.status(200).send({'stuff': 'api/messages response'})
})

app.post('/api/messages', (req, res) => {
    console.log(req)
    res.send(200)
})
app.get('/api/messages_sent', (req, res) => {
    data = getObjFromJsonFile(MESSAGES_SENT)
    res.send(data)
})


app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})