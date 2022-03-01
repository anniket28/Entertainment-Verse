// Entertainment Verse Script Sheet

// Open Login Modal
function openLoginModal(){
    document.getElementById('login-modal').style.display='block'
}

// Close Login Modal
window.onclick=(event)=>{
    if(event.target==document.getElementById('login-modal')){
        document.getElementById('login-modal').style.display='none'
    }
}

// Open Sidebar Signup
function openSignupSidebar(){
    document.getElementById('signup').style.width="400px"
}

// Close Sidebar Signup
function closeSignupSidebar(){
    document.getElementById('signup').style.width="0px"
}

// Open User
function openUser(){
    document.getElementById('user').style.display='block'
}

// Close User
function closeUser(){
    document.getElementById('user').style.display='none'
}

// Open Profile Modal
function openProfile(){
    document.getElementById('profile-modal').style.display='block'
}

// Close Profile Modal
function closeProfile(){
    document.getElementById('profile-modal').style.display='none'
}


// Open Sidebar Change Pass
function openChangePassSidebar(){
    document.getElementById('changepass').style.width="400px"
}

// Close Sidebar Change Pass
function closeChangePassSidebar(){
    document.getElementById('changepass').style.width="0px"
}

// Open Logout Modal
function openLogoutModal(){
    document.getElementById('logout-modal').style.display='block'
}

// Close Logout Modal
function closeLogoutModal(){
    document.getElementById('logout-modal').style.display='none'
}

/* Search Box */
function searchBox(){
    document.getElementById('query').style.width='500px'
}

/* Search Box Rev*/
function searchBoxRev(){
    document.getElementById('query').style.width='250px'
}