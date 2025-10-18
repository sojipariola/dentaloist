import { fetcher } from "../api";

export const getInvoices = async () => {
  return fetcher("/api/billing");
};
