<script setup>
const props = defineProps({
  is_active: { type: Boolean, required: true },
  item: {
    type: Object,
  },
});

const emit = defineEmits(["update:is_active", "close"]);

const form = ref({});

function onDialogChange(val) {
  emit("update:is_active", val);
}
const processedTexts = computed(() =>
  props.item?.content
    .replace(/.*(?=<div class="news_img_cont">)/s, "")
    .replaceAll("\n", "<br/><br/>")
);
</script>

<template>
  <ClientOnly>
    <v-dialog
      :model-value="is_active"
      scrollable
      width="900"
      @update:model-value="onDialogChange"
    >
      <v-card>
        <div class="dialog-top">
          <button
            class="icon--dialog-close"
            variant="text"
            @click="onDialogChange(false)"
          >
            <v-icon icon="mdi-close" size="large" />
          </button>
        </div>
        <div class="px-8 pt-8 pb-12">
          <p class="text-primary text-center mb-1 fw-500">
            {{ item.post_ctgry }}
          </p>
          <h4>{{ item.title }}</h4>
          <v-divider class="mb-8" />
          <div
            ref="draggable_text"
            class="news_content"
            v-html="processedTexts"
          ></div>
        </div>
      </v-card>
    </v-dialog>
  </ClientOnly>
</template>
<style scoped>
h4 {
  text-align: center;
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
}
</style>
