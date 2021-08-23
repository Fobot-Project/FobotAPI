const functions = require("firebase-functions");
const admin = require("firebase-admin");


var serviceAccount = require("./permission.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://test-bot-hldq-default-rtdb.firebaseio.com"
});


const express = require("express");
const app = express();
const db = admin.firestore();

const cors = require("cors");
app.use(cors({origin:true}))



// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
// exports.helloWorld = functions.https.onRequest((request, response) => {
//   functions.logger.info("Hello logs!", {structuredData: true});
//   response.send("Hello from Firebase!");
// });

//Routes
app.get('/hello-world', (req,res) =>{
    return res.status(200).send("Hello world!");

});

//Upload
//Post
app.post('/api/create-menu', (req,res) =>{
    (async () => {

        try
        {
            await db.collection('User').doc('baoWAOSj1kSObBVDcyD2').collection('menu').doc('/'+req.body.id + '/')
            .create({
                name:req.body.name,
                price:req.body.price
            })

            return res.status(200).send();
        }
        catch (error)
        {
            console.log(error);
            return res.status(500).send(error);
        }
    })();

});

//Read
//Get
//get order inforamtion by ID
app.get('/api/getorder/:id', (req,res) =>{
    (async () => {

        try
        {
            const document = db.collection('orders').doc(req.params.id);
            let order = await document.get();
            let response = order.data();


            return res.status(200).send(response);
        }
        catch (error)
        {
            console.log(error);
            return res.status(500).send(error);
        }
    })();

});
//get all the orders 

app.get('/api/getorders', (req,res) =>{
    (async () => {

        try
        {
            let query =db.collection('orders');
            let response =[];
            await query.get().then(querySnapshot =>{
                let docs = querySnapshot.docs;

                for(let doc of docs)
                {
                    const selectedorder = {
                        id : doc.id,
                        orders: doc.get('orders')

                    };
                    response.push(selectedorder);
                }
                return response;
            })


            return res.status(200).send(response);
        }
        catch (error)
        {
            console.log(error);
            return res.status(500).send(error);
        }
    })();

});


//Update
//Put

app.put('/api/update-menu/:id', (req,res) =>{
    (async () => {

        try
        {
            const document = db.collection('User').doc('baoWAOSj1kSObBVDcyD2').collection('menu').doc(req.params.id);

            await document.update({
                name: req.body.name,
                price:req.body.price
            });

            return res.status(200).send();
        }
        catch (error)
        {
            console.log(error);
            return res.status(500).send(error);
        }
    })();

});

//Delete
//Delete
app.delete('/api/delete-menu/:id', (req,res) =>{
    (async () => {

        try
        {
            const document = db.collection('User').doc('baoWAOSj1kSObBVDcyD2').collection('menu').doc(req.params.id);
            await document.delete();
            return res.status(200).send();
        }
        catch (error)
        {
            console.log(error);
            return res.status(500).send(error);
        }
    })();

});
//export the api to Firebase cloud functions
exports.app = functions.https.onRequest(app);
