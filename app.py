<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>B-Techno | Animated App</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    * {margin: 0; padding: 0; box-sizing: border-box; font-family: "Segoe UI", sans-serif;}

    body {
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background: linear-gradient(135deg, #2a5298, #1e3c72);
    }

    .container {
      width: 1000px;
      height: 600px;
      background: #fff;
      border-radius: 14px;
      display: flex;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    /* Left Login Panel */
    .form-container {
      width: 40%;
      background: linear-gradient(135deg, #2a5298, #1e3c72);
      color: #fff;
      padding: 40px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      animation: slideInLeft 1s ease;
    }

    .form-container h2 {text-align: center; margin-bottom: 20px;}
    .form-container input {
      margin: 12px 0;
      padding: 12px;
      border: none;
      border-radius: 8px;
      outline: none;
    }

    .btn {
      margin-top: 15px;
      padding: 12px;
      border: none;
      border-radius: 8px;
      background: #46c7c7;
      color: #fff;
      font-weight: bold;
      cursor: pointer;
      transition: 0.3s;
    }
    .btn:hover {background: #37a3a3;}

    .forgot, .signup-text {font-size: 13px; text-align: center; margin-top: 10px;}
    .signup-text a {color: #fff; font-weight: bold;}

    .social-login {margin-top: 15px; text-align: center;}
    .social-login a {
      margin: 0 8px;
      color: #fff;
      background: rgba(255,255,255,0.2);
      padding: 10px;
      border-radius: 50%;
      transition: 0.3s;
    }
    .social-login a:hover {background: #fff; color: #1e3c72;}

    /* Right Illustration Panel */
    .illustration-container {
      width: 60%;
      padding: 40px;
      text-align: center;
      animation: fadeIn 1.2s ease;
    }
    .illustration-container img {width: 80%; margin-bottom: 20px;}
    .illustration-container h3 {margin-bottom: 10px; color: #222;}
    .illustration-container p {color: #666; margin-bottom: 20px;}

    /* App Pages */
    .app-container {display: none; flex-direction: column; align-items: center; justify-content: center; width: 100%; text-align: center;}
    .nav-buttons {margin-top: 20px;}
    .nav-buttons button {
      margin: 8px;
      padding: 12px 20px;
      border: none;
      border-radius: 10px;
      background: #2a5298;
      color: white;
      cursor: pointer;
      transition: 0.3s;
    }
    .nav-buttons button:hover {background: #1e3c72;}

    /* Animations */
    @keyframes slideInLeft {from {transform: translateX(-100%);} to {transform: translateX(0);}}
    @keyframes fadeIn {from {opacity: 0;} to {opacity: 1;}}
  </style>
</head>
<body>
  <div class="container" id="login-container">
    <!-- Left Sign In Panel -->
    <div class="form-container">
      <h2>Sign In</h2>
      <input type="text" id="username" placeholder="Username">
      <input type="password" id="password" placeholder="Password">
      <button class="btn" onclick="login()">Sign In</button>
      <p class="forgot">Forgot Password?</p>
      <div class="social-login">
        <a href="#"><i class="fab fa-facebook-f"></i></a>
        <a href="#"><i class="fab fa-twitter"></i></a>
        <a href="#"><i class="fab fa-google"></i></a>
      </div>
      <p class="signup-text">Don’t have an account? <a href="#">Sign Up</a></p>
    </div>

    <!-- Right Illustration Panel -->
    <div class="illustration-container">
      <img src="https://i.ibb.co/6tL9pQz/software-illustration.png" alt="Illustration">
      <h3>Technical Analysis of Software Requirements</h3>
      <p>Curabitur sed lectus in dui consectetur rhoncus sit amet nec sapien. Donec vel felis non tellus tristique condimentum.</p>
    </div>
  </div>

  <!-- App Pages After Login -->
  <div class="container app-container" id="app-container">
    <h2 id="welcome-text">Welcome!</h2>
    <div class="nav-buttons">
      <button onclick="showPage('Home')">Home</button>
      <button onclick="showPage('Dashboard')">Dashboard</button>
      <button onclick="showPage('Profile')">Profile</button>
      <button onclick="showPage('Feedback')">Feedback</button>
      <button onclick="logout()">Logout</button>
    </div>
    <div id="page-content" style="margin-top:20px; font-size:16px; color:#333;"></div>
  </div>

  <script>
    function login() {
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      if (username && password) {
        document.getElementById("login-container").style.display = "none";
        document.getElementById("app-container").style.display = "flex";
        document.getElementById("welcome-text").innerText = "Welcome, " + username + "!";
      } else {
        alert("Please enter username and password.");
      }
    }

    function logout() {
      document.getElementById("app-container").style.display = "none";
      document.getElementById("login-container").style.display = "flex";
    }

    function showPage(page) {
      let content = "";
      if (page === "Home") content = "🏠 This is the Home page.";
      if (page === "Dashboard") content = "📊 Dashboard with charts and analytics.";
      if (page === "Profile") content = "👤 User profile details shown here.";
      if (page === "Feedback") content = "📝 Feedback form and submissions.";
      document.getElementById("page-content").innerText = content;
    }
  </script>
</body>
</html>
