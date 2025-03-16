import type { UseFetchOptions } from "nuxt/app";
// export default <T>(url: string, options: UseFetchOptions<T> = {}) => {
//   const login_token = useCookie("login_token");
//   const config = useRuntimeConfig();

//   const defaults: UseFetchOptions<T> = {
//     headers: { Authorization: `Bearer ${login_token.value ?? ""}` },
//   };
//   const settings = defu(options, defaults);

//   return useLazyFetch(url, settings);
// };

export function useApi<T>(
  url: string | (() => string),
  options: UseFetchOptions<T> = {}
) {
  const login_token = useCookie("login_token");
  const config = useRuntimeConfig();

  const defaults: UseFetchOptions<T> = {
    baseURL: config.public.CDN_HOST + "/api",
    headers: { Authorization: `Bearer ${login_token.value ?? ""}` },
    credentials: "omit",
    onRequest({ request, options }) {},
    onResponseError({ request, response, options }) {},
    $fetch: useNuxtApp().$api as typeof $fetch,
    ...options,
  };

  return useFetch(url, defaults);
}
