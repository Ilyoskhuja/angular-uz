# Ilovaning HousingLocation komponentini yarating

Bu darslik darsi Angular ilovangizga `HousingLocation` komponentini qanday qoʻshishni koʻrsatadi.

<docs-video src="https://www.youtube.com/embed/R0nRX8jD2D0?si=U4ONEbPvtptdUHTt&amp;start=440"/>

## Nimalarni oʻrganasiz {#what-youll-learn}

- Ilovangizda yangi komponent paydo boʻladi: `HousingLocation`, va u komponent ilovangizga qoʻshilganini tasdiqlovchi xabarni koʻrsatadi.

<docs-workflow>

<docs-step title="`HousingLocation` komponentini yarating">
Bu qadamda ilovangiz uchun yangi komponent yaratasiz.

IDE'ingizning **Terminal** panelida:

1. Loyiha katalogingizda `first-app` katalogiga oʻting.

1. Yangi `HousingLocation` yaratish uchun quyidagi buyruqni bajaring

   ```shell
   ng generate component housingLocation
   ```

1. Ilovangizni build qilish va ishga tushirish uchun quyidagi buyruqni bajaring.

   ```shell
   ng serve
   ```

   NOTE: Bu qadam faqat lokal muhitingiz uchun!

1. Brauzerni ochib, ilovani koʻrish uchun `http://localhost:4200` manziliga oʻting.
1. Ilova xatosiz build boʻlishini tasdiqlang.

   HELPFUL: U oldingi darsdagi kabi koʻrinishi kerak, chunki yangi komponent qoʻshgan boʻlsangiz-da, uni hali ilovaning hech bir shabloniga kiritmagansiz.

1. Keyingi qadamlarni bajarayotganingizda `ng serve`'ni ishlab turgan holda qoldiring.
   </docs-step>

<docs-step title="Yangi komponentni ilovangiz joylashuviga qoʻshing">
Bu qadamda yangi `HousingLocation` komponentini ilovangizning `Home` komponentiga qoʻshasiz, shunda u ilovangiz joylashuvida koʻrinadi.

IDE'ingizning **Edit** panelida:

1.  Muharrirda `home.ts` faylini oching.
1.  `home.ts` faylida fayl darajasidagi importlarga quyidagi qatorni qoʻshib, `HousingLocation`'ni import qiling.

      <docs-code header="src/app/home/home.ts faylida HousingLocation'ni import qiling" path="adev/src/content/tutorials/first-app/steps/04-interfaces/src/app/home/home.ts" visibleLines="[2]"/>

1.  Keyin `@Component` metamaʼlumotlarining `imports` xususiyatini massivga `HousingLocation`'ni qoʻshib yangilang.

      <docs-code  header="src/app/home/home.ts faylidagi imports massiviga HousingLocation'ni qoʻshing" path="adev/src/content/tutorials/first-app/steps/04-interfaces/src/app/home/home.ts" visibleLines="[6]"/>

1.  Endi komponent `Home` shablonida ishlatishga tayyor. `@Component` metamaʼlumotlarining `template` xususiyatini `<app-housing-location>` tegiga havola kiritib yangilang.

      <docs-code language="angular-ts" header="src/app/home/home.ts faylidagi komponent shabloniga housing location'ni qoʻshing" path="adev/src/content/tutorials/first-app/steps/04-interfaces/src/app/home/home.ts" visibleLines="[7,17]"/>

</docs-step>

<docs-step title="Komponent uchun stillarni qoʻshing">
Bu qadamda ilova toʻgʻri render qilinishi uchun `HousingLocation` komponenti uchun oldindan yozilgan stillarni ilovangizga nusxalaysiz.

1. `src/app/housing-location/housing-location.css` faylini oching va quyidagi stillarni faylga joylashtiring:

   NOTE: Brauzerda bularni `src/app/housing-location/housing-location.ts` faylidagi `styles` massiviga joylashtirish mumkin.

   <docs-code header="src/app/housing-location/housing-location.css faylida housing location komponentiga CSS stillarini qoʻshing" path="adev/src/content/tutorials/first-app/steps/04-interfaces/src/app/housing-location/housing-location.css"/>

1. Kodingizni saqlang, brauzerga qayting va ilova xatosiz build boʻlishini tasdiqlang. Ekranda "housing-location works!" xabari render qilinganini koʻrishingiz kerak. Keyingi qadamga oʻtishdan oldin barcha xatolarni tuzating.

   <img alt="browser frame of homes-app displaying logo, filter text input box and search button and the message 'housing-location works!" src="assets/images/tutorials/first-app/homes-app-lesson-03-step-2.png">

</docs-step>

</docs-workflow>

SUMMARY: Bu darsda ilovangiz uchun yangi komponent yaratdingiz va uni ilova joylashuviga qoʻshdingiz.