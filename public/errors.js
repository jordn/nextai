
// window.addEventListener("error", (ErrorEvent) => {
//     console.log("Handling error");
//     const queryParams = new URLSearchParams(JSON.stringify(ErrorEvent)).toString();

//     fetch({method: "GET", url: "http://alex-brain:3050/error" + queryParams})
//     console.log("after logs");
// })

window.onerror = function (event, source, lineno, colno, error) {
    console.log("Handling error");
    const errorData = {event, source, lineno, colno, errorMessage: error.messsage, errorTrace: error.stack}
    
    fetch("http://alex-brain:3070/error?error=" + encodeURIComponent(JSON.stringify(errorData))).then((res)=> {
        console.log("after logs", res);
    })
    
}