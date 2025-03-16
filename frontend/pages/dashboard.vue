<script setup>
const member = useMember();
const items = [
  { type: "subheader", title: "아모레 뉴스" },
  {
    title: "아모레퍼시픽, CDP 평가에서 2개 부문 모두 최고 등급 획득",
    subtitle: `<span class="text-primary">to Alex, Scott, Jennifer</span>아모레퍼시픽은 이번 평가를 포함해 3년 연속 기후변화 대응 부문 A를 획득하며 기후변화에 대한 투명성 분야의 리더십을 인정받았다. 올해 처음으로 획득한 수자원 관리 부문에서도 수자원의 효율적인 사용과 관리, 순환 사용, 수질오염 방지 등에 대한 노력을 인정받아 최고 등급인 A를 받았다.`,
  },
  {
    title: "일리윤, 세라마이드 아토 라인 3세대 출시",
    subtitle:
      '<span class="text-primary">Trevor Hansen</span> CDP는 전 세계 금융투자기관이 주도하여 기업에게 환경 관련 경영정보공개를 요청하는 글로벌 이니셔티브다. 매년 기업들이 공개한 정보를 바탕으로 세계 최대 규모의 환경 데이터베이스를 보유하고 있으며, 전 세계 금융기관이 기업 투자와 대출 등의 의사결정에 의미 있는 정보로 활용할 수 있게 지원하여 저탄소 사회와 지속가능한 사회를 위한 기반을 만들어가고 있다. CDP는 기후 및 물 관련 리스크에 대한 대응, 도전적인 감축 목표, 리더십과 관리체계 등을 기반으로 기업을 평가하며 매년 전 세계 23,200개 이상의 기업이 응답하고 있다.',
  },
  {
    title: "설화수, 노스텔지어와 함께 한국 고가구 전시 진행",
    subtitle:
      '<span class="text-primary">Sandra Adams</span> &mdash;아모레퍼시픽은 자사 사업장 내에서 발생하는 온실가스 직접배출량(Scope1)과 전기 등을 구매하면서 발생하는 간접배출량(Scope2)의 총량을 2020년 대비 2050년까지 90% 감축하여 넷제로를 달성하려는 목표를 수립했다. 그 계획의 일환으로 아모레퍼시픽은 적극적인 전사 재생에너지 전환을 추진하고 있으며, 그 결과 2024년 기준 설화수, 라네즈, 해피바스를 비롯한 아모레퍼시픽의 주요 제품을 생산하는 오산, 대전, 안성, 상해 사업장 및 물류 사업장의 재생 전력 100%를 달성했다. 2025년은 아모레퍼시픽 전사 단위의 RE100 달성을 목표로 하고 있다.',
  },

  {
    title: "일리윤, 세라마이드 아토 라인 3세대 출시",
    subtitle:
      '<span class="text-primary">Trevor Hansen</span> CDP는 전 세계 금융투자기관이 주도하여 기업에게 환경 관련 경영정보공개를 요청하는 글로벌 이니셔티브다. 매년 기업들이 공개한 정보를 바탕으로 세계 최대 규모의 환경 데이터베이스를 보유하고 있으며, 전 세계 금융기관이 기업 투자와 대출 등의 의사결정에 의미 있는 정보로 활용할 수 있게 지원하여 저탄소 사회와 지속가능한 사회를 위한 기반을 만들어가고 있다. CDP는 기후 및 물 관련 리스크에 대한 대응, 도전적인 감축 목표, 리더십과 관리체계 등을 기반으로 기업을 평가하며 매년 전 세계 23,200개 이상의 기업이 응답하고 있다.',
  },
];
const items1 = [
  { type: "subheader", title: "외부자료/저널" },
  {
    title: "일리윤, 세라마이드 아토 라인 3세대 출시",
    subtitle:
      '<span class="text-primary">Trevor Hansen</span> CDP는 전 세계 금융투자기관이 주도하여 기업에게 환경 관련 경영정보공개를 요청하는 글로벌 이니셔티브다. 매년 기업들이 공개한 정보를 바탕으로 세계 최대 규모의 환경 데이터베이스를 보유하고 있으며, 전 세계 금융기관이 기업 투자와 대출 등의 의사결정에 의미 있는 정보로 활용할 수 있게 지원하여 저탄소 사회와 지속가능한 사회를 위한 기반을 만들어가고 있다. CDP는 기후 및 물 관련 리스크에 대한 대응, 도전적인 감축 목표, 리더십과 관리체계 등을 기반으로 기업을 평가하며 매년 전 세계 23,200개 이상의 기업이 응답하고 있다.',
  },
  {
    title: "아모레퍼시픽, CDP 평가에서 2개 부문 모두 최고 등급 획득",
    subtitle: `<span class="text-primary">to Alex, Scott, Jennifer</span>아모레퍼시픽은 이번 평가를 포함해 3년 연속 기후변화 대응 부문 A를 획득하며 기후변화에 대한 투명성 분야의 리더십을 인정받았다. 올해 처음으로 획득한 수자원 관리 부문에서도 수자원의 효율적인 사용과 관리, 순환 사용, 수질오염 방지 등에 대한 노력을 인정받아 최고 등급인 A를 받았다.`,
  },
  {
    title: "설화수, 노스텔지어와 함께 한국 고가구 전시 진행",
    subtitle:
      '<span class="text-primary">Sandra Adams</span> &mdash;아모레퍼시픽은 자사 사업장 내에서 발생하는 온실가스 직접배출량(Scope1)과 전기 등을 구매하면서 발생하는 간접배출량(Scope2)의 총량을 2020년 대비 2050년까지 90% 감축하여 넷제로를 달성하려는 목표를 수립했다. 그 계획의 일환으로 아모레퍼시픽은 적극적인 전사 재생에너지 전환을 추진하고 있으며, 그 결과 2024년 기준 설화수, 라네즈, 해피바스를 비롯한 아모레퍼시픽의 주요 제품을 생산하는 오산, 대전, 안성, 상해 사업장 및 물류 사업장의 재생 전력 100%를 달성했다. 2025년은 아모레퍼시픽 전사 단위의 RE100 달성을 목표로 하고 있다.',
  },
  {
    title: "일리윤, 세라마이드 아토 라인 3세대 출시",
    subtitle:
      '<span class="text-primary">Trevor Hansen</span> CDP는 전 세계 금융투자기관이 주도하여 기업에게 환경 관련 경영정보공개를 요청하는 글로벌 이니셔티브다. 매년 기업들이 공개한 정보를 바탕으로 세계 최대 규모의 환경 데이터베이스를 보유하고 있으며, 전 세계 금융기관이 기업 투자와 대출 등의 의사결정에 의미 있는 정보로 활용할 수 있게 지원하여 저탄소 사회와 지속가능한 사회를 위한 기반을 만들어가고 있다. CDP는 기후 및 물 관련 리스크에 대한 대응, 도전적인 감축 목표, 리더십과 관리체계 등을 기반으로 기업을 평가하며 매년 전 세계 23,200개 이상의 기업이 응답하고 있다.',
  },
];
const model = ref([]);
</script>

<template>
  <div id="AiSearch" class="content">
    <div class="content_inner">
      <h2 class="title--xl fw-700">
        안녕하세요,
        <span class="text-underline ml-1">
          {{ member.name }} {{ member.position }}님
        </span>
        <br />
        무엇을 도와드릴까요?
      </h2>
      <div class="input--search mt-5">
        <v-icon icon="mdi-magnify" />
        <input type="text" />
      </div>
      <v-divider class="mt-9" />
    </div>
    <article class="mt-7">
      <ClientOnly>
        <v-sheet class="group_card" style="">
          <v-slide-group v-model="model" class="pa-2" show-arrows>
            <v-slide-group-item v-for="n in 8" :key="n">
              <div class="group_card_item">
                <!-- <v-card :class="['ma-4']" height="250" width="340" @click="toggle"> -->
                <div class="d-flex fill-height align-center justify-center">
                  item
                </div>
                <!-- </v-card> -->
              </div>
            </v-slide-group-item>
          </v-slide-group>
        </v-sheet>
      </ClientOnly>
    </article>
    <div class="content_inner grid-cols-2">
      <article class="mt-2">
        <v-card class="mx-auto" elevation="0">
          <v-list :items="items" lines="two" item-props>
            <template v-slot:prepend>
              <v-avatar color="grey-lighten-1">
                <NuxtImg src="img/icon/story.svg" width="30" />
              </v-avatar>
            </template>
            <template v-slot:subtitle="{ subtitle }">
              <div v-html="subtitle" class="mr-2" />
            </template>
            <template v-slot:append>
              <v-btn
                class="icon--toggle"
                color="grey-lighten-2"
                icon="mdi-star"
                variant="text"
              />
            </template>
          </v-list>
        </v-card>
      </article>
      <article class="mt-2">
        <v-card class="mx-auto" elevation="0">
          <v-list :items="items1" lines="two" item-props>
            <template v-slot:subtitle="{ subtitle }">
              <div v-html="subtitle" class="mr-2" />
            </template>
            <template v-slot:append>
              <v-btn color="grey-lighten-2" icon="mdi-folder" variant="text" />
              <v-btn class="icon--toggle" icon="mdi-star" variant="text" />
            </template>
          </v-list>
        </v-card>
      </article>
    </div>
  </div>
</template>

<style scoped>
#AiSearch {
  margin-bottom: 2.5rem;
}
#AiSearch h2 {
  font-size: 30px;
  line-height: 43px;
  word-spacing: -4px;
  margin-top: 32px;
}
#AiSearch .grid-cols-2 {
  column-gap: 2rem;
}
.text-underline {
  font-weight: 800;
  text-underline-offset: 6px;
}
.input--search {
  display: flex;
  align-items: center;
  margin-top: 2px;
}
.input--search {
  border: 3px solid var(--color-black);
  border-radius: 60px;
  padding: 4px 10px;
  box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
}
.input--search input {
  width: 100%;
  outline: none;
}
.input--search i {
  font-size: 34px;
}
.group_card {
  margin: 0 auto;
  width: calc(100vw - 280px);
  min-width: 1040px;
  max-width: 1400px;
}
.group_card_item {
  height: 200px;
  min-width: 295px;
  width: calc((100vw - 360px) / 5);
  border-radius: var(--radius-3);
  /* border: 1px solid var(--border-color); */
  background: #e5e5e5;
  margin-right: 16px;
}
.group_card_item:last-of-type {
  margin-right: 0;
}
.group_card_item .card_img {
  border-radius: var(--radius-3);
}
</style>
