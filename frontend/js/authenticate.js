const token = localStorage.getItem("token");

document
.getElementById("authenticateBtn")
.addEventListener("click", async ()=>{

    const sample={

        H_period:0.12

    };

    const response=await fetch(

        "http://127.0.0.1:8000/authenticate",

        {

            method:"POST",

            headers:{

                "Content-Type":"application/json",

                "Authorization":"Bearer "+token

            },

            body:JSON.stringify(sample)

        }

    );

    const result=await response.json();

    document
    .getElementById("result")
    .innerHTML=

    JSON.stringify(result,null,2);

});