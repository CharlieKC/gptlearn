// app/sessions.ts
import { createCookieSessionStorage, redirect } from "@remix-run/node"; // or cloudflare/deno

type SessionData = {
  userId: string;
};

type SessionFlashData = {
  error: string;
};


export const BASE_URL = "http://reverse_proxy"

// make a function to wrap the fetch call and prepend the base url
export const fetchApi = (url: string, options: any) => {
  // ensure the url starts with a slash
  if (!url.startsWith("/")) { throw new Error("URL must start with a slash"); }

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
    if (jsonData.token == null || jsonData.expiry == null) {
      console.error("Error fetching token: ", jsonData);
      return null;
    }
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

        // Set this to the domain once I have once
        // domain: "remix.run",
        httpOnly: true,
        path: "/",
        sameSite: "lax",
        secrets: ["s3cret1"],
        secure: true,
      },
    }
  );

export { getSession, commitSession, destroySession };
