<script setup>
const props = defineProps({
  dialog: { type: Boolean },
  title: { type: String, default: "" },
  text: { type: String, default: "" },
});
const emit = defineEmits(["submit", "close"]);

function agree() {
  emit("submit", "confirm");
}
function cancel() {
  emit("close", "confirm");
}
</script>

<template>
  <v-dialog v-model="$attrs" max-width="390" persistent>
    <v-card :title="title" :text="text">
      <template v-slot:actions>
        <v-spacer></v-spacer>

        <v-btn @click="agree"> 예 </v-btn>

        <v-btn @click="cancel"> 아니오 </v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>
