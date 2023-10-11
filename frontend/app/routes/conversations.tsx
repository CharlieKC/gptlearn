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
        // render the first 5 characters of the csrf token
    );
}
