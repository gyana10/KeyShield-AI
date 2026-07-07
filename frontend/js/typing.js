let keyEvents = [];

const typingArea = document.getElementById("typingArea");

typingArea.addEventListener("keydown", function(e){

    keyEvents.push({

        key:e.key,

        type:"keydown",

        time:performance.now()

    });

});

typingArea.addEventListener("keyup", function(e){

    keyEvents.push({

        key:e.key,

        type:"keyup",

        time:performance.now()

    });

});