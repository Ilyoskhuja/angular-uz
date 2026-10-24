# Komponent shabloniga interpolyatsiya qoʻshing

Bu darslik darsi shablonda dinamik maʼlumotlarni koʻrsatish uchun Angular shablonlariga interpolyatsiya qoʻshishni koʻrsatadi.

<docs-video src="https://www.youtube.com/embed/eM3zi_n7lNs?si=IFAly3Ss8dwqFx8N&amp;start=338"/>

## Nimalarni oʻrganasiz {#what-youll-learn}

- Ilovangiz `HousingLocation` shablonida interpolyatsiya qilingan qiymatlarni koʻrsatadi.
- Ilovangiz turar joy maʼlumotlarini brauzerda render qiladi.

## Interpolyatsiyaning konseptual koʻrinishi {#conceptual-preview-of-interpolation}

Bu qadamda `input` xususiyatlaridan oʻqilgan qiymatlarni shablonda interpolyatsiya yordamida koʻrsatasiz.

Angular shablonlarida `{{ expression }}` yordamida xususiyatlar, `input`'lar va toʻgʻri JavaScript ifodalaridan olingan qiymatlarni render qilishingiz mumkin.

Batafsilroq tushuntirish uchun [Qiymatlarni interpolyatsiya bilan koʻrsatish](guide/templates/binding#render-dynamic-text-with-text-interpolation) qoʻllanmasiga qarang.

<docs-workflow>

<docs-step title="`HousingLocation` shablonini interpolyatsiya qilingan qiymatlarni oʻz ichiga oladigan qilib yangilang">
Bu qadam `HousingLocation` shabloniga yangi HTML tuzilmasi va interpolyatsiya qilingan qiymatlarni qoʻshadi.

Kod muharririda:

1.  `src/app/housing-location/housing-location.ts` fayliga oʻting
1.  `@Component` dekoratorining template xususiyatida mavjud HTML belgilanishini quyidagi kod bilan almashtiring:

    <docs-code language="angular-ts"  header="housing-location.ts faylida HousingLocation shablonini yangilang" path="adev/src/content/tutorials/first-app/steps/08-ngFor/src/app/housing-location/housing-location.ts" visibleLines="[6,17]"/>

Bu yangilangan shablon kodida `housingLocation.photo`'ni `src` atributiga bogʻlash uchun xususiyat bogʻlashdan foydalandingiz. `alt` atributi rasmning alt matniga koʻproq kontekst berish uchun interpolyatsiyadan foydalanadi.

`housingLocation` xususiyatining `name`, `city` va `state` qiymatlarini kiritish uchun interpolyatsiyadan foydalanasiz.

</docs-step>

<docs-step title="Oʻzgarishlar brauzerda render qilinishini tasdiqlang">
1.  Barcha oʻzgarishlarni saqlang.
1.  Brauzerni oching va ilova namunaviy rasm, shahar va shtat maʼlumotlarini render qilishini tasdiqlang.
    <img alt="browser frame of homes-app displaying logo, filter text input box, search button and the same housing location UI card" src="assets/images/tutorials/first-app/homes-app-lesson-07-step-2.png">
</docs-step>

</docs-workflow>

SUMMARY: Bu darsda yangi HTML tuzilmasi qoʻshdingiz va `HousingLocation` shablonida qiymatlarni render qilish uchun Angular shablon sintaksisidan foydalandingiz.

Endi sizda ikkita muhim koʻnikma bor:

- komponentlarga maʼlumot uzatish
- shablonga qiymatlarni interpolyatsiya qilish

Bu koʻnikmalar bilan ilovangiz endi maʼlumot ulasha oladi va brauzerda dinamik qiymatlarni koʻrsata oladi. Shu paytgacha ajoyib ish qildingiz.

Bu darsda yoritilgan mavzular haqida koʻproq maʼlumot olish uchun quyidagilarga qarang:

<docs-pill-row>
  <docs-pill href="guide/templates" title="Shablon sintaksisi"/>
  <docs-pill href="guide/templates/binding#render-dynamic-text-with-text-interpolation" title="Qiymatlarni interpolyatsiya bilan koʻrsatish"/>
</docs-pill-row>