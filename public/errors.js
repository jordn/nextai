
// window.addEventListener("error", (ErrorEvent) => {
//     console.log("Handling error");
//     const queryParams = new URLSearchParams(JSON.stringify(ErrorEvent)).toString();

//     fetch({method: "GET", url: "http://alex-brain:3050/error" + queryParams})
//     console.log("after logs");
// })

window.onerror = function (error, source, lineno, colno, error) {
    console.log("Handling error");
    const errorData = {error, source, lineno, colno, error}
    
    // const queryParams = new URLSearchParams(JSON.stringify(ErrorEvent)).toString();

    fetch("http://alex-brain:3050/error", {method: "POST", url: "http://alex-brain:3050/error", body: JSON.stringify(ErrorEvent)})
    console.log("after logs");
}