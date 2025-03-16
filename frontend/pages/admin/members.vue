<script setup>
definePageMeta({
  middleware: ["auth"],
});

const member = useMember();
const tabs = ref([
  { text: "재직직원", value: "" },
  { text: "퇴직직원", value: "퇴직" },
]);
const snackbar = ref({ active: false, message: "" });
const employment_status = ref({ text: "재직직원", value: "" });
const propItem = ref(null);
const dialog = ref(false);
const dialogMode = ref(null);

const filter = ref({
  employment_status: "",
  query: "",
  current_page: 1,
  item_per_page: 20,
});

const filter_query = computed(() => ({
  employment_status: filter.value.employment_status,
  current_page: filter.value.current_page,
  item_per_page: filter.value.item_per_page,
}));

const {
  data: board,
  status,
  refresh,
} = useApi("/admin/members", {
  key: "member-list",
  query: filter_query,
});

const total_cnt = computed(() => board.value?.paging.total_rows);

function changePage(current_page) {
  if (current_page === filter.value.current_page) {
    return;
  }
  filter.value.current_page = current_page;
  scrollToTop();
}

function notify(msg) {
  snackbar.value.active = true;
  snackbar.value.message = msg;
}
function openDialog(mode, item) {
  dialogMode.value = mode;
  propItem.value = item;
  dialog.value = true;
}

function closeDialog() {
  dialogMode.value = null;
  dialog.value = false;
  propItem.value = null;
}

async function successDialog(mode) {
  if (mode === "register") {
    filter.value.current_page = 1;
  } else {
  }
  refresh();
  closeDialog();
}
watch(employment_status, (newValue) => {
  filter.value.employment_status = newValue.value;
  changePage(1);
});
</script>

<template>
  <div id="Members" class="content">
    <ClientOnly>
      <div class="content_inner">
        <div class="page_header">
          <h2 class="page_title">직원관리</h2>
          <div class="board_tab depth-1">
            <v-tabs
              v-model="employment_status"
              bg-color="transparent"
              align-tabs="center"
              density="comfortable"
              selected-class="text-primary"
            >
              <v-tab
                v-for="tab in tabs"
                :key="tab.value"
                :text="tab.text"
                :value="tab"
                :ripple="false"
              />
            </v-tabs>
          </div>
        </div>
        <div class="board">
          <div class="board_util">
            <div class="board_desc">
              <span class="body--m text-gray-03">total: {{ total_cnt }}</span>
            </div>
            <small v-if="employment_status.value === '퇴직'" class="ml-2">
              퇴직직원의 정보는 관리자만 수정 가능합니다.
            </small>
            <v-btn
              v-if="employment_status.value === ''"
              density="comfortable"
              icon="mdi-plus"
              color="black"
              @click="openDialog('register')"
            />
          </div>

          <div class="board_list" v-if="status === 'success'">
            <v-table>
              <thead>
                <tr>
                  <th class="text-center" style="width: 78px">번호</th>
                  <th>이름</th>
                  <th>사번</th>
                  <th>소속</th>
                  <th>부서</th>
                  <th>직급</th>
                  <th style="width: 120px">생년월일</th>
                  <th style="width: 140px">휴대폰번호</th>
                  <th style="width: 120px">입사일</th>
                  <th style="width: 90px">근무상태</th>
                  <th class="text-center" style="width: 70px">수정</th>
                </tr>
              </thead>
              <tbody v-if="board?.result && total_cnt > 0">
                <tr v-for="(item, index) in board?.result" :key="item.name">
                  <td class="text-center">{{ total_cnt - index }}</td>
                  <td>
                    <v-icon
                      v-if="item.role == 2"
                      icon="mdi-shield-account"
                      color="primary"
                    />
                    {{ item.name }}
                  </td>
                  <td>{{ item.emp_no }}</td>
                  <td>{{ item.company_affiliation }}</td>
                  <td>{{ item.department }}</td>
                  <td>{{ item.position }}</td>
                  <td>{{ item.birth_date }}</td>
                  <td>{{ formatPhone(item.phone) }}</td>
                  <td>{{ item.hire_date }}</td>
                  <td>{{ item.employment_status }}</td>
                  <td class="text-center">
                    <v-btn
                      :id="`member-${index}`"
                      icon="mdi-account-edit"
                      color="grey-lighten-2"
                      class="icon--toggle"
                      :class="
                        employment_status === '' || member.role >= 2
                          ? 'active'
                          : ''
                      "
                      @click.stop="openDialog('edit', item)"
                      variant="text"
                    />
                  </td>
                </tr>
              </tbody>
            </v-table>
            <div v-if="total_cnt == 0" class="no-result">
              <v-icon icon="mdi-magnify" color="grey-lighten-2" />
              <p class="text-gray-02">조회된 결과가 없습니다</p>
            </div>
            <Paging
              :paging="filter"
              :status="status"
              :total_row="total_cnt"
              @changePage="changePage"
            />
          </div>
        </div>
      </div>
      <DialogManageMember
        :mode="dialogMode"
        :is_active="dialog"
        :item="propItem"
        @update:is_active="dialog = $event"
        @notify="notify"
        @close="closeDialog"
        @success="successDialog"
      />

      <v-snackbar v-model="snackbar.active" :timeout="3000" color="primary">
        {{ snackbar.message }}
      </v-snackbar>
    </ClientOnly>
  </div>
</template>

<style scoped></style>
