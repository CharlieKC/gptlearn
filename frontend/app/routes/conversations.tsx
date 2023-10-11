// vite host gave me the host I was running on
// fetch("http://172.18.0.3:5173/api/csrf/").then((data) => {console.log(data)})
// actually worked...
// or using
// fetch("http://localhost:5173/api/csrf/").then((data) => {console.log(data)})


// const csrfUrl = "http://localhost:3000/api/csrfToken/";


const csrfUrl = "http://172.19.0.5/api/csrfToken/"; //This works, using nginx ipv4 found using docker network inspect

const BASE_URL = "http://172.19.0.5"

// make a function to wrap the fetch call and prepend the base url
const fetchApi = (url: string, options: any) => {
    // ensure the url starts with a slash
    if (!url.startsWith("/")) {
        url = "/" + url;
        console.log("Url should start with a slash, adding one now...");
    }
    console.log("Fetching from: ", BASE_URL + url);
    return fetch(BASE_URL + url, options);
}

console.log("Gonna fetch csrf token from ", csrfUrl);
fetchApi("/api/csrfToken", {
    method: 'GET',
    credentials: 'same-origin',
    headers: {
        'Content-Type': 'application/json'
    }
}).then(data => {
    // console log the X-CSRFToken header
    const csrfToken = data.headers.get('X-CSRFToken');
    if (csrfToken == null) {
        console.log("csrfToken is null, something went wrong");
    }
    console.log("X-CSRFToken: ", data.headers.get('X-CSRFToken'));

});



export default function Conversations() {
    return (
        <p id="conversation-page">Conversation page, placeholder, oi! woo</p>
        // render the first 5 charecters of the csrf token
    );
}
