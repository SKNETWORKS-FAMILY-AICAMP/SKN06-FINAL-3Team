<script setup>
const member = useMember();
const dialogPwdChange = ref(false);
const dialogConfirm = ref({
  active: false,
  title: "",
  text: "",
});

const snackbar = ref({ active: false, message: "" });
const notify = (msg) => {
  snackbar.value.message = msg;
  snackbar.value.active = true;
};

const form = ref({
  phone: member.value.phone,
});

async function updateMyInfo() {
  dialogConfirm.value.active = false;

  if (!validatePhone(form.value.phone))
    return notify("휴대폰번호를 확인해 주세요.");

  const { code, msg, result } = await $http("/member/me", {
    method: "PUT",
    body: {
      member_id: member.value.member_id,
      phone: form.value.phone.replaceAll("-", ""),
    },
  });

  if (code == 1) return (snackbar.value.message = msg);
  snackbar.value.message = "수정되었습니다.";
  snackbar.value.active = true;

  await useLoginHandler().refresh(result);
}

const { data: mypage } = useApi("/member/me", {
  key: "mypage-board",
});
</script>

<template>
  <div id="Mypage" class="content">
    <div class="content_inner">
      <div class="page_header">
        <h2 class="page_title">마이페이지</h2>
      </div>
      <div id="myInfo" class="flex">
        <ClientOnly>
          <section class="info_detail" v-if="mypage?.result">
            <article>
              <h5>
                <v-icon
                  v-if="mypage?.role > 1"
                  icon="mdi-shield-account"
                  color="primary"
                  class="mr-1"
                />
                {{ mypage.result?.name }}
                <span class="fw-500 ml-2">{{ mypage.result?.position }}</span>
              </h5>

              <v-divider class="mt-2 mb-2" thickness="2" opacity=".8" />

              <b>
                <small style="font-size: 8px" class="mr-2">▶</small>
                직원 정보
              </b>

              <div class="grid-cols-2 ml-4 mb-3">
                <p>
                  <b class="mr-6">소속 / 근무부서</b>
                  {{ mypage.result?.company_affiliation }} /
                  {{ mypage.result?.department }}
                </p>
                <p>
                  <b class="mr-6">사원번호</b>
                  {{ mypage.result?.emp_no }}
                </p>
                <p>
                  <b class="mr-6">근무상태</b>
                  {{ mypage.result?.employment_status }}
                </p>
                <p>
                  <b class="mr-6">입사일</b>
                  {{ mypage.result?.hire_date }}
                </p>
              </div>
            </article>
            <v-divider class="mt-4 mb-3" />

            <article>
              <b>
                <small style="font-size: 8px" class="mr-2">▶</small>
                개인 정보
              </b>
              <div class="grid-cols-2 ml-4 mb-3">
                <p>
                  <b class="mr-6">생년월일</b>
                  <span>{{ mypage.result?.birth_date }}</span>
                </p>
                <div class="input_cont">
                  <b class="pr-7"> 휴대폰번호 </b>
                  <div class="flex gap-2">
                    <v-text-field
                      width="184"
                      hide-details
                      variant="outlined"
                      v-model="form.phone"
                      v-mask="'###-####-####'"
                    />
                    <v-btn
                      width="70"
                      color="black"
                      @click="
                        activate_confirm(
                          dialogConfirm,
                          '회원정보 수정',
                          '수정하시겠습니까?'
                        )
                      "
                    >
                      수정
                    </v-btn>
                  </div>
                </div>
              </div>
            </article>

            <article class="my-setting">
              <v-divider thickness="2" opacity=".8" />
              <div class="px-3">
                <p>
                  <v-icon icon="mdi-lock-outline " class="mr-2" /> 비밀번호 변경
                </p>
                <p>
                  <v-btn
                    @click="dialogPwdChange = true"
                    color="black"
                    width="160"
                    rounded
                  >
                    비밀번호 변경
                  </v-btn>
                </p>
              </div>
            </article>
          </section>
        </ClientOnly>
      </div>
    </div>

    <v-snackbar v-model="snackbar.active" :timeout="3000" color="primary">
      {{ snackbar.message }}
    </v-snackbar>

    <!-- DIALOG -->
    <DialogManagePassword
      v-model="dialogPwdChange"
      @notify="notify"
      @close="dialogPwdChange = false"
    />
    <DialogConfirm
      v-model="dialogConfirm.active"
      :title="dialogConfirm.title"
      :text="dialogConfirm.text"
      @submit="updateMyInfo"
      @close="dialogConfirm.active = false"
    />
  </div>
</template>

<style scoped>
.v-snackbar__wrapper {
  margin-left: 200px;
}

#myInfo {
  display: flex;
  justify-content: center;
  margin: 1.5rem auto 2.25rem;
  column-gap: 2.75rem;
}
#myInfo h3 {
  font-size: var(--body-size-l) !important;
  font-weight: 600;
  margin: 0 auto;
  color: var(--color-black);
}
#myInfo .info_summary {
  display: flex;
  flex-direction: column;
  width: 200px;
  font-size: var(--body-size-m) !important;
  margin-top: 14px;
}
#myInfo .info_summary p {
  display: flex;
  justify-content: space-between;
  padding: 0 12px;
  height: 28px;
}
#myInfo .info_summary p span:nth-of-type(1) {
  width: 76px;
  font-size: 0.8125rem;
  font-weight: 400;
  color: var(--color-gray-04);
  font-weight: 500;
}

#myInfo .info_detail {
  width: calc(100% - 200px);
}
#myInfo .info_detail .input_cont {
  display: flex;
  flex-direction: row;
  align-items: center;
  column-gap: 1.5rem;
  font-weight: 500;
}
#myInfo .info_detail .input_cont label {
  color: var(--color-gray-04);
  font-size: 0.8125rem;
  width: 64px;
  font-weight: 400;
}
#myInfo h4 {
  font-size: 16px;
  font-weight: 500;
  color: var(--main-color);
}
#myInfo h4 i {
  margin-bottom: 2px;
  font-weight: 500;
}
#myInfo h5 {
  font-size: 18px;
  display: flex;
  align-items: center;
  margin-top: 10px;
  margin-bottom: 8px;
  font-weight: 600;
}
article.my-setting {
  margin-top: 70px;
}
article.my-setting > div {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 76px;
}
article.my-setting p {
  font-weight: 500;
}
#myInfo .info_detail p,
#myInfo .info_detail b {
  display: flex;
  align-items: center;
  height: 35px;
  font-size: 0.875rem;
}
</style>
