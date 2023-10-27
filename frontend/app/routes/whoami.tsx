import type {
  LoaderFunctionArgs,
} from "@remix-run/node"; // or cloudflare/deno
import { useLoaderData } from "@remix-run/react";

import { fetchApi, getSession } from "../sessions";

export async function loader({
  request,
}: LoaderFunctionArgs) {
  const session = await getSession(
    request.headers.get("Cookie")
  );
  const userId = session.get("userId")
  const username = fetchApi("/api/whoami/", {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${await userId}`
    }
  }).then(data => {
    var jsonData = data.json();
    return jsonData;
  });
  return await username;
}


export default function WhoAmI() {
  const data = useLoaderData<typeof loader>();
  console.log(data);

  return (
    <div>
        <h1>WhoAmI</h1>
      {data ? <div className="whoami">{data.username}</div> : null}
    </div>
  );
}
