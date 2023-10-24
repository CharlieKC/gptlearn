import {
    redirect,
    type ActionFunctionArgs,
  type LoaderFunctionArgs,
} from "@remix-run/node"; // or cloudflare/deno
import { Form, useLoaderData } from "@remix-run/react";

import { BASE_URL, getSession, commitSession } from "../sessions";

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
    const session = await getSession(request.headers.get("Cookie"));

    // try another api call
    const convs = fetchApi("/api/conversation/", {
        method: 'GET',
        headers: {
            'Authorization': `Token ${await session.get("userId")}`
        }
    }).then(data => {
        var jsonData = data.json();
        return jsonData;
    }
    );
    console.log("convs: ", await convs)
    return convs
};
type Conversation = {
    id: number,
    user: string,
    created_at: string,
}

export const action = async ({
  request,
}: ActionFunctionArgs) => {
  const session = await getSession(request.headers.get("Cookie"));
  const makeConv = fetchApi("/api/conversation/", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${await session.get("userId")}`
    },
    // body: JSON.stringify({
    //     "user": 1,
    // })
  }).then(data => {
    var jsonData = data.json();
    return jsonData;
  });
  console.log("new conv: ", await makeConv);
  return redirect("/conversations");
};

export default function Conversations() {
    const convs = useLoaderData<typeof loader>();

    return (
        <div id="conversation-page">
            <h1 id="conversation-page">Conversation page</h1>
            {convs.results.map((conv: Conversation) => (
                <p key={conv.id}>{conv.id}: {conv.created_at}</p>
            ))}
        <Form method="POST">
            <button type="submit">Create New Conversation</button>
        </Form>
        </div>
    );
}
