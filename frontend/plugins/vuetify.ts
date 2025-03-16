import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";

export default defineNuxtPlugin((app) => {
  const vuetify = createVuetify({
    components,
    icons: {
      defaultSet: "mdi",
    },
    theme: {
      themes: {
        light: {
          dark: false,
          colors: {
            primary: "#784aab",
            main: "#784AAB",
            sub: "#A28DD4",
            black: "#10021a",
            "border-color": "#aaaaaa",
            "on-border-color": "#aaaaaa",
            "on-background": "#10021a",
            "on-surface": "#10021a",
            "on-surface-bright": "#10021a",
            "on-surface-light": "#10021a",
          },
        },
      },
    },
  });
  app.vueApp.use(vuetify);
});
