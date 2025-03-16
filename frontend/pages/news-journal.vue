<script setup>
const tabs = ref([
  { text: "뉴스", value: "NEWS" },
  { text: "저널", value: "JOURNAL" },
]);
const snackbar = ref({ active: false, message: "" });
const post_type = ref({ text: "회사뉴스", value: "NEWS" });
const source_name = ref({
  name: "코스인코리아닷컴",
  value: "코스인코리아닷컴",
});
const query = ref("");
const filter = ref({
  post_type: "NEWS",
  source_name: "코스인코리아닷컴",
  query: "",
  current_page: 1,
  item_per_page: 10,
});

const filter_query = computed(() => ({
  post_type: filter.value.post_type,
  query: filter.value.query,
  source_name: filter.value.source_name,
  current_page: filter.value.current_page,
  item_per_page: filter.value.item_per_page,
}));

function changePage(current_page) {
  if (current_page === filter.value.current_page) {
    return;
  }
  filter.value.current_page = current_page;
  scrollToTop();
}

const { data: board, status } = useApi("/post/external", {
  key: "post-board",
  query: filter_query,
});
const total_cnt = computed(() => board.value.paging?.total_rows);

function notify(msg) {
  snackbar.value.active = true;
  snackbar.value.message = msg;
}
function change_query() {
  filter.value.query = query.value;
}
watch(post_type, (newValue) => {
  filter.value.post_type = newValue.value;
  source_name.value = externalCategory[newValue.value][0];
  filter.value.source_name = source_name.value.value;
  filter.value.current_page = 1;
  filter.value.query = "";
  query.value = "";
  change_query();
});
watch(source_name, (newValue) => {
  filter.value.source_name = newValue.value;
  filter.value.current_page = 1;
  filter.value.query = "";
  query.value = "";
});
</script>

<template>
  <div id="NewsJournal" class="content">
    <div class="content_inner">
      <ClientOnly>
        <div class="page_header">
          <h2 class="page_title">뉴스 / 저널</h2>
          <div class="board_tab depth-1">
            <v-tabs
              v-model="post_type"
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
          <div class="board_tab depth-2">
            <v-btn-toggle v-model="source_name" mandatory rounded="0">
              <v-btn
                v-for="(board, index) in externalCategory[post_type.value]"
                :key="index"
                :value="board"
                :ripple="false"
                height="40"
                min-width="72"
                selected-class="text-primary"
              >
                {{ board.name }}
              </v-btn>
            </v-btn-toggle>
          </div>
        </div>
        <div class="search_input_cont mb-5">
          <label for="search_input">
            <v-icon icon="mdi-magnify" color="primary" />
          </label>
          <input
            id="search_input"
            type="text"
            v-model="query"
            @keydown.enter="change_query"
            placeholder="제목 또는 내용을 입력해 주세요"
            :disabled="status === 'pending'"
            style="outline: none"
          />
        </div>
        <div
          v-if="status === 'success' && board?.result && total_cnt > 0"
          class="board"
        >
          <div class="board_list">
            <template v-if="filter.post_type == 'NEWS'">
              <ListItemNews
                v-for="item in board?.result"
                scope="EXTERNAL"
                :key="item.post_id"
                :item="item"
                @notify="notify"
              />
            </template>
            <template v-else-if="filter.post_type == 'JOURNAL'">
              <ListItemLink
                v-for="item in board?.result"
                scope="EXTERNAL"
                :key="item.post_id"
                :item="item"
                @notify="notify"
              />
            </template>
          </div>
          <Paging
            :paging="filter"
            :status="status"
            :total_row="total_cnt"
            @changePage="changePage"
          />
        </div>
        <div v-else class="no-result">
          <template v-if="status === 'pending'">
            <v-icon icon="mdi-magnify" color="grey-lighten-2" />
            <p class="text-gray-02">조회중입니다. 잠시만 기다려주세요</p>
          </template>

          <template v-else>
            <v-icon icon="mdi-magnify" color="grey-lighten-2" />
            <p class="text-gray-02">조회된 결과가 없습니다</p>
          </template>
        </div>
        <v-snackbar v-model="snackbar.active" :timeout="1000" color="primary">
          {{ snackbar.message }}
        </v-snackbar>
      </ClientOnly>
    </div>
  </div>
</template>

<style scoped>
.search_input_cont {
  min-width: 1100px;
  max-width: 1400px;
}
</style>
