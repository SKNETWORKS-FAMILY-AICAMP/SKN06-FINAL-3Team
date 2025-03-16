<script setup>
const props = defineProps({ is_active: Boolean });
const emit = defineEmits(["update:modelValue", "close", "notify"]);

const closeDialog = (value) => {
  emit("close");
  initForm();
};
const initForm = () => {
  form.value.password = "";
  form.value.new_password = "";
  form.value.new_password_check = "";
};

function updateDialog() {
  emit("update:modelValue", value);
}
const form = ref({
  password: "",
  new_password: "",
  new_password_check: "",
});
const snackbar = ref({ active: false, message: "" });

const validatePassword = () => {
  snackbar.value.active = false;
  const { password, new_password, new_password_check } = form.value;

  if (password.length === 0)
    return emit("notify", "현재 비밀번호를 입력해 주세요.");
  if (new_password.length === 0)
    return emit("notify", "비밀번호를 입력해 주세요.");
  if (new_password_check.length === 0)
    return emit("notify", "비밀번호 확인을 입력해 주세요.");
  if (new_password !== new_password_check)
    return emit("notify", "비밀번호가 일치하지 않습니다.");

  return true;
};

async function updateMyPassword() {
  if (!validatePassword()) return;
  const { code, msg } = await $http("/member/password", {
    method: "PUT",
    body: {
      password: form.value.password,
      new_password: form.value.new_password,
    },
  });
  emit("notify", msg);
  if (code == 0) {
    closeDialog();
  }
}
</script>

<template>
  <v-dialog
    :model-value="is_active"
    @update:model-value="updateDialog"
    max-width="390"
    persistent
  >
    <v-card class="board_card">
      <v-toolbar align="center" color="black" class="px-7">
        비밀번호 변경
      </v-toolbar>
      <v-card-text class="mt-2">
        <form onsubmit="return false;">
          <div class="input_cont">
            <label> 현재 비밀번호 </label>
            <v-text-field
              hide-details
              variant="outlined"
              v-model="form.password"
              type="password"
              autocomplete="off"
            />
          </div>
          <div class="input_cont">
            <label> 비밀번호 </label>
            <v-text-field
              hide-details
              variant="outlined"
              v-model="form.new_password"
              type="password"
              autocomplete="off"
            />
          </div>
          <div class="input_cont">
            <label> 비밀번호 확인 </label>
            <v-text-field
              hide-details
              variant="outlined"
              v-model="form.new_password_check"
              type="password"
              autocomplete="off"
            />
          </div>
        </form>
      </v-card-text>
      <v-card-actions class="pt-4 pb-3 px-6 border-top-1">
        <div class="flex justify-center gap-2">
          <v-btn
            variant="flat"
            color="black"
            text
            width="80"
            @click="updateMyPassword"
          >
            변경
          </v-btn>
          <v-btn
            variant="outlined"
            color="gray-black"
            text
            width="80"
            @click="closeDialog"
          >
            취소
          </v-btn>
        </div>
      </v-card-actions>
      <v-snackbar v-model="snackbar.active" :timeout="3000" color="primary">
        {{ snackbar.message }}
      </v-snackbar>
    </v-card>
  </v-dialog>
</template>
