import vuetify, { transformAssetUrls } from "vite-plugin-vuetify";

export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  css: [
    "~/assets/css/font.css",
    "~/assets/css/common.css",
    "~/assets/css/main.css",
  ],
  build: {
    transpile: ["vuetify"],
  },
  plugins: ["~/plugins/vue-the-mask.js"],
  modules: [
    (_options, nuxt) => {
      nuxt.hooks.hook("vite:extendConfig", (config) => {
        // @ts-expect-error
        config.plugins.push(vuetify({ autoImport: true }));
      });
    },
    "@nuxt/image",
  ],
  vite: {
    vue: {
      template: {
        transformAssetUrls,
      },
    },
    server: {
      proxy: {
        "/api": {
          target: process.env.SERVER_HOST,
          changeOrigin: true,
        },
      },
    },
  },
  runtimeConfig: {
    public: {
      SERVER_HOST: process.env.SERVER_HOST,
      CDN_HOST: process.env.CDN_HOST,
    },
  },
});
