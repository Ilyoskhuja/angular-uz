# Ilovaga marshrutlar qoʻshish

Bu dars ilovangizga marshrutlarni qanday qoʻshishni koʻrsatadi.

<docs-video src="https://www.youtube.com/embed/r5DEBMuStPw?si=H6Bx6nLJoMLaMxkx" />

IMPORTANT: Marshrutlashni oʻrganish uchun lokal muhitingizdan foydalanishni tavsiya qilamiz.

## Nimalarni oʻrganasiz {#what-youll-learn}

Bu dars oxirida ilovangiz marshrutlashni qoʻllab-quvvatlaydi.

## Marshrutlash haqida konseptual koʻrinish {#conceptual-preview-of-routing}

Bu darslik Angular'da marshrutlash bilan tanishtiradi. Marshrutlash — ilovadagi bir komponentdan boshqasiga oʻtish imkoniyati. [Bir sahifali ilovalarda (SPA)](guide/routing) foydalanuvchi soʻragan koʻrinishni aks ettirish uchun sahifaning faqat ayrim qismlari yangilanadi.

[Angular Router](guide/routing) foydalanuvchilarga marshrutlarni eʼlon qilish va ilova ushbu marshrutni soʻraganda ekranda qaysi komponent koʻrsatilishi kerakligini belgilash imkonini beradi.

Bu darsda siz tafsilotlar sahifasiga oʻtish uchun ilovangizda marshrutlashni yoqasiz.

<docs-workflow>

<docs-step title="Standart tafsilotlar komponentini yarating {#create-a-default-details-component-}">
1. Terminaldan `Details`'ni yaratish uchun quyidagi buyruqni kiriting:

    ```shell
    ng generate component details
    ```

    Bu komponent berilgan turar joy haqida koʻproq maʼlumot beruvchi tafsilotlar sahifasini ifodalaydi.

</docs-step>

<docs-step title="Ilovaga marshrutlashni qoʻshing {#add-routing-to-the-application}">
1.  `src/app` katalogida `routes.ts` nomli fayl yarating. Bu faylda ilovadagi marshrutlarni aniqlaymiz.

2.  Ilovada marshrutlashni yoqish uchun `main.ts` faylida quyidagi yangilanishlarni kiriting:
    1.  Marshrutlar faylini va `provideRouter` funksiyasini import qiling:

          <docs-code header="src/main.ts fayliga marshrutlash tafsilotlarini import qilish" path="adev/src/content/tutorials/first-app/steps/11-details-page/src/main.ts" visibleLines="[3,4]"/>

    1.  `bootstrapApplication` chaqiruvini marshrutlash konfiguratsiyasini oʻz ichiga oladigan qilib yangilang:

          <docs-code header="src/main.ts fayliga router konfiguratsiyasini qoʻshish" path="adev/src/content/tutorials/first-app/steps/11-details-page/src/main.ts" visibleLines="[6,8]"/>

3.  `src/app/app.ts` faylida komponentni marshrutlashdan foydalanadigan qilib yangilang:
    1.  Router direktivalari `RouterOutlet` va `RouterLink` uchun fayl darajasidagi importlarni qoʻshing:

          <docs-code language="angular-ts" header="src/app/app.ts fayliga router direktivalarini import qilish" path="adev/src/content/tutorials/first-app/steps/11-details-page/src/app/app.ts" visibleLines="[3]"/>

    1.  `RouterOutlet` va `RouterLink`'ni `@Component` metadatasining imports roʻyxatiga qoʻshing

          <docs-code language="angular-ts" header="src/app/app.ts da komponent importlariga router direktivalarini qoʻshish" path="adev/src/content/tutorials/first-app/steps/11-details-page/src/app/app.ts" visibleLines="[6]"/>

    1.  `template` xususiyatida `<app-home />` tegini `<router-outlet>` direktivasi bilan almashtiring va bosh sahifaga qaytish havolasini qoʻshing. Kodingiz quyidagi kodga mos boʻlishi kerak:

          <docs-code language="angular-ts" header="src/app/app.ts fayliga router-outlet qoʻshish" path="adev/src/content/tutorials/first-app/steps/11-details-page/src/app/app.ts" visibleLines="[7,18]"/>

</docs-step>

<docs-step title="Yangi komponentga marshrut qoʻshing {#add-route-to-new-component}">
Oldingi qadamda siz shablondagi `<app-home>` komponentiga havolani olib tashladingiz. Bu qadamda oʻsha komponentga yangi marshrut qoʻshasiz.

1. Marshrut yaratish uchun `routes.ts` faylida quyidagi yangilanishlarni bajaring.
   1. Marshrut taʼriflarida ishlatadigan `Home`, `Details` va `Routes` turi uchun fayl darajasidagi importlarni qoʻshing.

      <docs-code header="Komponentlar va Routes'ni import qilish" path="adev/src/content/tutorials/first-app/steps/11-details-page/src/app/routes.ts" visibleLines="[1,3]"/>

   1. `Routes` turidagi `routeConfig` nomli oʻzgaruvchini aniqlang va ilova uchun ikkita marshrut belgilang:
      <docs-code header="Ilovaga marshrutlar qoʻshish" path="adev/src/content/tutorials/first-app/steps/11-details-page/src/app/routes.ts" visibleLines="[5,18]"/>

      `routeConfig` massividagi yozuvlar ilovadagi marshrutlarni ifodalaydi. Birinchi yozuv url `''` ga mos kelganda `Home`'ga oʻtadi. Ikkinchi yozuvda kelgusi darsda qayta koʻrib chiqiladigan maxsus formatlash ishlatilgan.

1. Barcha oʻzgarishlarni saqlang va ilova brauzerda ishlayotganini tasdiqlang. Ilova hali ham turar joylar roʻyxatini koʻrsatishi kerak.
   </docs-step>

</docs-workflow>

SUMMARY: Bu darsda siz ilovangizda marshrutlashni yoqdingiz va yangi marshrutlarni aniqladingiz. Endi ilovangiz koʻrinishlar oʻrtasida navigatsiyani qoʻllab-quvvatlaydi. Keyingi darsda berilgan turar joy uchun "tafsilotlar" sahifasiga oʻtishni oʻrganasiz.

Ilovangiz bilan ajoyib natijalarga erishmoqdasiz, barakalla.

Bu darsda yoritilgan mavzular haqida koʻproq maʼlumot olish uchun quyidagilarga qarang:

<docs-pill-row>
  <docs-pill href="guide/routing" title="Angular'da marshrutlash: umumiy koʻrinish"/>
  <docs-pill href="guide/routing/common-router-tasks" title="Keng tarqalgan marshrutlash vazifalari"/>
</docs-pill-row>
