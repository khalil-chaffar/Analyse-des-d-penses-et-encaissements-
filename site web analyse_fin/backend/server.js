const express = require('express');
const cors = require('cors');

require('./config/connect');

const userRouter = require('./routes/user.route');

const app = express();
app.use(cors());
app.use(express.json());

app.use('/user/', userRouter);




app.listen(3000, () => {
    console.log('server work');
});