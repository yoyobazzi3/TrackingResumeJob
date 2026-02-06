import { apiFetch } from "./client";

export async function signup(
  email: string,
  password: string,
  firstName: string,
  lastName: string
) {
  return apiFetch("/auth/signup", {
    method: "POST",
    body: JSON.stringify({
      email,
      password,
      first_name: firstName,
      last_name: lastName,
    }),
  });
}

export async function login(email: string, password: string) {
  return apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}
