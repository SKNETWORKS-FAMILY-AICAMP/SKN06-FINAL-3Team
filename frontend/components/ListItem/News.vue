<script setup>
const props = defineProps(["item", "scope", "is_favorite"]);
const emit = defineEmits(["success", "notify"]);

const is_favorite = ref(props.is_favorite || !isEmpty(props.item?.is_favorite));

function openLink(url) {
  window.open(url);
}
function downloadFnc(item) {
  window.open(item.original_file_url);
}

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
</script>

<template>
  <ClientOnly>
    <div external class="list-item">
      <div class="list-left">
        <!-- @click="openLink(item.source_url)" class="cur-p"x -->
        <div>
          <v-img
            width="180px"
            height="110px"
            :src="item.thumbnail_image_url"
            cover
          ></v-img>
        </div>
        <div class="flex-column justify-center">
          <p class="list-title">{{ item.title }}</p>
          <p class="list-text text-clamp-4">{{ item.content }}</p>
          <p>
            <span class="text-gray-04 mr-2">
              {{ formatDate(item.created_at) }}
            </span>
            <span class="text-gray-04" v-if="item.source_name">
              {{ item.source_name }}
            </span>
          </p>
        </div>
      </div>

      <div>
        <template v-if="item?.original_file_url">
          <v-btn
            color="sub"
            icon="mdi-folder"
            variant="text"
            @click="downloadFnc(item)"
          />
        </template>
        <template v-else>
          <v-btn
            color="sub"
            icon="mdi-link"
            variant="text"
            @click="openLink(item.source_url)"
          />
        </template>

        <v-btn
          class="icon--toggle"
          :class="{ active: is_favorite }"
          icon="mdi-star"
          variant="text"
          @click="toggleFavorites(item)"
        />
      </div>
    </div>
  </ClientOnly>
</template>

<style scoped>
.list-item {
  padding: 10px 16px;
  text-decoration: none;
}
.list-item {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
}
.list-item .list-title {
  font-weight: 500;
  line-height: 1.5rem;
  font-size: 0.9375rem;
  margin-bottom: 2px;
}
.list-left {
  display: flex;
  column-gap: 20px;
  width: calc(100% - 120px);
}
.list-item p {
  font-size: 0.8125rem;
  line-height: 1rem;
}
.list-item p.list-text {
  margin-bottom: 4px;
  font-size: 0.8125rem;
  /* min-height: 50px; */
}
.list-item:first-child {
  border-top: 1px solid var(--border-color) !important;
}
</style>
