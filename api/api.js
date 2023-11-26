// first time use must run the npm installer to build the folder node_modules with all required packages/libraries
// node_modules folder will be gitignored, they stay on yr local machine once created and never comitted

// $ npm i 
// the packages are now installed, you only ever need to run npm i when new packages are added
// # start the web server using
// $ node api.js

// check it out, if the path starts with api/ then you will prolly get json back
// $ curl http:localhost:3000/api/users

// api urls:
// json GET  /api/messages, /api/messages_sent, /api/users, /api/users/:id
// json POST /api/messages

// html urls:
// html GET  /, /stuff

// require is like import in python, these files (console, express, cors etc) are in node_modules/
const express = require('express')
const app = express()
const PORT = 3000

let fs = require("fs") // the file system so we can read and write files
cors = require('cors')
app.use(cors());
app.use(express.json()) // json will be in req.body

app.use(function(req, res, next) {
    // default headers can be overriden later
    res.header("Access-Control-Allow-Origin", "*")
    res.header("Content-Type","application/json; charset=utf-8")
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Accept")
    next();
});

// some file paths to our json database!
const USERS_FN = 'data_files/users.json'
const MESSAGES_FN = 'data_files/messages.json'
const MESSAGES_SENT_FN = 'data_files/messages_sent.json'

// helper func: opens a json text file and returns it as a js object
function getObjFromJsonFile(fileName) {
    return JSON.parse(fs.readFileSync(fileName, 'utf8'))
}

// FYI in these section you get 2 vars, req + res
// the are the request and response variables 
// when a client sends an http request it sends hidden stuff we can access in req.params req.body req.headers etc
// when we responsd to a request we attach stuff such as status code along with headers before res.send()

// HTML ROUTES
// the default GET / returns index.html
app.get('/', (req, res) => {
    // overide the default header to html
    res.header("Content-Type", "text/html; charset=utf-8")
    // open the file and send the text content with an OK 200 code
    html = fs.readFileSync('html_files/index.html', 'utf8')
    res.status(200).send(html)
})
// a specific url to /stuff
app.get('/stuff', (req, res) => {
    res.header("Content-Type", "text/html; charset=utf-8")
    html = fs.readFileSync('html_files/stuff.html', 'utf8')
    res.send(html) // you actually need to set a status code
})



// API USERS ROUTES
// get all the users
app.get('/api/users', (req, res) => {
    users = getObjFromJsonFile(USERS_FN)
    res.send(users)
})

// get user by id
// get a variable from the urls argument[2] aka :id 
// : put whatever you like after :userid etc call it whatever you want
// it will get auto added to the req.params.id = 'ABC'
app.get('/api/users/:id', (req, res) => {
    const UID = req.params.id; // get the actual id from part of the url :id save it as UID 
    // SECURITY: this is user input from the urls of whatever they typed in, make sure it is safe and not malicious <script>js.get('http://hacker.com')
    // TODO write a regex to make safe then check it length etc
    users = getObjFromJsonFile(USERS_FN) // get all the users.json as a js object
    user = users.filter(x => x.id == UID); // filter the users into a new array that have an 'id' of the url UID
    // FYI the x and x.id is simply a temp name for the users array while inside the filter operation, we can call it whatever we like x , stuff blah
    // user should be an array with exactly one record, user[0],  anything else is treated as garbage
    if(user.length == 1) {
        res.status(200).send(user)
    } else { 
        res.status(400).send('item not found')
    }
})


// API MESSAGES ROUTES
// get all messages
app.get('/api/messages', (req, res) => {
    msgs = getObjFromJsonFile(MESSAGES_FN)
    res.send(msgs)
})
// post a message json will create a new record and saved
app.post('/api/message', (req, res) => {
    msgs = getObjFromJsonFile(MESSAGES_FN) // get all the messages as a js array
    msgs.push(req.body) // add the posted json to the array
    json = JSON.stringify(msgs, null, 4) // turn the msgs js object into a json string with pretty indent 4
    fs.writeFile(MESSAGES_FN, json, (error) => { // save the string to json file
        if (error) {
            console.log('error: ', error);  
            res.status(500).send('The data could not be saved, try again later') 
        } else {
            console.log('File saved OK', MESSAGES_FN)
            res.status(200).send(msgs) // send a 200 and we can also send the new data we actually saved
        }

    })
})

// API MESSAGES_SENT ROUTES
app.get('/api/messages_sent', (req, res) => {
    msgs = getObjFromJsonFile(MESSAGES_SENT_FN)
    res.send(msgs)
})

// SERVER at last we run the server 
// start the server on the PORT we set at the top
// all requests sent to this server will be handled by the above app routes
app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`)
})