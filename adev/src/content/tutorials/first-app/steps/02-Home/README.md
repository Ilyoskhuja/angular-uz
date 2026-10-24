# Home komponentini yarating

Bu darslik darsi Angular ilovangiz uchun yangi [komponent](guide/components) yaratishni koʻrsatadi.

<docs-video src="https://www.youtube.com/embed/R0nRX8jD2D0?si=OMVaw71EIa44yIOJ"/>

## Nimalarni oʻrganasiz {#what-youll-learn}

Ilovangizda yangi komponent paydo boʻladi: `Home`.

## Angular komponentlarining konseptual koʻrinishi {#conceptual-preview-of-angular-components}

Angular ilovalari komponentlar atrofida quriladi — komponentlar Angular'ning qurilish bloklaridir.
Komponentlar ilovadagi elementning funksiyasi va koʻrinishini taʼminlovchi kod, HTML joylashuvi (layout) va CSS stil maʼlumotlarini oʻz ichiga oladi.
Angular'da komponentlar boshqa komponentlarni oʻz ichiga olishi mumkin. Ilovaning funksiyalari va koʻrinishini komponentlarga boʻlib tashlash mumkin.

Angular'da komponentlar oʻz xususiyatlarini belgilovchi metamaʼlumotlarga ega.
`Home` komponentini yaratganingizda quyidagi xususiyatlardan foydalanasiz:

- `selector`: Angular shablonlarda komponentga qanday murojaat qilishini tavsiflaydi.
- `imports`: komponentning bogʻliqliklarini tavsiflaydi.
- `template`: komponentning HTML belgilanishi (markup) va joylashuvini tavsiflaydi.
- `styleUrls`: komponent foydalanadigan CSS fayllarining URL manzillarini massivda sanab oʻtadi.

<docs-pill-row>
  <docs-pill href="api/core/Component" title="Komponentlar haqida koʻproq bilib oling"/>
</docs-pill-row>

<docs-workflow>

<docs-step title="`Home` komponentini yarating {#create-the-home}">
Bu qadamda ilovangiz uchun yangi komponent yaratasiz.

IDE'ingizning **Terminal** panelida:

1. Loyiha katalogingizda `first-app` katalogiga oʻting.
1. Yangi `Home` yaratish uchun quyidagi buyruqni bajaring

   ```shell
   ng generate component home
   ```

1. Ilovangizni build qilish va ishga tushirish uchun quyidagi buyruqni bajaring.

   NOTE: Bu qadam faqat lokal muhitingiz uchun!

   ```shell
   ng serve
   ```

1. Brauzerni ochib, ilovani koʻrish uchun `http://localhost:4200` manziliga oʻting.

1. Ilova xatosiz build boʻlishini tasdiqlang.

   HELPFUL: U oldingi darsdagi kabi koʻrinishi kerak, chunki yangi komponent qoʻshgan boʻlsangiz-da, uni hali ilovaning hech bir shabloniga kiritmagansiz.

1. Keyingi qadamlarni bajarayotganingizda `ng serve`'ni ishlab turgan holda qoldiring.
   </docs-step>

<docs-step title="Yangi komponentni ilovangiz joylashuviga qoʻshing {#add-the-new-component-to-your-apps-layout}">
Bu qadamda yangi `Home` komponentini ilovangizning asosiy (root) komponenti `App`'ga qoʻshasiz, shunda u ilovangiz joylashuvida koʻrinadi.

IDE'ingizning **Edit** panelida:

1.  Muharrirda `app.ts` faylini oching.
1.  `app.ts` faylida fayl darajasidagi importlarga quyidagi qatorni qoʻshib, `Home`'ni import qiling.

      <docs-code header="src/app/app.ts faylida Home'ni import qiling" path="adev/src/content/tutorials/first-app/steps/03-HousingLocation/src/app/app.ts" visibleLines="[2]"/>

1.  `app.ts` faylida, `@Component` ichida, `imports` massiv xususiyatini yangilab, `Home`'ni qoʻshing.

      <docs-code header="src/app/app.ts faylida almashtiring" path="adev/src/content/tutorials/first-app/steps/03-HousingLocation/src/app/app.ts" visibleLines="[6]"/>

1.  `app.ts` faylida, `@Component` ichida, `template` xususiyatini quyidagi HTML kodini oʻz ichiga oladigan qilib yangilang.

      <docs-code language="angular-ts" header="src/app/app.ts faylida almashtiring" path="adev/src/content/tutorials/first-app/steps/03-HousingLocation/src/app/app.ts" visibleLines="[7,16]"/>

1.  `app.ts` faylidagi oʻzgarishlaringizni saqlang.
1.  Agar `ng serve` ishlab turgan boʻlsa, ilova yangilanishi kerak.
    Agar `ng serve` ishlamayotgan boʻlsa, uni qayta ishga tushiring.
    Ilovangizdagi _Hello world_ matni `Home` komponentidan kelgan _home works!_ matniga oʻzgarishi kerak.
1.  Brauzerda ishlab turgan ilovani tekshirib, ilova yangilanganini tasdiqlang.

  <img alt="browser frame of page displaying the text 'home works!'" src="assets/images/tutorials/first-app/homes-app-lesson-02-step-2.png">

</docs-step>

<docs-step title="`Home` komponentiga imkoniyatlar qoʻshing {#add-features-to-home}">

Bu qadamda `Home` komponentiga imkoniyatlar qoʻshasiz.

Oldingi qadamda standart `Home` komponentini ilovangiz shabloniga qoʻshdingiz, shunda uning standart HTML'i ilovada paydo boʻldi.
Bu qadamda keyingi darslardan birida ishlatiladigan qidiruv filtri va tugmasini qoʻshasiz.
Hozircha `Home` komponentida boshqa hech narsa boʻlmaydi.
Eʼtibor bering, bu qadam qidiruv elementlarini joylashuvga hozircha hech qanday funksionallikisiz qoʻshadi.

Agar boshlangʻich loyihani yuklab olish oʻrniga yangi Angular loyihasidan
(ng new) boshlagan boʻlsangiz: qidiruv tugmasi va input chegarasi koʻrinishi uchun `src/styles.css` fayliga quyidagi global stillarni qoʻshing:

```css
:root {
  --primary-color: #605dc8;
  --secondary-color: #8b89e6;
  --accent-color: #e8e7fa;
  --shadow-color: #e8e8e8;
}

button.primary {
  padding: 10px;
  border: solid 1px var(--primary-color);
  background: var(--primary-color);
  color: white;
  border-radius: 8px;
}
```

IDE'ingizning **Edit** panelida:

1.  `first-app` katalogida muharrirda `home.ts` faylini oching.
1.  `home.ts` faylida, `@Component` ichida, `template` xususiyatini quyidagi kod bilan yangilang.

      <docs-code language="angular-ts" header="src/app/home/home.ts faylida almashtiring" path="adev/src/content/tutorials/first-app/steps/03-HousingLocation/src/app/home/home.ts" visibleLines="[5,12]"/>

1.  Keyin muharrirda `home.css` faylini oching va uning tarkibini quyidagi stillar bilan yangilang.

    NOTE: Brauzerda bularni `src/app/home/home.ts` faylidagi `styles` massiviga joylashtirish mumkin.

       <docs-code header="src/app/home/home.css faylida almashtiring" path="adev/src/content/tutorials/first-app/steps/03-HousingLocation/src/app/home/home.css"/>

1.  Ilova xatosiz build boʻlishini tasdiqlang. Ilovangizda filtr soʻrovi maydoni va tugmani koʻrishingiz kerak, ular stillangan boʻlishi lozim. Keyingi qadamga oʻtishdan oldin barcha xatolarni tuzating.

   <img alt="browser frame of homes-app displaying logo, filter text input box and search button" src="assets/images/tutorials/first-app/homes-app-lesson-02-step-3.png">
</docs-step>

</docs-workflow>

SUMMARY: Bu darsda ilovangiz uchun yangi komponent yaratdingiz va unga filtr kiritish maydoni hamda tugma berdingiz.

Bu darsda yoritilgan mavzular haqida koʻproq maʼlumot olish uchun quyidagilarga qarang:

<docs-pill-row>
  <docs-pill href="cli/generate/component" title="`ng generate component`"/>
  <docs-pill href="api/core/Component" title="`Component` maʼlumotnomasi"/>
  <docs-pill href="guide/components" title="Angular komponentlari umumiy koʻrinishi"/>
</docs-pill-row>