<script setup>
const tabs = ref([
  { text: "자사제품", value: "INTERNAL" },
  { text: "타사제품", value: "EXTERNAL" },
]);
const snackbar = ref({ active: false, message: "" });
const scope = ref({ text: "자사제품", value: "INTERNAL" });
const selected_brand_id = ref(null);
const category_1 = ref({ name: "전체", value: "" });
const dialog = ref(false);
const targetItem = ref(null);

const filter = ref({
  scope: "INTERNAL",
  category_1: "",
  brand_ids: selected_brand_id.value,
  current_page: 1,
  item_per_page: 12,
});

const filter_query = computed(() => ({
  scope: filter.value.scope,
  category_1: filter.value.category_1,
  brand_ids: filter.value.brand_ids,
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

const { data: brands } = useApi("/amorepacific/brands", {
  key: "cosmetic-brands",
});

const {
  data: board,
  status,
  refresh,
} = useApi("/product/products", {
  key: "product-board",
  query: filter_query,
});

function notify(msg) {
  snackbar.value.active = true;
  snackbar.value.message = msg;
}

function openRnb(item) {
  dialog.value = true;
  targetItem.value = item;
}

watch(scope, (newValue) => {
  filter.value.scope = newValue.value;
  if (newValue.value == "INTERNAL") {
    filter.value.category_1 = "";
    selected_brand_id.value = null;
  }
  if (newValue.value == "EXTERNAL") {
    filter.value.brand_ids = null;
    category_1.value = { name: "전체", value: "" };
  }
  filter.value.current_page = 1;
});

watch(selected_brand_id, (newValue) => {
  filter.value.brand_ids = newValue;
  filter.value.current_page = 1;
});

watch(category_1, (newValue) => {
  filter.value.category_1 = newValue.value;
  filter.value.current_page = 1;
});

const total_cnt = computed(() => board.value.paging?.total_rows || 0);
</script>

<template>
  <div id="Products" class="content">
    <div class="content_inner">
      <ClientOnly>
        <div class="page_header">
          <h2 class="page_title">화장품</h2>
          <div class="board_tab depth-1">
            <v-tabs
              v-model="scope"
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
        <div v-if="filter.scope === 'INTERNAL'" class="mt-4 mb-6">
          <v-sheet class="mx-auto">
            <v-slide-group
              v-if="brands"
              show-arrows
              v-model="selected_brand_id"
              selected-class="active"
            >
              <v-slide-group-item
                v-for="(brand, i) in brands?.result"
                :key="i"
                :value="brand?.brand_id"
                v-slot="{ toggle, selectedClass }"
              >
                <v-card variant="flat" height="72">
                  <button
                    :class="[selectedClass]"
                    class="list_avatar"
                    @click="toggle"
                  >
                    <v-img width="64" :src="brand.image_url" />
                    <small class="text-white fw-500">
                      {{ brand.brand_kor }}
                    </small>
                  </button>
                  <div
                    class="d-flex fill-height align-center justify-center"
                  ></div>
                </v-card>
              </v-slide-group-item>
            </v-slide-group>
          </v-sheet>
        </div>
        <div v-if="filter.scope === 'EXTERNAL'" class="board_tab depth-2">
          <v-btn-toggle v-model="category_1" mandatory rounded="0">
            <v-btn
              v-for="(board, index) in externalCategory.COSMETIC"
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
        <div
          class="board"
          v-if="status === 'success' && board?.result && total_cnt > 0"
        >
          <div class="board_list">
            <div class="board_cards product_card grid-cols-4">
              <ListItemProduct
                v-for="item in board?.result"
                :key="item?.cosmetic_id"
                :item="item"
                :scope="filter.scope"
                :is_favorite="false"
                @notify="notify"
                @showDetail="openRnb"
              />
              <RnbProduct
                :is_active="dialog"
                :item="targetItem"
                @update:is_active="dialog = $event"
              />
            </div>

            <Paging
              :paging="filter"
              :status="status"
              :total_row="total_cnt"
              @changePage="changePage"
            />
          </div>
        </div>
        <div v-else class="no-result">
          <template v-if="status === 'pending'">
            <v-icon icon="mdi-magnify" color="grey-lighten-2" />
            <p class="text-gray-02">조회중입니다. 잠시만 기다려주세요</p>
          </template>

          <template v-else-if="total_cnt == 0">
            <v-icon :icon="' mdi-magnify'" color="grey-lighten-2" />
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
.rnb_header {
  height: 38px;
  margin-left: 0.75rem;
  width: 100%;
  display: flex;
  align-items: center;
}
.chip_group {
  width: 100%;
  display: flex;
  align-items: center;
  grid-template: 4rem;
  margin-top: 10px;
}
.list_avatar {
  margin: 0 6px;
}
</style>
