<script setup>
const { $api } = useNuxtApp();
definePageMeta({
  layout: false,
});

const snackbar = ref({ active: false, message: "" });
const form = ref({
  emp_no: "",
  password: "",
});

const visible = ref(false);

async function login() {
  if (form.value.emp_no.length === 0) {
    notify("사원번호를 입력해 주세요.");
    return;
  }
  if (form.value.password.length === 0) {
    notify("비밀번호를 입력해 주세요.");
    return;
  }

  try {
    const { code, msg, result } = await $http("/auth/login", {
      method: "POST",
      body: new URLSearchParams({
        username: form.value.emp_no,
        password: form.value.password,
      }),
    });

    code === 0 ? await loginSuccess(result.access_token) : notify(msg);
  } catch (error) {
    console.log(error);
  }
}

async function loginSuccess(access_token) {
  await useLoginHandler().refresh(access_token);
  await navigateTo("/ai-search");
}

function notify(msg) {
  snackbar.value.active = true;
  snackbar.value.message = msg;
}
</script>

<template>
  <div id="LoginPage">
    <div class="gradient-bg">
      <svg xmlns="http://www.w3.org/2000/svg">
        <defs>
          <filter id="goo">
            <feGaussianBlur
              in="SourceGraphic"
              stdDeviation="10"
              result="blur"
            />
            <feColorMatrix
              in="blur"
              mode="matrix"
              values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8"
              result="goo"
            />
            <feBlend in="SourceGraphic" in2="goo" />
          </filter>
        </defs>
      </svg>
      <div class="gradients-container">
        <div class="g1"></div>
        <div class="g2"></div>
        <div class="g3"></div>
        <div class="g4"></div>
        <div class="g5"></div>
        <div class="interactive"></div>
      </div>
    </div>
    <div class="login_left">
      <div>
        <h2 class="fw-700 dotum">환영합니다!</h2>
        <p class="title--l dotum fw-700">
          <span>AmoreSearch</span>
          와 함께하는 더 나은 내일
        </p>
        <p class="mt-3 mb-4 dotum">
          <span class="dotum">우리 회사의 업무를 지원하고,</span>
          <br />
          <span class="dotum"
            >화장품 산업에서 중요한 혁신을 이끌어가도록 돕겠습니다.</span
          >
        </p>
        <p class="body--l fw-600 mt-12">로그인하고 효율적인 업무 시작하세요!</p>
      </div>
    </div>
    <div class="login_right">
      <form class="login_form" onsubmit="return false;">
        <h1 class="text-center fw-600 mb-2">
          <NuxtImg class="logo" src="img/logo.svg" />
        </h1>
        <div class="input_wrap">
          <ClientOnly>
            <v-text-field
              density="compact"
              label="사원번호"
              placeholder="사원번호"
              variant="outlined"
              hide-details
              single-line
              v-model="form.emp_no"
              oninput="javascript: this.value = this.value.replace(/[^0-9]/g, '');"
              maxLength="10"
              autocomplete="off"
            />
            <v-text-field
              :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
              :type="visible ? 'text' : 'password'"
              prepend-inner-icon="mdi-lock-outline"
              placeholder="비밀번호"
              label="비밀번호"
              density="compact"
              variant="outlined"
              hide-details
              single-line
              v-model="form.password"
              autocomplete="off"
              @click:append-inner="visible = !visible"
              @keydown.enter="login"
            />
            <v-btn
              class="w-full mb-4"
              color="primary"
              @click="login"
              size="large"
              :ripple="false"
            >
              로그인
            </v-btn>
          </ClientOnly>
        </div>
      </form>
    </div>
    <v-snackbar v-model="snackbar.active" :timeout="3000" color="primary">
      {{ snackbar.message }}
    </v-snackbar>
  </div>
</template>

<style scoped>
#LoginPage {
  display: flex;
  height: 100vh;
}
#LoginPage h2 {
  font-size: 3.75rem;
  line-height: 5rem;
  opacity: 0;
  animation: fadeInDown 1.5s forwards;
}
.login_left > div p:nth-of-type(1) {
  font-size: 1.75rem;
  line-height: 34px;
  opacity: 0;
  animation: fadeInDown 1.5s forwards;
  animation-delay: 0.075s;
}
.login_left > div p:nth-of-type(2) {
  opacity: 0;
  animation: fadeInDown 1.5s forwards;
  animation-delay: 0.1s;
}
.login_left > div p:nth-of-type(3) {
  opacity: 0;
  animation: fadeInDown 1.5s forwards;
  animation-delay: 0.15s;
}
.login_left,
.login_right {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-width: 700px;
  z-index: 1;
}
.login_left {
  width: 52%;
  color: white;
}

.login_left > div {
  min-width: 460px;
}
.login_right {
  width: 48%;
  align-items: center;
}
.login_right h1 {
  margin-bottom: 0.5rem;
}
.login_right .logo {
  width: 200px;
}
.login_form {
  width: 280px;
}

/* 그라디언트 블롭 */
.gradient-bg {
  width: 52%;
  min-width: 700px;
  height: 100vh;
  position: absolute;
  overflow: hidden;
  background: linear-gradient(40deg, var(--color-bg1), var(--color-bg2));
  top: 0;
  left: 0;
}
.gradient-bg svg {
  position: fixed;
  top: 0;
  left: 0;
  width: 0;
  height: 0;
}
.gradient-bg .gradients-container {
  filter: url(#goo) blur(40px);
  width: 100%;
  height: 100%;
}
.gradient-bg .g1 {
  position: absolute;
  background: radial-gradient(
      circle at center,
      rgba(var(--color1), 0.8) 0,
      rgba(var(--color1), 0) 50%
    )
    no-repeat;
  mix-blend-mode: var(--blending);

  width: var(--circle-size);
  height: var(--circle-size);
  top: calc(50% - var(--circle-size) / 2);
  left: calc(50% - var(--circle-size) / 2);

  transform-origin: center center;
  animation: moveVertical 30s ease infinite;

  opacity: 1;
}
.gradient-bg .g2 {
  position: absolute;
  background: radial-gradient(
      circle at center,
      rgba(var(--color2), 0.8) 0,
      rgba(var(--color2), 0) 50%
    )
    no-repeat;
  mix-blend-mode: var(--blending);

  width: var(--circle-size);
  height: var(--circle-size);
  top: calc(50% - var(--circle-size) / 2);
  left: calc(50% - var(--circle-size) / 2);

  transform-origin: calc(50% - 400px);
  animation: moveInCircle 20s reverse infinite;

  opacity: 1;
}
.gradient-bg .g3 {
  position: absolute;
  background: radial-gradient(
      circle at center,
      rgba(var(--color3), 0.8) 0,
      rgba(var(--color3), 0) 50%
    )
    no-repeat;
  mix-blend-mode: var(--blending);

  width: var(--circle-size);
  height: var(--circle-size);
  top: calc(50% - var(--circle-size) / 2 + 200px);
  left: calc(50% - var(--circle-size) / 2 - 500px);

  transform-origin: calc(50% + 400px);
  animation: moveInCircle 40s linear infinite;

  opacity: 1;
}
.gradient-bg .g4 {
  position: absolute;
  background: radial-gradient(
      circle at center,
      rgba(var(--color4), 0.8) 0,
      rgba(var(--color4), 0) 50%
    )
    no-repeat;
  mix-blend-mode: var(--blending);

  width: var(--circle-size);
  height: var(--circle-size);
  top: calc(50% - var(--circle-size) / 2);
  left: calc(50% - var(--circle-size) / 2);

  transform-origin: calc(50% - 200px);
  animation: moveHorizontal 40s ease infinite;

  opacity: 0.7;
}
.gradient-bg .g5 {
  position: absolute;
  background: radial-gradient(
      circle at center,
      rgba(var(--color5), 0.8) 0,
      rgba(var(--color5), 0) 50%
    )
    no-repeat;
  mix-blend-mode: var(--blending);

  width: calc(var(--circle-size) * 2);
  height: calc(var(--circle-size) * 2);
  top: calc(50% - var(--circle-size));
  left: calc(50% - var(--circle-size));

  transform-origin: calc(50% - 800px) calc(50% + 200px);
  animation: moveInCircle 20s ease infinite;

  opacity: 1;
}
.gradient-bg .interactive {
  position: absolute;
  background: radial-gradient(
      circle at center,
      rgba(var(--color-interactive), 0.8) 0,
      rgba(var(--color-interactive), 0) 50%
    )
    no-repeat;
  mix-blend-mode: var(--blending);

  width: 100%;
  height: 100%;
  top: -50%;
  left: -50%;

  opacity: 0.7;
}
</style>
