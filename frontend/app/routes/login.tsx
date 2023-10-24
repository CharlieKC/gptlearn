import type {
  ActionFunctionArgs,
  LoaderFunctionArgs,
} from "@remix-run/node"; // or cloudflare/deno
import { json, redirect } from "@remix-run/node"; // or cloudflare/deno
import { useLoaderData } from "@remix-run/react";

import { fetchApi, login, getSession, commitSession } from "../sessions";

export async function loader({
  request,
}: LoaderFunctionArgs) {
  console.log("Login loader!");
  const session = await getSession(
    request.headers.get("Cookie")
  );

  if (session.has("userId")) {
    // Redirect to the home page if they are already signed in.
    console.log("User already signed in, redirecting to home page");
    return redirect("/");
  }
  console.log("User is not logged in!");

  const data = { error: session.get("error") };

  return json(data, {
    headers: {
      "Set-Cookie": await commitSession(session),
    },
  });
}

export async function action({
  request,
}: ActionFunctionArgs) {
  console.log("Login action!")
  const session = await getSession(
    request.headers.get("Cookie")
  );
  const form = await request.formData();
  const username = form.get("username");
  const password = form.get("password");

  const loginResponse = await login(
    username?.toString() ?? "",
    password?.toString() ?? ""
  );
  console.log("jwt:", loginResponse.token, "username:", username);

  if (loginResponse == null) {
    session.flash("error", "Invalid username/password");

    // Redirect back to the login page with errors.
    return redirect("/login", {
      headers: {
        "Set-Cookie": await commitSession(session),
      },
    });
  }

  console.log("Setting userId in session")
  session.set("userId", loginResponse.token);
  console.log("Session has userId:", session.has("userId"));

  const whoami = fetchApi("/api/whoami/", {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${await loginResponse.token}`
    }
  }).then(data => {
    var jsonData = data.json();
    return jsonData;
  });
  console.log("whoami: ", await whoami);


  // Login succeeded, send them to the home page.
  return redirect("/", {
    headers: {
      "Set-Cookie": await commitSession(session, {expires: new Date(loginResponse.expiry)})
    },
  });
}

export default function Login() {
  const { error } = useLoaderData<typeof loader>();

  return (
    <div>
      {error ? <div className="error">{error}</div> : null}
      <form method="POST">
        <div>
          <p>Please sign in</p>
        </div>
        <label>
          Username: <input type="text" name="username" />
        </label>
        <label>
          Password:{" "}
          <input type="password" name="password" />
        </label>
        <button type="submit">Log in</button>
      </form>
    </div>
  );
}
