<script setup>
const props = defineProps(["item", "scope", "is_favorite"]);
const emit = defineEmits(["success", "notify", "overview"]);

const is_favorite = ref(props.is_favorite || !isEmpty(props.item?.is_favorite));

async function toggleFavorites(item) {
  const body = {
    favorite_type: item.post_type,
    target_id: item.post_id,
    scope: props.scope,
  };

  let method = "";
  if (is_favorite.value) method = "DELETE";
  if (!is_favorite.value) method = "POST";

  try {
    const { code, msg } = await $http("/member/favorites", {
      method,
      body,
    });

    emit("notify", msg);
    emit("success");
    if (code == 0) is_favorite.value = !is_favorite.value;
  } catch (e) {
    emit("notify", "서버 오류 발생");
  }
}
function overview() {
  emit("overview", "internal_news", props.item);
}
</script>

<template>
  <v-card class="board_card">
    <div class="card-img cur-p" @click="overview">
      <v-img
        height="180px"
        :src="item.image_url"
        cover
        style="border-radius: 12px"
      ></v-img>
    </div>
    <v-card-text class="mt-4" style="min-height: 60px">
      <p class="mr-1 text-primary">{{ item.post_ctgry }}</p>
      <b class="fw-500 text-clamp-2">{{ item.title }}</b>
    </v-card-text>
    <div class="v-card-custom-action pr-1 pb-1">
      <span class="v-card-date">{{ formatDate(item.created_at) }}</span>
      <v-btn
        class="icon--toggle"
        :class="{ active: is_favorite }"
        icon="mdi-star"
        variant="text"
        @click="toggleFavorites(item)"
      />
    </div>
  </v-card>
</template>
