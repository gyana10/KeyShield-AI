function extractFeatures(events){

    const holdTimes = [];

    const flightTimes = [];

    let previousKeyUp = null;

    let totalDuration = 0;

    let backspaces = 0;

    const keyDownMap = {};

    events.forEach(event=>{

        if(event.key==="Backspace"){

            backspaces++;

        }

        if(event.type==="keydown"){

            keyDownMap[event.key]=event.time;

            if(previousKeyUp!==null){

                flightTimes.push(

                    event.time-previousKeyUp

                );

            }

        }

        if(event.type==="keyup"){

            if(keyDownMap[event.key]!=null){

                holdTimes.push(

                    event.time-keyDownMap[event.key]

                );

            }

            previousKeyUp=event.time;

        }

    });

    if(events.length>0){

        totalDuration=

            events[events.length-1].time-

            events[0].time;

    }

    return{

        holdTimes,

        flightTimes,

        totalDuration,

        backspaces

    };

}