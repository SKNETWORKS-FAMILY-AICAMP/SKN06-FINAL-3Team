<script setup>
const config = useRuntimeConfig().public;
const tabs = [
  { text: "회사뉴스", value: "NEWS" },
  { text: "IR 및 기타보고서", value: "REPORT" },
  { text: "브랜드", value: "BRAND" },
];
const dialog = ref({
  brand: false,
  internal_news: false,
});
const propsItem = ref(null);
const snackbar = ref({ active: false, message: "" });
const post_type = ref({ text: "회사뉴스", value: "NEWS" });
const post_ctgry = ref({ name: "전체", value: "" });
const filter = ref({
  post_type: "NEWS",
  post_ctgry: "",
  current_page: 1,
  item_per_page: 8,
});

const filter_query = computed(() => ({
  post_type: filter.value.post_type,
  post_ctgry: filter.value.post_ctgry,
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

const { data: board, status } = useApi("/post/internal", {
  key: "amorestory-board",
  query: filter_query,
});
const total_cnt = computed(() => board.value.paging.total_rows);

function notify(msg) {
  snackbar.value.active = true;
  snackbar.value.message = msg;
}

async function openDialog(type, item) {
  propsItem.value = item;
  dialog.value[type] = true;
}

watch(post_type, (newValue) => {
  filter.value.post_type = newValue.value;
  filter.value.post_ctgry = "";
  post_ctgry.value = { name: "전체", value: "" };
  filter.value.current_page = 1;
  if (newValue.value === "NEWS") filter.value.item_per_page = 8;
  else if (newValue.value === "REPORT") filter.value.item_per_page = 10;
  else if (newValue.value === "BRAND") filter.value.item_per_page = 100;
});

watch(post_ctgry, (newValue) => {
  filter.value.post_ctgry = newValue.value;
  filter.value.current_page = 1;
});
</script>

<template>
  <div id="AmoreStory" class="content">
    <div class="content_inner">
      <ClientOnly>
        <div class="page_header">
          <h2 class="page_title">아모레스토리</h2>
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
            <v-btn-toggle v-model="post_ctgry" mandatory rounded="0">
              <v-btn
                v-for="(board, index) in boardCategory[post_type.value]"
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
        <div class="board">
          <div
            class="board_content"
            v-if="status === 'success' && board?.result"
          >
            <!-- 회사뉴스 -->
            <template v-if="post_type.value === 'NEWS'">
              <div v-if="board?.result" class="board_cards grid-cols-4">
                <ListItemCardNews
                  v-for="(item, i) in board?.result"
                  :key="i"
                  :item="item"
                  scope="INTERNAL"
                  @notify="notify"
                  @overview="openDialog"
                />
              </div>
            </template>

            <!-- 보고서 -->
            <template v-else-if="post_type.value === 'REPORT'">
              <ListItemLink
                v-for="(item, index) in board?.result"
                :key="index"
                scope="INTERNAL"
                :item="item"
                @notify="notify"
              />
            </template>

            <!-- 브랜드 -->
            <template v-else-if="post_type.value === 'BRAND'">
              <div class="card--brand grid-cols-5">
                <v-card
                  v-for="(item, i) in board?.result"
                  :key="i"
                  @click="openDialog('brand', item)"
                >
                  <NuxtImg
                    :src="(config.CDN_HOST, item.image_url)"
                    class="align-end"
                    height="82"
                    cover
                  />
                  <div class="brand_info">
                    <v-chip
                      size="small"
                      color="sub"
                      variant="flat"
                      class="mr-1"
                      density="comfortable"
                    >
                      {{ enums.brand_ctgry[item.brand_ctgry] }}
                    </v-chip>
                    <p class="text-white">
                      {{ item.brand_kor }}
                    </p>
                  </div>
                </v-card>
              </div>
            </template>

            <!-- paging -->
            <Paging
              v-if="post_type.value === 'NEWS' || post_type.value === 'REPORT'"
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
        </div>

        <!-- dialog -->
        <DialogOverviewNews
          :is_active="dialog.internal_news"
          :item="propsItem"
          @update:is_active="dialog.internal_news = $event"
        />
        <DialogOverviewBrand
          :is_active="dialog.brand"
          :item="propsItem"
          @update:is_active="dialog.brand = $event"
        />
        <v-snackbar v-model="snackbar.active" :timeout="1000" color="primary">
          {{ snackbar.message }}
        </v-snackbar>
      </ClientOnly>
    </div>
  </div>
</template>

<style scoped>
.card--brand {
  margin: 1rem auto 2.125rem;
  row-gap: 1.25rem;
}
</style>
