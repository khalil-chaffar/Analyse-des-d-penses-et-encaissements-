const User = require('../models/user.model');

const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

const login = (req, res) => {
    let {email , password} = req.body;
    User.findOne({email:email})
        .then(
            (user)=>{
                if(!user){
                    res.send({ message: 'email or password invalid'});
                }else{
                    let valid = bcrypt.compareSync(password, user.password);
                    if(!valid){
                        res.send({ message: 'email or password invalid'})
                    }else{
                        let payload = {
                            _id: user._id,
                            name: user.name,
                            lastname: user.lastname,
                            email: user.email
                        }
                        let token = jwt.sign(payload, '123456789');
                        res.send({myToken: token});
                    }
                }

            }
        )
}

const register = (req, res) => {
    let data = req.body;
    let user = new User(data);
    user.password = bcrypt.hashSync(user.password, 10);
    user.save()
        .then(() => {
            res.status(201).json({ message: 'User created' });
        })
        .catch(err => {
            res.status(400).json({ error: err.message });
        });
}

module.exports = {
    login,
    register
}