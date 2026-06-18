import axios from "axios";

export const api = axios.create({
  baseURL: "https://transaction-validator-api-2hlm.onrender.com/api",
});