import {
  redirect,
  type ActionFunctionArgs,
  type LoaderFunctionArgs,
} from "@remix-run/node"; // or cloudflare/deno
import { Form, useLoaderData } from "@remix-run/react";

import { fetchApi, BASE_URL, getSession, commitSession } from "../sessions";


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

type Message = {
  id: number,
  text: string,
  role: string,
  created_at: string,
}

type Conversation = {
  id: number,
  user: string,
  created_at: string,
  messages: Message[],
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
      <h1>Conversation page</h1>

      {/* Show all the conversations and messages */}
      {convs.results.map((conv: Conversation) => (
        <div key={conv.id}>
          <p>{conv.id}: {conv.created_at}</p>
          <p>Messages: </p>
          <ul>
            {conv.messages.map((msg) => (
              <li key={msg.id}>{msg.text}</li>
            ))}
          </ul>
        </div>
      ))}

      {/* Make a new conversation */}
      <Form method="POST">
        <button type="submit">Create New Conversation</button>
      </Form>
    </div>
  );
}
