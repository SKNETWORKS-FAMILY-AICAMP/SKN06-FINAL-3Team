<script setup>
const props = defineProps({
  item: { required: true },
  is_active: { type: Boolean, required: true },
});

const emit = defineEmits(["notify", "update:is_active"]);

function onDialogChange(val) {
  emit("update:is_active", val);
}
</script>

<template>
  <div class="no-scroll">
    <v-navigation-drawer
      class="rnb"
      :model-value="is_active"
      @update:model-value="onDialogChange"
      temporary
      location="right"
      width="500"
    >
      <template v-if="item">
        <div class="rnb_wrap">
          <div class="rnb_img card-img">
            <v-img height="250" :src="item.image_url" cover></v-img>
          </div>
          <div class="rnb_content">
            <div class="rnb_header ml-3 w-full flex align-center">
              <div class="chip_group">
                <v-chip
                  v-for="(tag, idx) in item.tags"
                  :key="idx"
                  size="x-small"
                >
                  {{ tag }}
                </v-chip>
                <v-chip size="x-small">{{ item.texture }}</v-chip>
              </div>
            </div>

            <v-card-item class="pt-1">
              <h3 class="card_title fw-600">
                {{ item.product_name }}
              </h3>
              <v-card-subtitle>
                <div class="flex px-3 gap-1"></div>
                <p class="flex gap-2 mt-1">
                  <button class="text-black fw-500 hover_underline">
                    {{ item.brand_kor }}
                  </button>
                  <small>|</small>
                  <span class="body--s">
                    {{ formatNumber(item.price) }}원
                  </span>
                  <small>|</small>

                  <span class="body--s">
                    {{ item.capacity }}
                  </span>
                </p>
              </v-card-subtitle>
            </v-card-item>
            <v-card-text>
              <div>
                <h4 class="mb-1 fw-600 flex align-center gap-1 word-space--1">
                  <v-icon
                    icon="mdi-information"
                    size="small"
                    color="grey-lighten-1"
                  />
                  ｢화장품법｣에 따라 기재ㆍ표시하여야 하는 모든 성분
                </h4>
                <p>
                  {{ item.ingredients }}
                </p>
              </div>

              <div>
                <h4
                  class="mt-5 mb-1 fw-600 flex align-center gap-1 word-space--1"
                >
                  <v-icon
                    icon="mdi-information"
                    size="small"
                    color="grey-lighten-1"
                  />
                  제품 주요 사양
                </h4>
                <p>{{ item.specification }}</p>
              </div>
              <div>
                <h4
                  class="mt-5 mb-1 fw-600 flex align-center gap-1 word-space--1"
                >
                  <v-icon
                    icon="mdi-information"
                    size="small"
                    color="grey-lighten-1"
                  />
                  사용방법
                </h4>
                <p>{{ item.use_period }}</p>
              </div>
              <div v-if="item.mfds">
                <h4
                  class="mt-5 mb-1 fw-600 flex align-center gap-1 word-space--1"
                >
                  <v-icon
                    icon="mdi-information"
                    size="small"
                    color="grey-lighten-1"
                  />
                  ｢화장품법｣에 따른 기능성 화장품 심사(보고) 여부
                </h4>
                <p>{{ item.mfds }}</p>
              </div>
              <div>
                <h4
                  class="mt-5 mb-1 fw-600 flex align-center gap-1 word-space--1"
                >
                  <v-icon
                    icon="mdi-information"
                    size="small"
                    color="grey-lighten-1"
                  />
                  사용할 때의 주의사항
                </h4>
                <p>{{ item.precaution }}</p>
              </div>
              <div v-if="item.manufacture">
                <h4
                  class="mt-5 mb-1 fw-600 flex align-center gap-1 word-space--1"
                >
                  <v-icon
                    icon="mdi-information"
                    size="small"
                    color="grey-lighten-1"
                  />
                  소비자상담 전화번호
                </h4>
                <p>{{ item.manufacture }}</p>
              </div>
            </v-card-text>
          </div>
        </div>
      </template>
    </v-navigation-drawer>
  </div>
</template>
