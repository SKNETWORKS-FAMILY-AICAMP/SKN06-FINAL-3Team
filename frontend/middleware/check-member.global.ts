export default defineNuxtRouteMiddleware(async (to, from) => {
  const login_token = useCookie("login_token");
  const member = useMember();

  if (import.meta.server) {
    if (to.path !== "/") {
      if (!login_token.value) return navigateTo("/");

      const { code, result }: any = await $http(`/auth/me`);
      if (code === 0) {
        member.value = result;
      } else {
        return navigateTo("/");
      }
    }
  }

  if (
    import.meta.client &&
    to.path !== "/" &&
    (member.value.member_id === 0 || !login_token.value)
  ) {
    if (!login_token.value) return navigateTo("/");
  }

  if (to.path === "/") useCookie("login_token").value = null;
});
