import { json } from "@remix-run/node"; // or cloudflare/deno
import { useLoaderData } from "@remix-run/react";
// the nginx reverse proxy will set the header host to 127.0.0.1 and forward
// any requests to the backend, ok, what
const BASE_URL = "http://reverse_proxy"

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


export const loader = async () => {
    const csrfToken: string = await fetchApi("/api/csrfToken/", {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(data => {
        const token = data.headers.get('X-CSRFToken');
        if (token == null) {
            console.log("csrfToken is null, something went wrong");
        }
        return token ? token : "";

    })
    return json([
        { csrf: await csrfToken },
    ]);
};


export default function Conversations() {
    const csrfToken = useLoaderData<typeof loader>();

    return (
        <div id="conversation-page">
            <h1 id="conversation-page">Conversation page</h1>
            {csrfToken.map((token) => (
                <p key={token.csrf}>{token.csrf}</p>
            ))}
        </div>

    );
}
