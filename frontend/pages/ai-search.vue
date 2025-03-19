<script setup>
const member = useMember();
const config = useRuntimeConfig().public;

let controller = new AbortController();

// 요청 상태 관련
const searchMode = ref(false);
const waiting = ref(false);
const streaming = ref(false);

// 검색 관련
const tags = ref(["화장품", "성분", "뉴스/저널/문서"]);
const filter = ref({ query: " ", tag: "" });
const inputValue = ref("");
const resultTab = ref(1);
const paging = ref({ current_page: 1, item_per_page: 4 });

const llm_response = ref("");
const question_response = ref([]);

const metadata_response = ref(null);
const ingredient_response = ref([]);
const post_response = ref([]);
const cosmetic_response = ref([]);

const snackbar = ref({ active: false, message: "" });
const dialog = ref(false);
const targetItem = ref(null);

const isResultReady = computed(
  () => !waiting.value && llm_response.value.length > 0
);

const paginatedPosts = computed(() => {
  if (post_response.length === 0) return [];

  const startIndex =
    (paging.value.current_page - 1) * paging.value.item_per_page;
  const endIndex = startIndex + paging.value.item_per_page;
  return post_response.value.slice(startIndex, endIndex);
});

function notify(msg) {
  snackbar.value.active = true;
  snackbar.value.message = msg;
}

async function searchFnc(query) {
  if (query.length === 0) return;
  if (streaming.value || waiting.value) return;

  initResponse();

  searchMode.value = true;
  waiting.value = true;

  filter.value.query = query;

  controller = new AbortController();

  try {
    const response = await fetch(
      `${config.SERVER_HOST}/api/search/ai?query=${query}`,
      {
        signal: controller.signal,
      }
    );

    if (!response.body) {
      console.error("스트리밍 응답을 받을 수 없습니다.");
      waiting.value = false;
      streaming.value = false;
      return;
    }
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        waiting.value = false;
        streaming.value = false;
        break;
      }
      if (waiting.value) waiting.value = false;

      const text = decoder.decode(value, { stream: true });
      const lines = text.split("\n").filter((line) => line.trim() !== "");

      for (const line of lines) {
        try {
          const json = JSON.parse(line);

          if (json.type === "metadata") {
            metadata_response.value = json.data;
            setResponses(metadata_response.value);
          } else if (json.type === "message") {
            llm_response.value += json.data;
          }
        } catch (err) {
          console.error("JSON 파싱 오류:", err);
        }
      }
    }
  } catch (error) {
    console.error("스트리밍 중 오류 발생:", error);
  }
}

function setResponses(data) {
  const { ingredient, cosmetic, post } = data;
  ingredient_response.value = ingredient;

  if (Object.keys(cosmetic).length > 0) {
    cosmetic_response.value = flattenAndAddScope(cosmetic);
  }
  if (Object.keys(post).length > 0) {
    post_response.value = flattenAndAddScope(post);
  }
  if (post_response.value.length > 0) resultTab.value = 1;
  else if (ingredient_response.value.length > 0) resultTab.value = 2;
  else resultTab.value = 0;
}

function openRnb(item) {
  dialog.value = true;
  targetItem.value = item;
}

function flattenAndAddScope(data) {
  const scopeMapping = {
    자사: "INTERNAL",
    INTERNAL: "INTERNAL",
    타사: "EXTERNAL",
    EXTERNAL: "EXTERNAL",
  };

  return Object.entries(data).reduce((acc, [key, items]) => {
    if (scopeMapping[key]) {
      acc.push(...items.map((item) => ({ ...item, scope: scopeMapping[key] })));
    }
    return acc;
  }, []);
}

function changePage(page) {
  paging.value.current_page = page;
}

function changeTab(tab) {
  if (waiting.value) return;
  resultTab.value = tab;
}
function initPage() {
  searchMode.value = false;
  initResponse();
}

function initResponse() {
  llm_response.value = "";
  question_response.value = [];
  ingredient_response.value = [];
  cosmetic_response.value = [];
  post_response.value = [];
  // posts.value = [];

  paging.value.current_page = 1;
  resultTab.value = 1;

  inputValue.value = "";
  filter.value.query = "";
}

// async function toggleFavorites(item) {
//   const body = {
//     favorite_type: item.post_type,
//     target_id: item.post_id
//     scope: props.scope,
//   };

//   let method = "";
//   if (is_favorite.value) method = "DELETE";
//   if (!is_favorite.value) method = "POST";

//   try {
//     const { code, msg } = await $http("/member/favorites", {
//       method,
//       body,
//     });

//     emit("notify", msg);
//     emit("success");
//     if (code == 0) is_favorite.value = !is_favorite.value;
//   } catch (e) {
//     emit("notify", "서버 오류 발생");
//   }
// }

onUnmounted(() => {
  controller.abort();
});
</script>

<template>
  <div id="AiSearch" class="content">
    <div class="content_inner">
      <!-- <div>{{ cosmetic_response }}</div> -->
      <!-- <div>{{ question_response }}</div> -->
      <ClientOnly>
        <template v-if="!searchMode">
          <div class="content_center">
            <h2 class="fw-700 gradient-text mb-6">
              안녕하세요,
              <span class="ml-1">
                {{ member.name }} {{ member.position }}님
              </span>
              <br />
              무엇을 도와드릴까요?
            </h2>

            <div>
              <SearchInput
                :texts="[
                  '최근에 출시한 우리회사 제품들을 소개해줘',
                  '선크림에 주요한 성분들에 대해서 알려줘',
                ]"
                @search="searchFnc"
              />
            </div>
            <div class="flex justify-center mt-6">
              <!-- <v-chip-group
                v-model="filter.tag"
                selected-class="text-primary"
                mandatory
              >
                <v-chip
                  filter
                  v-for="tag in tags"
                  :key="tag"
                  :text="tag"
                  :value="tag"
                  style="font-size: 15px; font-weight: 500; padding: 20px 22px"
                />
              </v-chip-group> -->
            </div>
          </div>
        </template>
        <template v-else>
          <div class="search_result">
            <div class="search_result_cont">
              <div class="search_result_left">
                <!-- 검색 쿼리 -->
                <h3 class="flex align-start col-gap-2 my-5">
                  <v-icon icon="mdi-magnify" color="primary" size="30" />
                  <p class="search_query">
                    {{ filter.query }}
                    <button v-if="!waiting" @click="initPage">
                      <v-icon
                        style="margin-bottom: 2px"
                        icon="mdi-close"
                        size="x-small"
                        color="primary"
                      />
                    </button>
                  </p>
                </h3>

                <!-- 왼쪽 -->
                <v-skeleton-loader
                  v-if="!isResultReady"
                  type="list-item-three-line"
                />
                <template v-else>
                  <div class="llm_cont">
                    <MDC :value="llm_response" tag="article" />
                  </div>

                  <div
                    v-if="!isEmpty(question_response) && !streaming"
                    class="question_cont"
                  >
                    <div
                      v-for="(question, index) in question_response"
                      :key="index"
                      class="question_item"
                      @click="searchFnc(question)"
                    >
                      <div class="flex">
                        <span>{{ index + 1 }}</span>
                        <p>{{ question }}</p>
                      </div>
                      <div>
                        <v-icon
                          color="main"
                          icon="mdi-arrow-right"
                          class="mr-6"
                        ></v-icon>
                      </div>
                    </div>
                  </div>
                </template>
                <div
                  v-if="!streaming && cosmetic_response.length > 0"
                  class="cosmetic_cont mt-4"
                >
                  <h4 class="body--l mb-2">참조 화장품</h4>
                  <div class="board_cards product_card grid-cols-4">
                    <ListItemProductDensed
                      v-for="item in cosmetic_response"
                      :key="item?.cosmetic_id"
                      :item="item"
                      :scope="item.scope"
                      :is_favorite="false"
                      @showDetail="openRnb"
                    />
                  </div>
                </div>
              </div>

              <!-- 오른쪽 -->
              <div class="search_result_right">
                <p class="mt-5 fw-600">
                  <template v-if="resultTab != 0">
                    <button
                      class="btn--text"
                      :disabled="
                        waiting || streaming || post_response?.length === 0
                      "
                      :class="{ active: resultTab == 1 }"
                      @click="changeTab(1)"
                    >
                      참조 문서
                    </button>
                    <button
                      class="btn--text"
                      :disabled="
                        waiting ||
                        streaming ||
                        ingredient_response?.length === 0
                      "
                      :class="{ active: resultTab == 2 }"
                      @click="changeTab(2)"
                    >
                      용어 사전
                    </button>
                  </template>
                </p>

                <div class="tab_content">
                  <!-- Tab 1:: 참조문서 item  -->
                  <template v-if="resultTab === 1">
                    <template v-if="!isResultReady">
                      <v-skeleton-loader
                        class="mx-auto border"
                        max-width="340"
                        type="chip, actions, article, chip, chip,"
                      />
                      <v-skeleton-loader
                        class="mx-auto border"
                        max-width="340"
                        type="chip, actions,article, chip, chip,"
                      />
                    </template>
                    <template v-else>
                      <ListItemPosts
                        v-for="item in paginatedPosts"
                        :key="item.post_id"
                        :item="item"
                        @notify="notify"
                      />
                      <Paging
                        :paging="paging"
                        :total_row="post_response.length"
                        :first-page="false"
                        :last-page="false"
                        @changePage="changePage"
                      />
                    </template>
                  </template>

                  <!-- Tab 2:: 용어사전 -->
                  <template v-else-if="resultTab === 2">
                    <ListItemIngredient
                      v-for="item in ingredient_response"
                      :key="item.ingred_id"
                      :item="item"
                      @notify="notify"
                      @search="searchFnc"
                    />
                  </template>
                </div>
              </div>
            </div>

            <div></div>

            <!-- input gradient bg-->
            <div class="block_bg_box" />
            <!-- 하단 검색 Input -->
            <div
              class="search_input_cont"
              :class="{ opacity_5: waiting || streaming }"
            >
              <label for="search_input">
                <v-icon icon="mdi-magnify" color="primary" />
              </label>
              <input
                id="search_input"
                type="text"
                v-model="inputValue"
                @keydown.enter="searchFnc(inputValue)"
                :disabled="waiting || streaming"
                style="outline: none"
              />
            </div>
          </div>
          <v-snackbar v-model="snackbar.active" :timeout="2000" color="primary">
            {{ snackbar.message }}
          </v-snackbar>
        </template>
      </ClientOnly>
    </div>
    <RnbProduct
      :is_active="dialog"
      :item="targetItem"
      @update:is_active="dialog = $event"
    />
  </div>
</template>

<style scoped>
.opacity_5 {
  opacity: 0.5;
}
.content_inner {
  position: relative;
  padding-right: 12px;
  padding-left: 28px;
  margin-bottom: 28px;
}
#AiSearch h2 {
  display: inline-block;
  font-size: 38px;
  text-align: center;
  line-height: 48px;
  word-spacing: -4px;
  font-weight: 800;
  margin: 0 auto;
  animation: fadeInDown2 0.8s;
}
#AiSearch .grid-cols-2 {
  column-gap: 2rem;
}
#AiSearch .paging {
  margin-top: 1rem;
  margin-bottom: 0.25rem;
}
#AiSearch.content {
  max-width: 100%;
}

.content_center {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0 80px 130px;
}

.group_card {
  margin: 0 auto;
  width: calc(100vw - 280px);
  min-width: 1040px;
  max-width: 1400px;
}
.group_card_item {
  height: 200px;
  min-width: 295px;
  width: calc((100vw - 360px) / 5);
  border-radius: var(--radius-3);
  background: #e5e5e5;
  margin-right: 16px;
}
.group_card_item:last-of-type {
  margin-right: 0;
}
.group_card_item .card_img {
  border-radius: var(--radius-3);
}

.search_result {
  display: flex;
  flex-direction: column;
}
.search_result > .search_result_cont {
  display: flex;
  min-height: calc(100vh - 100px);
}
.search_result h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.2;
}
.search_result .search_result_left {
  flex: 1;
  margin-bottom: 3rem;
  margin-right: 1.5rem;
}
.search_result .search_result_right {
  width: 340px;
  margin-bottom: 3rem;
  display: flex;
  flex-direction: column;
  row-gap: 10px;
}
.search_input_cont {
  position: fixed;
  z-index: 2;
  bottom: 16px;
  left: 216px;
  width: calc(100% - 230px);
  box-shadow: rgba(0, 0, 0, 0.12) 0px 1px 3px, rgba(0, 0, 0, 0.24) 0px 1px 2px;
}
.search_query {
  font-weight: 700;
  word-spacing: -1px;
}
.block_bg_box {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 84px;
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 1) 35%
  );
  z-index: 1;
}

button.btn--text {
  font-size: 1rem;
  margin-right: 1.45rem;
  transition: all 0.2s ease;
  word-spacing: -3px;
  color: var(--color-gray-03);
  font-weight: 500;
}
button.btn--text:hover {
  color: var(--main-color);
}
button.btn--text.active {
  color: var(--color-black);
  font-weight: 500;
}
button.btn--text:disabled {
  color: var(--color-gray-01) !important;
}
.llm_cont {
  min-height: 100px;
  font-size: 14px;
  line-height: 1.5;
}

.question_cont {
  margin-top: 3rem;
}
.question_item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 45px;
  border-bottom: 1px solid var(--border-color);
  font-size: 14px;
  cursor: pointer;
  user-select: none;
  background: #fff;
  transition: all 0.1s ease;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}
.question_item:nth-child(1) {
  border-top: 1px solid var(--border-color);
}
.question_item > div {
  display: flex;
  align-items: center;
}
.question_item span {
  margin-left: 8px;
  margin-right: 2px;
  font-weight: 700;
  color: var(--main-color);
  padding: 0 12px;
  font-size: 15px;
}
.question_item p {
  font-size: 13px;
}
.question_item i,
.question_item span {
  transition: all 0.15s ease;
}

.question_item:hover span {
  margin-left: 16px !important;
}
.question_item:hover i {
  margin-right: 16px !important;
}
</style>
