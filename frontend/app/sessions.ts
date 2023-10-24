// app/sessions.ts
import { createCookieSessionStorage, redirect } from "@remix-run/node"; // or cloudflare/deno

type SessionData = {
  userId: string;
};

type SessionFlashData = {
  error: string;
};


// const BASE_URL = "http://reverse_proxy"
export const BASE_URL = "http://localhost:8000"

// make a function to wrap the fetch call and prepend the base url
export const fetchApi = (url: string, options: any) => {
  // ensure the url starts with a slash
  if (!url.startsWith("/")) {
    url = "/" + url;
    console.log("Url should start with a slash, adding one now...");
  }
  console.log("Fetching from: ", BASE_URL + url);
  return fetch(BASE_URL + url, options).then(response => {
    if (!response.ok) {
      if (response.status == 401) {
        console.log("Got 401")
      }
      throw new Error(`Fetch error: ${response.status} ${response.statusText}`);
    }
    return response;
  });
}

const validateCredentials = async (username: string, password: string) => {
  const auth = btoa(`${username}:${password}`);
  const authHeader = `Basic ${auth}`;

  const loginResponse = fetchApi("/api/auth/getToken/", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': authHeader,
    },
  }).then(data => {
    var jsonData = data.json();
    // this should have two fields, expiry and token
    // can I also get the username here?
    return jsonData;
  }).catch(error => {
    console.error("Error fetching token: ", error);
    return null;
  });
  return loginResponse;
};

export const login = async (username: string, password: string) => {
  let credentialResponse = await validateCredentials(username, password);
  if (credentialResponse == null) {
    console.error("Error validating credentials");
    return;
  }
  console.log("Token: ", credentialResponse.token, " Expiry: ", credentialResponse.expiry);
  return credentialResponse;
}


const { getSession, commitSession, destroySession } =
  createCookieSessionStorage<SessionData, SessionFlashData>(
    {
      // a Cookie from `createCookie` or the CookieOptions to create one
      cookie: {
        name: "__session",

        // all of these are optional
        // domain: "remix.run",
        // Expires can also be set (although maxAge overrides it when used in combination).
        // Note that this method is NOT recommended as `new Date` creates only one date on each server deployment, not a dynamic date in the future!
        // ToDo actually set this via the jwt.
        // expires: new Date(Date.now() + 60_000),
        httpOnly: true,
        // maxAge: 60,
        path: "/",
        sameSite: "lax",
        secrets: ["s3cret1"],
        secure: true,
      },
    }
  );

export { getSession, commitSession, destroySession };
