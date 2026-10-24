# Ilovangizga qidiruv imkoniyatini qoʻshish

Bu dars Angular ilovangizga qidiruv funksiyasini qanday qoʻshishni koʻrsatadi.

Ilova foydalanuvchilarga ilovangiz taqdim etgan maʼlumotlar boʻylab qidirish va faqat kiritilgan soʻzga mos natijalarni koʻrsatish imkonini beradi.

<docs-video src="https://www.youtube.com/embed/5K10oYJ5Y-E?si=TiuNKx_teR9baO7k&amp;start=457"/>

IMPORTANT: Darslikning bu qadami uchun lokal muhitingizdan foydalanishni tavsiya qilamiz.

## Nimalarni oʻrganasiz {#what-youll-learn}

- Ilovangiz mos turar joylarni qidirish uchun formadagi maʼlumotlardan foydalanadi
- Ilovangiz faqat mos turar joylarni koʻrsatadi

<docs-workflow>

<docs-step title="Home komponenti xususiyatlarini yangilang">
Bu qadamda siz `Home` klassini filtrlash uchun ishlatadigan yangi massiv xususiyatida maʼlumotlarni saqlaydigan qilib yangilaysiz.

1. `src/app/home/home.ts` faylida klassga `filteredLocationList` nomli yangi xususiyat qoʻshing.

   <docs-code header="home.ts fayliga filteredLocationList xususiyatini qoʻshish" path="adev/src/content/tutorials/first-app/steps/14-http/src/app/home/home.ts" visibleLines="[28]"/>

   `filteredLocationList` foydalanuvchi kiritgan qidiruv shartiga mos qiymatlarni saqlaydi.

1. Sahifa yuklanganda `filteredLocationList` sukut boʻyicha turar joylar qiymatlarining toʻliq toʻplamini oʻz ichiga olishi kerak. Qiymatni oʻrnatish uchun `Home`'ning `constructor`'ini yangilang.

   <docs-code header="filteredLocationList qiymatini oʻrnatish" path="adev/src/content/tutorials/first-app/steps/14-http/src/app/home/home.ts" visibleLines="[29,32]"/>

</docs-step>

<docs-step title="Home komponenti shablonini yangilang">
`Home` allaqachon foydalanuvchi kiritgan maʼlumotni olish uchun ishlatadigan input maydonini oʻz ichiga oladi. Bu satr matni natijalarni filtrlash uchun ishlatiladi.

1. `Home` shablonini `input` elementida `#filter` nomli shablon oʻzgaruvchisini oʻz ichiga oladigan qilib yangilang.

   <docs-code language="angular-ts" header="home.ts dagi input HTML elementiga shablon oʻzgaruvchisi qoʻshish" path="adev/src/content/tutorials/first-app/steps/14-http/src/app/home/home.ts" visibleLines="[12]"/>
   Bu misol `input` elementiga uning qiymati sifatida kirish uchun [shablon havola oʻzgaruvchisidan (template reference variable)](guide/templates) foydalanadi.

1. Keyin komponent shablonini "Search" tugmasiga hodisa ishlov beruvchisini biriktiradigan qilib yangilang.

   <docs-code language="angular-ts" header="home.ts da tugmaning click hodisasini metodga bogʻlash" path="adev/src/content/tutorials/first-app/steps/14-http/src/app/home/home.ts" visibleLines="[13]"/>

   `button` elementidagi `click` hodisasiga bogʻlanish orqali siz `filterResults` funksiyasini chaqira olasiz. Funksiya argumenti — `filter` shablon oʻzgaruvchisining `value` xususiyati. Aniqrogʻi, `input` HTML elementining `.value` xususiyati.

1. Soʻnggi shablon yangilanishi `@for` direktivasiga tegishli. `@for`'ni `filteredLocationList` massividagi qiymatlar boʻylab takrorlanadigan qilib yangilang.

   <docs-code language="angular-ts" header="home.ts dagi @for shablon direktivasini yangilash" path="adev/src/content/tutorials/first-app/steps/14-http/src/app/home/home.ts" visibleLines="[17,19]"/>

</docs-step>

<docs-step title="Hodisa ishlov beruvchi funksiyasini amalga oshiring">
Shablon `filterResults` funksiyasini `click` hodisasiga bogʻlaydigan qilib yangilandi. Keyingi vazifangiz — `Home` klassida `filterResults` funksiyasini amalga oshirish.

1.  `Home` klassini `filterResults` funksiyasining implementatsiyasini oʻz ichiga oladigan qilib yangilang.

    <docs-code header="filterResults funksiyasi implementatsiyasini qoʻshish" path="adev/src/content/tutorials/first-app/steps/14-http/src/app/home/home.ts" visibleLines="[35,44]"/>

    Bu funksiya `text` parametri qiymatini `housingLocation.city` xususiyati bilan solishtirish uchun `Array`'ning `filter` funksiyasidan foydalanadi. Qiziqarli mashq sifatida bu funksiyani istalgan xususiyat yoki bir nechta xususiyat boʻyicha moslashtiradigan qilib yangilashingiz mumkin.

1.  Kodingizni saqlang.

1.  Brauzerni yangilang va matn kiritib "Search" tugmasini bosganingizda turar joy maʼlumotlarini shahar boʻyicha qidira olishingizni tasdiqlang.

       <img alt="filtered search results based on user input" src="assets/images/tutorials/first-app/homes-app-lesson-13-step-3.png">

    </docs-step>

</docs-workflow>

SUMMARY: Bu darsda siz ilovangizni shablon qiymatlari bilan ishlash uchun shablon oʻzgaruvchilaridan foydalanadigan qilib yangiladingiz va hodisa bogʻlash hamda massiv funksiyalari yordamida qidiruv imkoniyatini qoʻshdingiz.

Bu darsda yoritilgan mavzular haqida koʻproq maʼlumot olish uchun quyidagilarga qarang:

<docs-pill-row>
  <docs-pill href="guide/templates" title="Shablon oʻzgaruvchilari"/>
  <docs-pill href="guide/templates/event-listeners" title="Hodisalarga ishlov berish"/>
</docs-pill-row>
