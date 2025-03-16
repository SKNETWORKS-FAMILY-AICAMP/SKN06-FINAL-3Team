<script setup>
useSeoMeta({
  title: "AmoreSearch",
  description: "AI AmoreSearch",
  keywords: "AmoreSearch",
  author: "AmoreSearch",
  publisher: "AmoreSearch",
  formatDetection: "telephone=no",
  ogType: "website",
  ogUrl: "http://15.165.170.3",
  ogTitle: "AmoreSearch",
  ogImage: "",
  ogDescription: "AmoreSearch",
  ogSiteName: "AmoreSearch",
  ogLocale: "ko_KR",
  ogKeyword: "AmoreSearch",
  ogAuthor: "AmoreSearch",
  ogRich_attachment: true,
});

useHead({
  lang: "ko",
  meta: [
    {
      name: "viewport",
      content:
        "viewport-fit=cover, width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no",
    },
  ],
  title: "AmoreSearch - 아모레서치",
  noscript: [{ children: "JavaScript is required" }],
  head: {
    link: [
      {
        rel: "stylesheet",
        href: "https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css",
      },
    ],
  },
});
</script>

<template>
  <v-app>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </v-app>
</template>
