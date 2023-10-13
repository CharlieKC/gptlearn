import type {
  ActionFunctionArgs,
  LoaderFunctionArgs,
} from "@remix-run/node"; // or cloudflare/deno
import { json, redirect } from "@remix-run/node"; // or cloudflare/deno
import { useLoaderData } from "@remix-run/react";

import { getSession, commitSession } from "../sessions";

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


export async function loader({
  request,
}: LoaderFunctionArgs) {
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

    let session = await getSession(request.headers.get("Cookie"));
    session.set("csrftoken", csrfToken);

    // check the token works by calling a view that requires a csrf token
    const response = fetchApi("/api/check-csrfToken/", {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(data => {
        var jsonData = data.json();
        return jsonData;
    })
    console.log("jsonData: ", await response);

    // try and login, but getting csrf token not set errors
    // try logging in with foobar (@example.com), defaultPass
    // /api/auth/login/

    // create basic
        //     // csrfmiddlewaretoken: csrfToken,
    let username = 'foobar';
    let password = 'defaultPass';
    let auth = btoa(`${username}:${password}`);
    let authHeader = `Basic ${auth}`;


    const loginResponse = fetchApi("/api/auth/getToken/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': authHeader,
        },
        }).then(data => {
            // return data
            var jsonData = data.json();
            // this should have two fields, expiry and token
            return jsonData;
        });
    console.log("loginResponse: ", await loginResponse);
    let token = await loginResponse.then(data => {
        return data.token;
    });

    // try another api call
    const convs = fetchApi("/api/conversation/", {
        method: 'GET',
        headers: {
            'Authorization': `Token ${await token}`
        }
    }).then(data => {
        var jsonData = data.json();
        return jsonData;
    }
    );
    console.log("convs: ", await convs)

    const whoami = fetchApi("/api/whoami/", {
        method: 'GET',
        headers: {
            'Authorization': `Token ${await token}`
        }
    }).then(data => {
        var jsonData = data.json();
        return jsonData;
    }
    );
    console.log("whoami: ", await whoami)





    return json([
        { csrf: token },
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
