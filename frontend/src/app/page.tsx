import  Style  from "./page.module.css"
export default function logIn () {
return (
  <>
  <div className={Style.container}>
    <h1 className={Style.Toptext}>Log in</h1>
    <label>Username: <input type="text" placeholder="joblooper" id="userField" className={Style.InputFields}/></label>
    <label>Password: <input type="password" placeholder="*******" id="passField" className={Style.InputFields}/></label>
    <button type="button" className={Style.btnLog}>Log in</button>
  </div>
  </>
)
}