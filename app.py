// app.js
// All-in-one: serves front-end + provides backend auth with SQLite
const express = require('express');
const bcrypt = require('bcryptjs');
const Database = require('better-sqlite3');
const path = require('path');

const app = express();
const db = new Database(path.join(__dirname, 'users.db'));

// Initialize DB
db.prepare(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
  )
`).run();

app.use(express.json());

// ---------- Frontend (single-page HTML) ----------
app.get('/', (req, res) => {
  res.send(`<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Two-Panel Auth</title>
  <style>
    :root{
      --g1: linear-gradient(135deg,#0f172a 0%,#0b3b63 40%,#2c6b5f 100%);
      --accent1: #7b61ff;
      --accent2: #00d4ff;
      --muted: rgba(255,255,255,0.7);
      font-family: Arial, sans-serif;
    }
    body{margin:0;background:var(--g1);color:#fff;min-height:100vh;display:grid;place-items:center}
    .wrap{display:grid;grid-template-columns:1fr 1fr;gap:40px;padding:40px;width:100%;max-width:1100px}
    .panel{background:rgba(255,255,255,0.05);border-radius:16px;padding:36px;box-shadow:0 8px 30px rgba(0,0,0,0.6)}
    .tab{display:inline-block;padding:8px 14px;border-radius:10px;cursor:pointer;color:var(--muted)}
    .tab.active{background:rgba(255,255,255,0.1);color:#fff}
    input{width:100%;padding:12px;border-radius:10px;border:none;margin-top:6px;background:rgba(255,255,255,0.1);color:#fff}
    .btn{margin-top:10px;padding:12px;width:100%;border:none;border-radius:10px;background:linear-gradient(90deg,var(--accent1),var(--accent2));cursor:pointer;color:#fff;font-weight:bold}
    .btn:hover{opacity:0.9}
    .app{display:none;padding:20px}
    .nav a{margin-right:10px;color:#fff;text-decoration:none}
    .cube{width:90px;height:90px;position:relative;transform-style:preserve-3d;animation:spin 9s linear infinite}
    .cube-face{position:absolute;width:90px;height:90px;display:flex;align-items:center;justify-content:center;font-weight:bold;color:#fff}
    .f1{background:#7b61ff;transform:translateZ(45px)}
    .f2{background:#0ea5a4;transform:rotateY(90deg) translateZ(45px)}
    .f3{background:#ef4444;transform:rotateY(180deg) translateZ(45px)}
    .f4{background:#7c3aed;transform:rotateY(-90deg) translateZ(45px)}
    @keyframes spin{0%{transform:rotateX(10deg) rotateY(0)}100%{transform:rotateX(10deg) rotateY(360deg)}}
  </style>
</head>
<body>
  <main class="wrap">
    <section class="panel">
      <div>
        <span id="tab-login" class="tab active">Sign In</span>
        <span id="tab-signup" class="tab">Sign Up</span>
      </div>
      <div id="forms">
        <form id="login-form">
          <h2>Login</h2>
          <input id="login-username" placeholder="Username" required>
          <input id="login-password" type="password" placeholder="Password" required>
          <button type="button" class="btn" id="btn-signin">Sign In</button>
        </form>
        <form id="signup-form" style="display:none">
          <h2>Create Account</h2>
          <input id="signup-name" placeholder="Full Name" required>
          <input id="signup-email" type="email" placeholder="Email" required>
          <input id="signup-username" placeholder="Username" required>
          <input id="signup-password" type="password" placeholder="Password" required>
          <button type="button" class="btn" id="btn-signup">Sign Up</button>
          <button type="button" class="btn" id="btn-cancel">Cancel</button>
        </form>
      </div>
    </section>
    <section class="panel" style="display:flex;align-items:center;justify-content:center;flex-direction:column">
      <div class="cube">
        <div class="cube-face f1">Req</div>
        <div class="cube-face f2">UI</div>
        <div class="cube-face f3">API</div>
        <div class="cube-face f4">DB</div>
      </div>
      <p style="margin-top:20px;text-align:center">Technical Analysis of Software Requirements</p>
    </section>
  </main>

  <div class="app" id="app-root">
    <div class="nav" id="topnav"></div>
    <div id="app-main"></div>
  </div>

<script>
const byId=id=>document.getElementById(id);
const tabLogin=byId('tab-login'), tabSignup=byId('tab-signup');
const loginForm=byId('login-form'), signupForm=byId('signup-form');

tabLogin.onclick=()=>{tabLogin.classList.add('active');tabSignup.classList.remove('active');signupForm.style.display='none';loginForm.style.display='block'};
tabSignup.onclick=()=>{tabSignup.classList.add('active');tabLogin.classList.remove('active');loginForm.style.display='none';signupForm.style.display='block'};
byId('btn-cancel').onclick=()=>tabLogin.onclick();

async function postJSON(url,data){
  const res=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  return res.json();
}

byId('btn-signup').onclick=async()=>{
  const data={name:byId('signup-name').value,email:byId('signup-email').value,username:byId('signup-username').value,password:byId('signup-password').value};
  const r=await postJSON('/signup',data);
  alert(r.ok?'Account created':'Signup failed: '+r.message);
  if(r.ok) tabLogin.onclick();
};

byId('btn-signin').onclick=async()=>{
  const data={username:byId('login-username').value,password:byId('login-password').value};
  const r=await postJSON('/login',data);
  if(r.ok) startApp(r.user); else alert('Login failed: '+r.message);
};

function startApp(user){
  document.querySelector('main.wrap').style.display='none';
  const app=byId('app-root');app.style.display='block';
  const nav=byId('topnav');nav.innerHTML='';
  ['Home','Dashboard','Profile','Feedback','Logout'].forEach(p=>{
    const a=document.createElement('a');a.href='#';a.textContent=p;
    a.onclick=(e)=>{e.preventDefault();route(p,user)};nav.appendChild(a);
  });
  route('Home',user);
}
function route(page,user){
  const main=byId('app-main');
  if(page==='Logout'){location.reload();return}
  if(page==='Home') main.innerHTML='<h2>Welcome '+user.name+'</h2><p>This is Home.</p>';
  if(page==='Dashboard') main.innerHTML='<h2>Dashboard</h2><p>Charts here.</p>';
  if(page==='Profile') main.innerHTML='<h2>Profile</h2><p>'+user.username+' ('+user.email+')</p>';
  if(page==='Feedback') main.innerHTML='<h2>Feedback</h2><textarea style="width:100%;height:100px"></textarea>';
}
</script>
</body>
</html>`);
});

// ---------- API ----------
const findByUsername = db.prepare('SELECT * FROM users WHERE username=?');
const findByEmail = db.prepare('SELECT * FROM users WHERE email=?');
const insertUser = db.prepare('INSERT INTO users (name,email,username,password_hash,created_at) VALUES (@name,@email,@username,@password_hash,@created_at)');

app.post('/signup', async (req,res)=>{
  const {name,email,username,password} = req.body||{};
  if(!name||!email||!username||!password) return res.json({ok:false,message:'Missing fields'});
  if(findByUsername.get(username)) return res.json({ok:false,message:'Username exists'});
  if(findByEmail.get(email)) return res.json({ok:false,message:'Email exists'});
  const hash = await bcrypt.hash(password,10);
  insertUser.run({name,email,username,password_hash:hash,created_at:new Date().toISOString()});
  res.json({ok:true});
});

app.post('/login', async (req,res)=>{
  const {username,password}=req.body||{};
  const user=findByUsername.get(username);
  if(!user) return res.json({ok:false,message:'Invalid credentials'});
  const ok=await bcrypt.compare(password,user.password_hash);
  if(!ok) return res.json({ok:false,message:'Invalid credentials'});
  res.json({ok:true,user:{id:user.id,name:user.name,username:user.username,email:user.email}});
});

const PORT=3000;
app.listen(PORT,()=>console.log('Server running at http://localhost:'+PORT));
