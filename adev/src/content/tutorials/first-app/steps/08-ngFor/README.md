# Komponentda obyektlar roʻyxatini chiqarish uchun @for dan foydalanish

Bu dars shablonda dinamik takrorlanadigan maʼlumotlarni koʻrsatish uchun Angular shablonlarida `@for` blokidan qanday foydalanishni koʻrsatadi.

<docs-video src="https://www.youtube.com/embed/eM3zi_n7lNs?si=MIl5NcRxvcLjYt5f&amp;start=477"/>

NOTE: Bu video eskiroq sintaksisni aks ettiradi, lekin asosiy tushunchalar oʻz kuchini saqlab qoladi.

## Nimalarni oʻrganasiz {#what-youll-learn}

- Ilovaga maʼlumotlar toʻplamini qoʻshgan boʻlasiz
- Ilovangiz `@for` yordamida yangi maʼlumotlar toʻplamidagi elementlar roʻyxatini koʻrsatadi

## `@for` haqida konseptual koʻrinish {#conceptual-preview-of-for}

Angular'da `@for` — shablonda maʼlumotlarni dinamik takrorlash uchun ishlatiladigan [boshqaruv oqimi blokining](/guide/templates/control-flow) alohida turi. Oddiy JavaScript'da siz for siklidan foydalanar edingiz — `@for` Angular shablonlari uchun shunga oʻxshash imkoniyat beradi.

`@for`'dan massivlar va hatto asinxron qiymatlar boʻylab takrorlash (iteratsiya) uchun foydalanishingiz mumkin. Bu darsda siz takrorlash uchun yangi maʼlumotlar massivini qoʻshasiz.

Batafsilroq tushuntirish uchun [boshqaruv oqimi](guide/templates/control-flow#repeat-content-with-the-for-block) qoʻllanmasiga murojaat qiling.

<docs-workflow>

<docs-step title="`Home`'ga turar joy maʼlumotlarini qoʻshing">

`Home`'da faqat bitta turar joy mavjud. Bu qadamda siz `HousingLocation` yozuvlaridan iborat massiv qoʻshasiz.

1. `src/app/home/home.ts` faylida `Home` klassidan `housingLocation` xususiyatini olib tashlang.
1. `Home` klassiga `housingLocationList` nomli xususiyat qoʻshing. Kodingizni quyidagi kodga moslab yangilang:
   <docs-code language="angular-ts"  header="home.ts fayliga housingLocationList xususiyatini qoʻshish" path="adev/src/content/tutorials/first-app/steps/09-services/src/app/home/home.ts" visibleLines="[26,127]"/>

   IMPORTANT: `@Component` dekoratorini olib tashlamang, bu kodni keyingi qadamlardan birida yangilaysiz.

</docs-step>

<docs-step title="`Home` shablonini `@for` ishlatadigan qilib yangilang">
Endi ilovada `@for` bloki yordamida yozuvlarni brauzerda koʻrsatish uchun foydalanishingiz mumkin boʻlgan maʼlumotlar toʻplami bor.

1. Shablon kodidagi `<app-housing-location>` tegini quyidagicha yangilang:
   <docs-code language="angular-ts"  header="home.ts dagi Home shabloniga @for qoʻshish" path="adev/src/content/tutorials/first-app/steps/09-services/src/app/home/home.ts" visibleLines="[15,19]"/>

   Eʼtibor bering, `[housingLocation] = "housingLocation"` kodida `housingLocation` qiymati endi `@for` blokida ishlatiladigan oʻzgaruvchiga ishora qiladi. Bu oʻzgarishdan oldin u `Home` klassidagi xususiyatga ishora qilar edi.

1. Barcha oʻzgarishlarni saqlang.

1. Brauzerni yangilang va ilova endi turar joylar toʻrini (grid) render qilayotganini tasdiqlang.

<section class="lightbox">
<img alt="browser frame of homes-app displaying logo, filter text input box, search button and a grid of housing location cards" src="assets/images/tutorials/first-app/homes-app-lesson-08-step-2.png">
</section>

</docs-step>

</docs-workflow>

SUMMARY: Bu darsda siz Angular shablonlarida maʼlumotlarni dinamik takrorlash uchun `@for` blokidan foydalandingiz. Shuningdek, Angular ilovasida ishlatish uchun yangi maʼlumotlar massivini qoʻshdingiz. Endi ilova brauzerda turar joylar roʻyxatini dinamik render qiladi.

Ilova shakllanib bormoqda, ajoyib ish.

Bu darsda yoritilgan mavzular haqida koʻproq maʼlumot olish uchun quyidagilarga qarang:

<docs-pill-row>
  <docs-pill href="guide/templates/control-flow" title="Boshqaruv oqimi bloklari"/>
  <docs-pill href="guide/templates/control-flow#repeat-content-with-the-for-block" title="@for qoʻllanmasi"/>
  <docs-pill href="/api/core/@for" title="@for"/>
</docs-pill-row>
