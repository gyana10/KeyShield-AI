const API_URL = "http://127.0.0.1:8000";

document
.getElementById("registerForm")
.addEventListener("submit", async function(e){

    e.preventDefault();

    const data = {

        username: document.getElementById("username").value,

        email: document.getElementById("email").value,

        password: document.getElementById("password").value

    };

    const response = await fetch(

        API_URL + "/register",

        {

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify(data)

        }

    );

    const result = await response.json();

    const message = document.getElementById("message");

    if(response.ok){

        message.style.color="lime";

        message.innerHTML="✅ Registration Successful";

        setTimeout(()=>{

            window.location.href="login.html";

        },1500);

    }

    else{

        message.style.color="red";

        message.innerHTML=result.detail;

    }

});