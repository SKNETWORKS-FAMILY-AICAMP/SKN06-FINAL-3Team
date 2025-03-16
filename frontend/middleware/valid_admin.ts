export default defineNuxtRouteMiddleware(async (to, from) => {
  const member = useMember();
  if (member.value.role < 2 || member.value.department !== "HR") {
    return navigateTo("/dashboard");
  }
});
