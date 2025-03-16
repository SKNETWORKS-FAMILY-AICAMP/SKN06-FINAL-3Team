<script setup>
const member = useMember();
const resultMode = ref(false);
const pending = ref(false);
const search_input = ref("");

const filter = ref({
  query: "미백 기능을 가진 화장품을 소개해줘 ",
  tag: "",
});

const paging = ref({
  current_page: 1,
  item_per_page: 4,
});

const tags = ref(["검색태그 1", "검색태그 2", "검색태그 3", "검색태그 4"]);
const items = [
  {
    title: "일리윤, 세라마이드 아토 라인 3세대 출시",
    content:
      "Trevor Hansen CDP는 전 세계 금융투자기관이 주도하여 기업에게 환경 관련 경영정보공개를 요청하는 글로벌 이니셔티브다. 매년 기업들이 공개한 정보를 바탕으로 세계 최대 규모의 환경 데이터베이스를 보유하고 있으며, 전 세계 금융기관이 기업 투자와 대출 등의 의사결정에 의미 있는 정보로 활용할 수 있게 지원하여 저탄소 사회와 지속가능한 사회를 위한 기반을 만들어가고 있다. CDP는 기후 및 물 관련 리스크에 대한 대응, 도전적인 감축 목표, 리더십과 관리체계 등을 기반으로 기업을 평가하며 매년 전 세계 23,200개 이상의 기업이 응답하고 있다.",
    post_type: "NEWS",
    created_at: new Date(),
    source_name: "코스메틱리포트",
    source_url: "",
  },
  {
    title: "아모레퍼시픽, CDP 평가에서 2개 부문 모두 최고 등급 획득",
    content: `to Ale Jennifer 아모레퍼시픽은 이번 평가를 포함해 3년 연속 기후변화 대응 부문 A를 획득하며 기후변화에 대한 투명성 분야의 리더십을 인정받았다. 올해 처음으로 획득한 수자원 관리 부문에서도 수자원의 효율적인 사용과 관리, 순환 사용, 수질오염 방지 등에 대한 노력을 인정받아 최고 등급인 A를 받았다.`,
    post_type: "JOURNAL",
    created_at: new Date(),
    source_name: "코스메틱리포트",
    source_url: "",
  },
  {
    title: "설화수, 노스텔지어와 함께 한국 고가구 전시 진행",
    content:
      "Sandra Adams &mdash;아모레퍼시픽은 자사 사업장 내에서 발생하는 온실가스 직접배출량(Scope1)과 전기 등을 구매하면서 발생하는 간접배출량(Scope2)의 총량을 2020년 대비 2050년까지 90% 감축하여 넷제로를 달성하려는 목표를 수립했다. 그 계획의 일환으로 아모레퍼시픽은 적극적인 전사 재생에너지 전환을 추진하고 있으며, 그 결과 2024년 기준 설화수, 라네즈, 해피바스를 비롯한 아모레퍼시픽의 주요 제품을 생산하는 오산, 대전, 안성, 상해 사업장 및 물류 사업장의 재생 전력 100%를 달성했다. 2025년은 아모레퍼시픽 전사 단위의 RE100 달성을 목표로 하고 있다.",
    post_type: "REPORT",
    post_ctgry: "경영성과",
    created_at: new Date(),
    original_file_url: "/",
  },
  {
    title: "일리윤, 세라마이드 아토 라인 3세대 출시",
    content:
      "Trevor Hansen CDP는 전 세계 금융투자기관이 주도하여 기업에게 환경 관련 경영정보공개를 요청하는 글로벌 이니셔티브다. 매년 기업들이 공개한 정보를 바탕으로 세계 최대 규모의 환경 데이터베이스를 보유하고 있으며, 전 세계 금융기관이 기업 투자와 대출 등의 의사결정에 의미 있는 정보로 활용할 수 있게 지원하여 저탄소 사회와 지속가능한 사회를 위한 기반을 만들어가고 있다. CDP는 기후 및 물 관련 리스크에 대한 대응, 도전적인 감축 목표, 리더십과 관리체계 등을 기반으로 기업을 평가하며 매년 전 세계 23,200개 이상의 기업이 응답하고 있다.",
    post_type: "REPORT",
    post_ctgry: "사업보고서",
    created_at: new Date(),
    original_file_url: "/",
  },
  {
    title: "일리윤, 세라마이드 아토 라인 3세대 출시",
    content:
      "Trevor Hansen CDP는 전 세계 금융투자기관이 주도하여 기업에게 환경 관련 경영정보공개를 요청하는 글로벌 이니셔티브다. 매년 기업들이 공개한 정보를 바탕으로 세계 최대 규모의 환경 데이터베이스를 보유하고 있으며, 전 세계 금융기관이 기업 투자와 대출 등의 의사결정에 의미 있는 정보로 활용할 수 있게 지원하여 저탄소 사회와 지속가능한 사회를 위한 기반을 만들어가고 있다. CDP는 기후 및 물 관련 리스크에 대한 대응, 도전적인 감축 목표, 리더십과 관리체계 등을 기반으로 기업을 평가하며 매년 전 세계 23,200개 이상의 기업이 응답하고 있다.",
    post_type: "NEWS",
    created_at: new Date(),
    source_name: "코스메틱리포트",
    source_url: "",
  },
];

const paginatedItems = computed(() => {
  const startIndex =
    (paging.value.current_page - 1) * paging.value.item_per_page;
  const endIndex = startIndex + paging.value.item_per_page;
  return items.slice(startIndex, endIndex);
});

async function search(query) {
  if (query.length === 0) return;
  filter.value.query = query;
  resultMode.value = true;
  pending.value = true;

  setTimeout(() => {
    pending.value = false;
  }, 3000);

  // body = {
  // query: query,
  // tag:};
  // const result = $http("/ai", {
  //   key: "ai-search",
  //   body,
  // });
  // pending.value = false;
}

function changePage(page) {
  paging.value.current_page = page;
}

function initSearch() {
  resultMode.value = false;
  filter.value.query = "";
  paging.value.current_page = 1;
}
</script>

<template>
  <div id="AiSearch" class="content">
    <div class="content_inner">
      <ClientOnly>
        <template v-if="!resultMode">
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
                @search="search"
              />
            </div>
            <!-- <div class="flex justify-center mt-6">
              <v-chip-group
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
              </v-chip-group>
            </div> -->
          </div>
        </template>
        <template v-else>
          <div class="block_bg_box"></div>
          <div class="search_result">
            <div class="search_result_cont">
              <div class="search_result_left">
                <h3 class="flex align-start col-gap-2 my-5">
                  <v-icon icon="mdi-magnify" color="primary" size="30" />
                  <p>
                    {{ filter.query }}
                    <button v-if="!pending" @click="initSearch">
                      <v-icon
                        style="margin-bottom: 2px"
                        icon="mdi-close"
                        size="x-small"
                        color="primary"
                      />
                    </button>
                  </p>
                </h3>
                <template v-if="pending">
                  <div>
                    <v-progress-linear
                      style="width: 60%"
                      class="progress_linear_primary mb-3"
                      indeterminate
                      rounded
                      height="15"
                    />
                    <v-progress-linear
                      style="width: 50%"
                      class="progress_linear_primary mb-3"
                      indeterminate
                      rounded
                      height="15"
                    />
                    <v-progress-linear
                      style="width: 40%"
                      class="progress_linear_primary mb-3"
                      indeterminate
                      rounded
                      height="15"
                    />
                  </div>
                </template>
                <template v-else>
                  <div>출력결과</div>
                </template>
              </div>
              <div v-if="!pending" class="search_result_right">
                <p class="body--l mt-5 fw-600">
                  <!-- {{ items?.length || 0 }}개의 출처 -->
                  NEWS / JOURNAL
                </p>
                <ListItemReference
                  v-for="(item, index) in paginatedItems"
                  :key="index"
                  :item="item"
                />
                <!-- paging -->
                <Paging
                  :paging="paging"
                  :status="status"
                  :total_row="items.length"
                  :first-page="false"
                  :last-page="false"
                  @changePage="changePage"
                />
              </div>
            </div>

            <div class="search_input_cont">
              <label for="search_input">
                <v-icon icon="mdi-magnify" color="primary" />
              </label>
              <input
                id="search_input"
                type="text"
                v-model="search_input"
                @keydown.enter="search"
                placeholder=""
                :disabled="pending"
                style="outline: none"
              />
            </div>
          </div>
        </template>
      </ClientOnly>
    </div>
  </div>
</template>

<style scoped>
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
  margin-right: 1rem;
}
.search_result .search_result_right {
  width: 340px;
  margin-bottom: 3rem;
  display: flex;
  flex-direction: column;
  row-gap: 16px;
}
.search_input_cont {
  position: fixed;
  z-index: 2;
  bottom: 16px;
  left: 216px;
  width: calc(100% - 230px);
  box-shadow: rgba(0, 0, 0, 0.12) 0px 1px 3px, rgba(0, 0, 0, 0.24) 0px 1px 2px;
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
</style>
