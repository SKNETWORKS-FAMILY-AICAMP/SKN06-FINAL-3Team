<script setup>
const lnb_items = [
  { name: "AI서치", path: "/ai-search", img_path: "img/icon/search.svg" },
  {
    name: "아모레스토리",
    path: "/amorestory",
    img_path: "img/icon/story.svg",
  },
  {
    name: "뉴스 / 저널",
    path: "/news-journal",
    img_path: "img/icon/news.svg",
  },
  { name: "화장품", path: "/products", img_path: "img/icon/cosmetics.png" },
  { name: "즐겨찾기", path: "/favorites", img_path: "img/icon/star.svg" },
];
const admin_items = [
  {
    name: "직원관리",
    path: "/admin/members",
    img_path: "img/icon/member.svg",
  },
];

const member = useMember();
const route = useRoute();

function active_menu(path) {
  return route.path.indexOf(path) > -1;
}

function logout() {
  navigateTo("");
}
</script>

<template>
  <nav id="lnb">
    <div class="lnb_top">
      <h1 class="buri">
        <NuxtLink to="/dashboard">
          <NuxtImg class="logo" src="img/logo_w.svg" />
        </NuxtLink>
      </h1>
      <NuxtLink class="lnb_myprofile" to="/mypage">
        <NuxtImg src="img/icon/account.png" width="44" />
        <div>
          <div class="text-gray-01 fw-500">
            <span>{{ member.department }}</span>
          </div>
          <p class="fw-800">
            {{ member.name }}
            <span class="fw-500"> {{ member.position }}</span>
          </p>
        </div>
      </NuxtLink>
      <div class="lnb_menu">
        <small class="text-gray-01">OVERVIEW</small>
        <ul class="lnb_list">
          <li
            v-for="item in lnb_items"
            :key="item.label"
            :class="{ active: active_menu(item.path) }"
          >
            <NuxtLink :to="item.path">
              <NuxtImg class="ml-1 mr-3" :src="item.img_path" width="20" />
              <span>{{ item.name }}</span>
            </NuxtLink>
          </li>
        </ul>
        <template v-if="member.role > 2 || member.department === 'HR'">
          <small class="text-gray-01">ADMIN</small>
          <ul class="lnb_list">
            <li
              v-for="item in admin_items"
              :key="item.label"
              :class="{ active: active_menu(item.path) }"
            >
              <NuxtLink :to="item.path">
                <NuxtImg class="ml-1 mr-3" :src="item.img_path" width="20" />
                <span>{{ item.name }}</span>
              </NuxtLink>
            </li>
          </ul>
        </template>
      </div>
    </div>
    <div class="lnb_bottom">
      <v-date-picker show-adjacent-months width="200" color="black" />
      <div>
        <button class="btn--logout" @click="logout">로그아웃</button>
      </div>
    </div>
  </nav>
</template>

<style scoped>
nav#lnb {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 10;
  height: 100vh;
  width: var(--lnb-width);
  min-width: var(--lnb-width);
  background: var(--lnb-bg-color);
  color: white;
  box-shadow: rgba(17, 17, 26, 0.05) 0px 1px 0px,
    rgba(17, 17, 26, 0.1) 0px 0px 8px;
}
nav#lnb h1 {
  font-size: 24px;
  padding: 32px 20px 0 20px;
}
.lnb_top h1 img {
  width: 152px;
}
.lnb_bottom {
  margin-top: 12px;
  padding-top: 24px;
  border-top: 1px solid #3f3f3f;
}
.lnb_bottom > div {
  display: flex;
  justify-content: flex-end;
  background: var(--lnb-bg-color);
}
.lnb_bottom .btn--logout {
  font-size: 13px;
  color: #868686;
  font-weight: 500;
  height: 36px;
  margin: 0 16px 8px;
}
.lnb_myprofile {
  display: flex;
  align-items: center;
  column-gap: 0.5rem;
  margin-top: 0.5rem;
  margin: 0.75rem 12px 1rem;
  text-decoration: none;
  color: white;
}
.lnb_myprofile div {
  line-height: 1.125rem;
}
.lnb_myprofile div p {
  display: flex;
  column-gap: 2px;
}
.lnb_myprofile div div {
  font-size: 0.75rem;
}
.lnb_menu small {
  display: block;
  font-size: 10px;
  margin-top: 12px;
  padding: 0 20px;
}
.lnb_list {
  padding: 0 8px;
  margin-top: 4px;
}
.lnb_list li {
  font-size: 15px;
  margin: 2px 0;
}
.lnb_list li img {
  width: 24px;
}
.lnb_list li a {
  display: flex;
  align-items: center;
  text-decoration: none;
  column-gap: 0.25rem;
  padding: 0 16px;
  color: white;
  line-height: 38px;
}
.lnb_list li a span {
  word-spacing: -1px;
}
.lnb_list li a i {
  margin-left: 2px !important;
}
.lnb_list li.active {
  /* background: #f5f5f5; */
  background: #3e3745;
  border-radius: 20px;
}
.lnb_list li.active a {
  font-weight: 600;
  /* color: var(--main-color); */
  color: white;
}
</style>
