<script setup>
const config = useRuntimeConfig().public;
const props = defineProps({
  is_active: { type: Boolean, required: true },
  item: {
    type: Object,
  },
});

const streaming = ref(false);
const requesting = ref(false);
const questions = computed(() => [
  `${[props.item?.brand_kor]}의 핵심 가치에 대해서 알려주세요.`,
  `${[props.item?.brand_kor]}의 주요 제품에 대해서 알려주세요`,
]);
const emit = defineEmits(["update:is_active", "close"]);

const search_input = ref("");
const search_query = ref("");
const search_result = ref("");
let controller = new AbortController();

async function search(query) {
  if (requesting.value) return;

  initSearch();
  search_query.value = query;
  requesting.value = true;
  streaming.value = true;
  controller = new AbortController();
  const response = await fetch(
    `http://localhost:8000/api/search/brand?brand_kor=${props.item?.brand_kor}&query=${search_query.value}`,
    {
      signal: controller.signal,
    }
  );

  if (!response.body) {
    console.error("스트리밍 응답을 받을 수 없습니다.");
    streaming.value = false;
    requesting.value = false;
    return;
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      streaming.value = false;
      requesting.value = false;
      break;
    }
    if (streaming.value) streaming.value = false;
    search_result.value += decoder.decode(value, { stream: true });
  }
}

function initSearch() {
  search_input.value = "";
  search_query.value = "";
  search_result.value = "";
  streaming.value = false;
  requesting.value = false;
}

function onDialogChange(val) {
  emit("update:is_active", val);
}

watch(
  () => props.is_active,
  (newValue) => {
    initSearch();
    if (!newValue) {
      controller.abort();
    }
  }
);

watch(
  () => props.brand_info,
  (newValue) => {
    brand_info.value = newValue;
  }
);
</script>

<template>
  <ClientOnly>
    <v-dialog
      :model-value="is_active"
      scrollable
      width="700"
      @update:model-value="onDialogChange"
    >
      <v-card>
        <v-card-text>
          <div class="dialog-top">
            <button
              class="icon--dialog-close"
              variant="text"
              @click="onDialogChange(false)"
            >
              <v-icon icon="mdi-close" size="large" />
            </button>
          </div>
          <div class="px-4">
            <p class="text-primary text-center mb-1 fw-500">
              <v-chip size="small">
                {{ enums.brand_ctgry[item.brand_ctgry] }}
              </v-chip>
            </p>

            <h4 class="flex align-center justify-center col-gap-3">
              <NuxtImg
                :src="(config.CDN_HOST, item.image_url)"
                class="align-end"
                height="50"
                width="50"
                cover
              />
              {{ item.brand_kor }}
            </h4>
            <p
              class="text-center text-gray-03 fw-300 body--m"
              style="line-height: 1.3"
              v-html="item.brand_subtitle"
            />
            <div class="flex justify-center align-center col-gap-4">
              <div class="flex mt-2">
                <span class="mr-5">
                  <b class="mr-2 text-primary fw-500">CEO</b> {{ item.ceo }}
                </span>
                <span>
                  <b class="mr-2 text-primary fw-500">설립연도</b>
                  {{ item.founded_year }}
                </span>
              </div>
            </div>
            <p class="mt-4">{{ item.brand_info }}</p>
            <div class="mb-8" />
            <!-- v-html="processedTexts" -->

            <div class="related_question_list">
              <h5>관련 질문</h5>
              <ol>
                <li v-for="(item, index) in questions" :key="index">
                  <span
                    @click="search(item)"
                    :class="{ 'text-underline': !requesting }"
                  >
                    {{ item }}
                  </span>
                </li>
              </ol>
            </div>

            <v-divider thickness="2" class="mb-4" />

            <div class="search_reply mb-6">
              <template v-if="search_query">
                <div class="search_q">{{ search_query }}</div>
                <div class="search_a" v-html="search_result"></div>
              </template>
              <template v-if="streaming">
                <div>
                  <v-progress-linear
                    style="width: 95%"
                    class="progress_linear_primary mb-2"
                    indeterminate
                    rounded
                    height="10"
                  />
                  <v-progress-linear
                    style="width: 85%"
                    class="progress_linear_primary"
                    indeterminate
                    rounded
                    height="10"
                  />
                </div>
              </template>
            </div>

            <div class="search_input_cont">
              <label for="search_input">
                <v-icon icon="mdi-magnify" color="primary" />
              </label>
              <input
                id="search_input"
                type="text"
                v-model="search_input"
                @keydown.enter="search(search_input)"
                placeholder=""
                :disabled="requesting"
                style="outline: none"
              />
            </div>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </ClientOnly>
</template>
<style scoped>
h4 {
  text-align: center;
  font-size: 1.5rem;
}
h5 {
  font-size: 14px;
  margin-top: 1rem;
  margin-bottom: 4px;
}
.search_reply {
  margin: 1rem 0;
}
.search_reply .search_q {
  color: var(--main-color);
  font-size: 15px;
  font-weight: 700;
  margin-bottom: 16px;
}
.search_reply .search_a {
  padding: 0 12px;
  font-size: 14px;
}
.related_question_list {
  margin-bottom: 1rem;
}
.related_question_list ol {
  list-style: disc;
  padding-left: 18px;
}
.related_question_list ol li {
  font-size: 14px;
  font-weight: 500;
  height: 22px;
  cursor: default !important;
}
.related_question_list ol li span {
  text-decoration: none !important;
  cursor: default !important;
}
.related_question_list ol li span.text-underline:hover {
  text-decoration: underline !important;
  cursor: pointer !important;
}
.related_question_list ol li:hover {
  cursor: pointer;
}
</style>
