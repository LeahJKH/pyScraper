"use client"
import  Style  from "./page.module.css"
import { useState } from "react"

export default function LogIn () {

  const [passWord, setPassword] = useState("");
  const [UserName, setUserName] = useState("");


  function passHandler(e: string) {
    setPassword(e)

  }
    function userNameHandler(e: string) {
    setUserName(e)

  }
  console.log(passWord)
  console.log(UserName)
  
  function LogIn(u: string, p: string) {
    console.log(u + " " + p)
  }

return (
  <>
  <div className={Style.container}>
    <h1 className={Style.Toptext}>Log in</h1>
    <label>Username: <input type="text" placeholder="joblooper" id="userField" className={Style.InputFields} onChange={(e) => userNameHandler(e.target.value)}/></label>
    <label>Password: <input type="password" placeholder="*******" id="passField" className={Style.InputFields} onChange={(e) => passHandler(e.target.value)}/></label>
    <button type="button" className={Style.btnLog} onClick={LogIn(UserName, passWord)}>Log in</button>
  </div>
  </>
)
}