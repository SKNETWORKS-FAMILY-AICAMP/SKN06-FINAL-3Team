<script setup>
const props = defineProps({
  paging: { type: Object, required: true },
  status: { type: String, default: "" },
  total_row: { required: true, default: 0 },
  disabled: { type: Boolean, default: false },
  boardType: { type: String, default: "" },
  noContentText: { type: String, default: "" },
  noContentIcon: { type: String, default: "" },
  firstPage: { type: Boolean, default: true },
  lastPage: { type: Boolean, default: true },
});

const emit = defineEmits(["changePage"]);
const page_per_group = 10;

const paging = ref({
  current_page: props.paging.current_page,
  item_per_page: props.paging.item_per_page,
  total_row: Number(props.total_row),
  lastPage: 1,
  groupStartPage: 1,
  groupEndPage: 1,
  pageList: [1],
});
set_paging_data();

watch(
  () => props.paging.current_page,
  (newValue) => {
    paging.value.current_page = newValue;
    set_paging_data();
  }
);

watch(
  () => props.total_row,
  (newValue) => {
    paging.value.total_row = newValue;
    set_paging_data();
  }
);

function groupEndPage() {
  const groupEndPageVal =
    Math.ceil(paging.value.current_page / page_per_group) * page_per_group;
  return groupEndPageVal < paging.value.lastPage
    ? groupEndPageVal
    : paging.value.lastPage;
}

function groupStartPage() {
  return (
    Math.floor((paging.value.current_page - 1) / page_per_group) *
      page_per_group +
    1
  );
}

function set_paging_data() {
  paging.value.pageList = [];
  paging.value.lastPage =
    paging.value.total_row == 0
      ? 1
      : Math.ceil(Number(paging.value.total_row) / paging.value.item_per_page);
  paging.value.groupStartPage = groupStartPage();
  paging.value.groupEndPage = groupEndPage();

  if (paging.value.groupEndPage > 0) {
    for (
      let i = paging.value.groupStartPage;
      i <= paging.value.groupEndPage;
      i++
    ) {
      paging.value.pageList.push(i);
    }
  }
}

const changePage = (page) => {
  if (props.disabled) {
    return;
  }
  let _page = page;
  if (page <= 0) _page = 1;
  if (page >= paging.value.lastPage) _page = paging.value.lastPage;

  emit("changePage", _page);
};
</script>
<template>
  <div v-if="total_row > 0" class="paging">
    <!-- list 조회중 / 결과없음 -->
    <button
      v-if="firstPage"
      @click="changePage(1)"
      :class="{
        hide:
          paging?.current_page === 1 || paging?.current_page <= page_per_group,
      }"
    >
      <v-icon icon="mdi-page-first" />
    </button>
    <button
      @click="changePage(paging?.groupStartPage - page_per_group)"
      :class="{
        hide:
          paging?.current_page === 1 || paging?.groupStartPage < page_per_group,
      }"
    >
      <v-icon icon="mdi-chevron-left" />
    </button>
    <div class="paging_num">
      <button
        v-for="item in paging?.pageList"
        :key="item"
        :class="{ active: paging?.current_page === item }"
        @click="changePage(item)"
      >
        {{ item }}
      </button>
    </div>
    <button
      :class="{
        hide:
          paging?.current_page === paging?.lastPage ||
          paging?.groupStartPage + 9 >= paging?.lastPage,
      }"
      @click="changePage(paging?.groupEndPage + 1)"
    >
      <v-icon icon="mdi-chevron-right" />
    </button>
    <button
      v-if="lastPage"
      :class="{
        hide:
          paging?.lastPage <= paging?.groupStartPage + page_per_group ||
          paging?.groupEndPage - paging?.groupStartPage + 1 < page_per_group,
      }"
      @click="changePage(paging?.lastPage)"
    >
      <v-icon icon="mdi-page-last" />
    </button>
  </div>
</template>
<style scoped>
.paging {
  display: flex;
  justify-content: center;
  align-items: center;
  column-gap: 0.5rem;
  margin-top: 3rem;
  margin-bottom: 3rem;
}
.paging_num {
  display: flex;
  align-items: center;
  column-gap: 0.5rem;
}
.paging_num button {
  padding: 4px;
}
.paging_num button.active {
  font-weight: 600;
  color: var(--main-color);
  padding: 4px;
}
.paging .hide {
  opacity: 0;
  pointer-events: none;
}
</style>
