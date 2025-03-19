<script setup>
const props = defineProps({
  item: { required: true },
  favorite_type: { type: String },
  is_favorite: {
    type: Boolean,
    required: false,
  },
});
const emit = defineEmits(["search", "notify"]);

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    emit("notify", "복사되었습니다.");

    setTimeout(() => {
      copied.value = false;
    }, 2000);
  } catch (err) {
    console.log(err);
  }
};
function search(ingred_kor) {
  const query = `'${ingred_kor}' 성분에 대해`;
  emit("search", query);
}
</script>
<template>
  <div class="ingred_card">
    <v-card class="mx-auto" min-height="110">
      <v-card-text class="pt-2">
        <div class="flex align-end justify-between" style="height: 30px;">
          <div style="margin-bottom:7px;">
            <div v-if="item.cas_no" class="custom_chip">
              CAS No. {{ item.cas_no }}
            </div>
          </div>
          <div class="mt-1 mb-1 ">
            <v-icon
              icon="mdi-magnify"
              variant="text"
              color="primary"
              @click="search(item.ingred_kor)"
            />
            <v-icon
              class="ml-4"
              icon="mdi-content-copy"
              variant="text"
              color="primary"
              @click="
                copyToClipboard(item.original_file_url || item.source_url)
              "
            />
          </div>
        </div>

        <p class="ingred_card_title  pl-1 mb-2 ">
          {{ item.ingred_kor }}
          <span class="ingred_card_sub_title text-clamp-2">{{ item.ingred_eng }}</span>
        </p>

        <div class="text-medium-emphasis text-clamp-4  pl-1 mb-3">
          {{ item.definition }}
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>
<style scoped>
.ingred_card {
  position: relative;
  background: #ddd;
  margin-bottom: 14px;
}
.ingred_card_title {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.25;
  margin-bottom: 6px;
}
.ingred_card b {
  font-weight: 500;
}
.ingred_card_sub_title {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-gray-03);
  word-break: keep-all;
  white-space: nowrap;
}
.text-medium-emphasis {
  line-height: 1.3;
  font-size: 12px;
}
.custom_chip {
  color: var(--main-color);
  display: inline-block;
  background: #EEE9F5;
  padding: 0 10px;
  border-radius: 30px;
  line-height: 18px;
  height: 18px;
  font-size: 12px;
}
</style>
