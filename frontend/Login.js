import { useState } from "react";
import axios from "axios";

function Login(props){
    const [loginForm, setLoginForm] = useState({
        email: "",
        password: ""
    })

    function logMeIn(event){
        axios({
            method: "POST",
            url: "/token",
            data:{
                email: loginForm.email,
                password: loginForm.password
            }
        }).then((response) => {
            props.setToken(response.data.access_token);
        }).catch((error) => {
            if (error.response){
                console.log(error.response);
            }
        })
        setLoginForm(({
            email: "",
            password: ""
        }))
        event.preventDefault()
    }
    function handleChange(event){
        const {value, name} = event.target;
        setLoginForm(prevNote => ({
            ...prevNote, [name]: value})
        )}
        return (
            <div>
                <h1>Login</h1>
                <form className="login">
                    <input onChange={handleChange} type={loginForm.email} name="email" placeholder="Email"/>
                    <input onChange={handleChange} type="password" placeholder="Password" value={loginForm.password}/>
                </form>

            </div>
        );
    }

    export default Login;
