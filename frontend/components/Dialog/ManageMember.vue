<script setup>
const member = useMember();
const props = defineProps({
  is_active: { type: Boolean, required: true },
  mode: { type: String, default: "register" },
  item: {
    type: Object,
  },
});

const emit = defineEmits(["update:is_active", "success", "close", "notify"]);
const modeText = computed(() => {
  if (props.mode === "register") return "등록";
  if (props.mode === "edit") return "수정";
});
const isDisabled = computed(() => props.item?.employment_status === "퇴직");

const form = ref({
  role: 1,
  emp_no: "",
  name: "",
  company_affiliation: "",
  department: "",
  position: "",
  birth_date: "",
  phone: "",
  hire_date: "",
  employment_status: "재직",
  resign_date: "",
  resign_reason: "",
  password: "",
});

const menu_birth = ref(false);
const menu_hire = ref(false);
const menu_resign = ref(false);
const datepicker_birth = ref(null);
const datepicker_hire = ref(null);
const datepicker_resign = ref(null);

async function submit() {
  if (!validateForm()) return;

  let response = null;

  if (props.mode === "register") {
    response = await addMember();
  } else {
    response = await updateMember();
  }
  if (response) {
    const { code, msg } = response;

    emit("notify", msg);
    if (code === 0) emit("success", props.mode);
    if (code === 0) emit("close");
  }
}

async function addMember() {
  const body = { ...form.value };
  if (body.phone.length) body.phone = body.phone.replaceAll("-", "");
  delete body.resign_date;
  delete body.resign_reason;

  try {
    const response = await $http("/admin/member", {
      method: "POST",
      body,
    });
    return response;
  } catch (e) {
    console.log(e);
  }
}

async function updateMember() {
  const body = { ...form.value };
  if (body.phone.length) body.phone = body.phone.replaceAll("-", "");
  delete body.emp_no;

  try {
    const response = await $http("/admin/member", {
      method: "PUT",
      body,
    });
    return response;
  } catch (e) {
    console.log(e);
    return false;
  }
}

function validateForm() {
  if (form.value.emp_no.length === 0)
    return emit("notify", "사원번호를 입력해주세요.");

  if (form.value.name.length === 0)
    return emit("notify", "이름을 입력해주세요.");

  if (props.mode === "register" && form.value.password.length === 0)
    return emit("notify", "비밀번호를 입력해주세요.");

  if (form.value.phone.length === 0)
    return emit("notify", "휴대폰번호를 입력해주세요.");

  if (form.value.birth_date.length === 0)
    return emit("notify", "생년월일를 입력해주세요.");

  if (form.value.hire_date.length === 0)
    return emit("notify", "입사일을 입력해주세요.");

  if (form.value.company_affiliation.length === 0)
    return emit("notify", "소속을 입력해주세요.");

  if (form.value.department.length === 0)
    return emit("notify", "근무부서를 입력해주세요.");

  if (form.value.position.length === 0)
    return emit("notify", "직급를 입력해주세요.");

  if (form.value.employment_status.length === 0)
    return emit("notify", "근무상태를 입력해주세요.");

  // 퇴직 validation
  if (form.value.employment_status === "퇴직") {
    if (isEmpty(form.value.resign_date))
      return emit("notify", "퇴직일을 입력해주세요.");
    if (isEmpty(form.value.resign_reason))
      return emit("notify", "퇴직사유를 입력해주세요.");
  } else {
    form.value.resign_date = null;
    form.value.resign_reason = null;
  }

  return true;
}
function initResignOptions() {
  if (form.value.employment_status !== "퇴직") {
    datepicker_resign.value = null;
    form.value.resign_date = null;
    form.value.resign_reason = null;
  } else {
    datepicker_resign.value = new Date();
    form.value.resign_date = formatDate(new Date());
  }
}

function set_form() {
  if (props.mode === "edit") {
    form.value.member_id = props.item?.member_id;
    form.value.role = props.item?.role;
    form.value.emp_no = props.item?.emp_no;
    form.value.name = props.item?.name;
    form.value.company_affiliation = props.item?.company_affiliation;
    form.value.department = props.item?.department;
    form.value.position = props.item?.position;
    form.value.birth_date = props.item?.birth_date;
    form.value.phone = props.item?.phone;
    form.value.hire_date = props.item?.hire_date;
    form.value.employment_status = props.item?.employment_status;
    form.value.resign_date = props.item?.resign_date;
    form.value.resign_reason = props.item?.resign_reason;
    form.value.password = "";

    datepicker_birth.value = new Date(form.value.birth_date);
    datepicker_hire.value = new Date(form.value.hire_date);

    if (form.value.resign_date) {
      datepicker_resign.value = new Date(form.value.resign_date);
    }
  } else {
    form.value.role = 1;
    form.value.emp_no = "";
    form.value.name = "";
    form.value.password = "";
    form.value.company_affiliation = "";
    form.value.department = "";
    form.value.position = "";
    form.value.birth_date = "";
    form.value.phone = "";
    form.value.hire_date = "";
    form.value.employment_status = "";
    form.value.resign_date = "";
    form.value.resign_reason = "";
  }
}

function onDialogChange(val) {
  emit("update:is_active", val);
}

watch(
  () => props.is_active,
  (newVal) => {
    if (newVal) set_form();
  }
);
watch(
  () => datepicker_birth.value,
  (newValue) => {
    form.value.birth_date = formatDate(newValue);
  }
);
watch(
  () => datepicker_hire.value,
  (newValue) => {
    form.value.hire_date = formatDate(newValue);
  }
);
watch(
  () => datepicker_resign.value,
  (newValue) => {
    form.value.resign_date = formatDate(newValue);
  }
);
</script>

<template>
  <ClientOnly>
    <v-dialog
      :model-value="is_active"
      scrollable
      max-width="560"
      @update:model-value="onDialogChange"
      persistent
    >
      <v-card>
        <v-toolbar align="center" color="black" class="px-7">
          직원 {{ modeText }}
        </v-toolbar>
        <v-card-text>
          <v-form class="pt-1">
            <div class="input_cont flex align-center" v-if="member?.role >= 2">
              <label class="mr-4 mb-0">권한</label>
              <v-chip-group
                v-model="form.role"
                mandatory
                selected-class="chip-selected"
                color="primary"
              >
                <template v-if="form.role === 3">
                  <span color="grey-lighten-2" :value="3"> 시스템관리자 </span>
                </template>
                <template v-else>
                  <v-chip
                    color="grey-lighten-2"
                    :value="2"
                    :disabled="isDisabled || form.role === 3"
                    >관리자</v-chip
                  >
                  <v-chip
                    color="grey-lighten-2"
                    :value="1"
                    :disabled="isDisabled || form.role === 3"
                    >일반</v-chip
                  >
                </template>
              </v-chip-group>
            </div>
            <div class="grid-cols-2">
              <div class="input_cont">
                <label>사원번호</label>
                <v-text-field
                  density="compact"
                  variant="outlined"
                  v-model="form.emp_no"
                  placeholder="사원번호 10자리를 입력해주세요"
                  :rules="[
                    (v) =>
                      v.length == 0 ||
                      v.length == 10 ||
                      '10자리를 입력해주세요',
                  ]"
                  oninput="javascript: this.value = this.value.replace(/[^0-9]/g, '');"
                  maxLength="10"
                  :disabled="mode === 'edit' || isDisabled"
                />
              </div>
              <div class="input_cont">
                <label>이름</label>
                <v-text-field
                  density="compact"
                  variant="outlined"
                  v-model="form.name"
                  placeholder="20자 이내로 입력해주세요"
                  :rules="[(v) => v.length <= 20 || '20자 이내로 입력해주세요']"
                  maxLength="20"
                  :disabled="isDisabled"
                />
              </div>
            </div>

            <div class="grid-cols-2">
              <div class="input_cont">
                <label>{{ mode === "edit" ? "초기화 " : "" }}비밀번호</label>
                <v-text-field
                  density="compact"
                  variant="outlined"
                  v-model="form.password"
                  type="password"
                  autocomplete="off"
                  placeholder="20자 이내로 입력해주세요"
                  :rules="[(v) => v.length <= 20 || '20자 이내로 입력해주세요']"
                  maxLength="20"
                  :disabled="isDisabled"
                />
              </div>
              <div class="input_cont">
                <label>휴대폰번호</label>
                <v-text-field
                  hide-details
                  density="compact"
                  variant="outlined"
                  v-model="form.phone"
                  v-mask="'###-####-####'"
                  :disabled="isDisabled"
                />
              </div>
            </div>
            <div class="grid-cols-2">
              <client-only>
                <div class="input_cont mb-3">
                  <label>생년월일</label>
                  <v-text-field
                    hide-details
                    density="compact"
                    variant="outlined"
                    v-model="form.birth_date"
                    v-mask="'####-##-##'"
                    prepend-inner-icon="mdi-calendar"
                    :disabled="isDisabled"
                    readonly
                  >
                    <v-menu
                      v-model="menu_birth"
                      :close-on-content-click="false"
                      activator="parent"
                      width="200"
                      :disabled="isDisabled"
                    >
                      <v-date-picker
                        hide-header
                        show-adjacent-months
                        v-model="datepicker_birth"
                      />
                    </v-menu>
                  </v-text-field>
                </div>
                <div class="input_cont mb-3">
                  <label>입사일</label>
                  <v-text-field
                    hide-details
                    density="compact"
                    variant="outlined"
                    v-model="form.hire_date"
                    v-mask="'####-##-##'"
                    prepend-inner-icon="mdi-calendar"
                    :disabled="isDisabled"
                    readonly
                  >
                    <v-menu
                      v-model="menu_hire"
                      :close-on-content-click="false"
                      activator="parent"
                      :disabled="isDisabled"
                    >
                      <v-date-picker
                        hide-header
                        show-adjacent-months
                        v-model="datepicker_hire"
                      />
                    </v-menu>
                  </v-text-field>
                </div>
              </client-only>
            </div>
            <div class="grid-cols-2">
              <div class="input_cont mb-3">
                <label>소속</label>
                <v-select
                  hide-details
                  variant="outlined"
                  v-model="form.company_affiliation"
                  :items="select_items.company_affiliation"
                  single-line
                  :disabled="isDisabled"
                />
              </div>
              <div class="input_cont mb-3">
                <label>근무부서</label>
                <v-select
                  hide-details
                  variant="outlined"
                  v-model="form.department"
                  :items="select_items.departments"
                  single-line
                  :disabled="isDisabled"
                />
              </div>
            </div>
            <div class="grid-cols-2">
              <div class="input_cont mb-3">
                <label>직급</label>
                <v-select
                  hide-details
                  variant="outlined"
                  v-model="form.position"
                  :items="select_items.positions"
                  single-line
                  :disabled="isDisabled"
                />
              </div>
              <div class="input_cont mb-3">
                <label>근무상태</label>
                <v-select
                  hide-details
                  variant="outlined"
                  v-model="form.employment_status"
                  :items="
                    mode === 'register'
                      ? select_items.employment_status
                      : select_items.all_employment_status
                  "
                  single-line
                  :disabled="isDisabled"
                  @change="initResignOptions"
                />
              </div>
            </div>
            <template v-if="form?.employment_status === '퇴직'">
              <v-divider class="mt-4 mb-4" />
              <div class="grid-cols-2">
                <client-only>
                  <div class="input_cont mb-3">
                    <label>퇴직일</label>
                    <v-text-field
                      hide-details
                      density="compact"
                      variant="outlined"
                      v-model="form.resign_date"
                      v-mask="'####-##-##'"
                      :rules="[
                        (v) =>
                          !v ||
                          /^\d{4}-\d{2}-\d{2}$/.test(v) ||
                          'YYYY-MM-DD 형식으로 입력해주세요',
                      ]"
                      prepend-inner-icon="mdi-calendar"
                      :disabled="isDisabled && member?.role < 2"
                      readonly
                    >
                      <v-menu
                        v-model="menu_resign"
                        :close-on-content-click="false"
                        activator="parent"
                        :disabled="isDisabled && member?.role < 2"
                      >
                        <v-date-picker
                          hide-header
                          show-adjacent-months
                          v-model="datepicker_resign"
                        />
                      </v-menu>
                    </v-text-field>
                  </div>
                </client-only>
              </div>

              <div class="input_cont">
                <label>퇴직사유</label>
                <v-textarea
                  row-height="25"
                  rows="5"
                  variant="outlined"
                  auto-grow
                  v-model="form.resign_reason"
                  :disabled="isDisabled && member?.role < 2"
                />
              </div>
            </template>
          </v-form>
        </v-card-text>

        <v-card-actions class="pt-4 pb-3 px-6 border-top-1">
          <v-btn variant="flat" color="black" text width="80" @click="submit">
            {{ modeText }}
          </v-btn>
          <v-btn
            variant="outlined"
            color="gray-black"
            text
            width="80"
            @click="onDialogChange(false)"
          >
            취소
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </ClientOnly>
</template>
