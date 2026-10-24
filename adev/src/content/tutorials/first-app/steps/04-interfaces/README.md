# Interfeys yaratish

Bu darslik darsi interfeys yaratish va uni ilovangizning komponentiga kiritishni koʻrsatadi.

<docs-video src="https://www.youtube.com/embed/eM3zi_n7lNs?si=YkFSeUeV8Ixtz8pm"/>

## Nimalarni oʻrganasiz {#what-youll-learn}

- Ilovangizda maʼlumot turi sifatida ishlatish mumkin boʻlgan yangi interfeys paydo boʻladi.
- Ilovangizda yangi interfeysning namunaviy maʼlumotlar bilan toʻldirilgan nusxasi (instance) paydo boʻladi.

## Interfeyslarning konseptual koʻrinishi {#conceptual-preview-of-interfaces}

[Interfeyslar](https://www.typescriptlang.org/docs/handbook/interfaces.html) — ilovangiz uchun maxsus maʼlumot turlari.

Angular qatʼiy tiplashtirilgan dasturlash muhitida ishlash afzalliklaridan foydalanish uchun TypeScript'dan foydalanadi.
Qatʼiy tip tekshiruvi ilovangizdagi bir element boshqasiga notoʻgʻri formatlangan maʼlumot yuborish ehtimolini kamaytiradi.
Bunday tiplar nomuvofiqligi xatolarini TypeScript kompilyatori ushlaydi va koʻplab shunday xatolarni IDE'ingizda ham aniqlash mumkin.

Bu darsda bitta turar joy (housing location) haqidagi maʼlumotlarni ifodalovchi xususiyatlarni belgilash uchun interfeys yaratasiz.

<docs-workflow>

<docs-step title="Yangi Angular interfeysini yarating {#create-a-new-angular-interface}">
Bu qadam ilovangizda yangi interfeys yaratadi.

IDE'ingizning **Terminal** panelida:

1. Loyiha katalogingizda `first-app` katalogiga oʻting.
1. `first-app` katalogida yangi interfeys yaratish uchun quyidagi buyruqni bajaring.

   ```shell

   ng generate interface housinglocation

   ```

1. Ilovani build qilish va `http://localhost:4200` manzilida ishga tushirish uchun `ng serve` buyrugʻini bajaring.
1. Ilovangizni koʻrish uchun brauzerda `http://localhost:4200` manzilini oching.
1. Ilova xatosiz build boʻlishini tasdiqlang.
   Keyingi qadamga oʻtishdan oldin barcha xatolarni tuzating.
   </docs-step>

<docs-step title="Yangi interfeysga xususiyatlar qoʻshing {#add-properties-to-the-new-interface}">
Bu qadam interfeysga ilovangiz turar joyni ifodalash uchun zarur boʻlgan xususiyatlarni qoʻshadi.

1.  IDE'ingizning **Terminal** panelida, agar hali ishlamayotgan boʻlsa, ilovani build qilish va `http://localhost:4200` manzilida ishga tushirish uchun `ng serve` buyrugʻini ishga tushiring.
1.  IDE'ingizning **Edit** panelida `src/app/housinglocation.ts` faylini oching.
1.  `housinglocation.ts` faylida yangi interfeysingiz ushbu misolga mos kelishi uchun standart tarkibni quyidagi kod bilan almashtiring.

      <docs-code header="src/app/housinglocation.ts faylini ushbu kodga moslab yangilang" path="adev/src/content/tutorials/first-app/steps/05-inputs/src/app/housinglocation.ts" visibleLines="[1,10]" />

1.  Oʻzgarishlaringizni saqlang va ilova hech qanday xato koʻrsatmasligini tasdiqlang. Keyingi qadamga oʻtishdan oldin barcha xatolarni tuzating.

Shu nuqtada siz turar joy haqidagi maʼlumotlarni — `id`, `name` va joylashuv maʼlumotlarini — ifodalovchi interfeysni belgiladingiz.
</docs-step>

<docs-step title="Ilovangiz uchun sinov uyini yarating {#create-a-test-house-for-your-app}">
Sizda interfeys bor, lekin siz undan hali foydalanmayapsiz.

Bu qadamda interfeysning nusxasini yaratasiz va unga namunaviy maʼlumotlar tayinlaysiz.
Bu namunaviy maʼlumotlar ilovangizda hali koʻrinmaydi.
Bunga erishish uchun yana bir necha darsni yakunlash kerak.

1.  IDE'ingizning **Terminal** panelida, agar hali ishlamayotgan boʻlsa, ilovani build qilish va `http://localhost:4200` manzilida ishga tushirish uchun `ng serve` buyrugʻini bajaring.
1.  IDE'ingizning **Edit** panelida `src/app/home/home.ts` faylini oching.
1.  `src/app/home/home.ts` faylida `Home` yangi interfeysdan foydalana olishi uchun mavjud `import` ifodalaridan keyin quyidagi import ifodasini qoʻshing.

      <docs-code language="angular-ts" header="src/app/home/home.ts faylida Home'ni import qiling" path="adev/src/content/tutorials/first-app/steps/05-inputs/src/app/home/home.ts" visibleLines="[3]"/>

1.  `src/app/home/home.ts` faylida komponentda yangi interfeysning bitta nusxasini yaratish uchun boʻsh `export class Home {}` taʼrifini quyidagi kod bilan almashtiring.

      <docs-code language="angular-ts" header="src/app/home/home.ts fayliga namunaviy maʼlumotlarni qoʻshing" path="adev/src/content/tutorials/first-app/steps/05-inputs/src/app/home/home.ts" visibleLines="[21,34]"/>

1.  `home.ts` faylingiz ushbu misolga mos kelishini tasdiqlang.

      <docs-code language="angular-ts" header="src/app/home/home.ts" path="adev/src/content/tutorials/first-app/steps/05-inputs/src/app/home/home.ts" visibleLines="[1,34]" />

    `Home` klassiga `HousingLocation` turidagi `housingLocation` xususiyatini qoʻshish orqali maʼlumotlar interfeys tavsifiga mos kelishini tasdiqlay olamiz. Agar maʼlumotlar interfeys tavsifini qoniqtirmasa, IDE bizga foydali xatolarni koʻrsatish uchun yetarli maʼlumotga ega boʻladi.

1.  Oʻzgarishlaringizni saqlang va ilovada hech qanday xato yoʻqligini tasdiqlang. Brauzerni oching va ilovangiz hali ham "housing-location works!" xabarini koʻrsatishini tasdiqlang

      <img alt="browser frame of homes-app displaying logo, filter text input box and search button and the message 'housing-location works!'" src="assets/images/tutorials/first-app/homes-app-lesson-03-step-2.png">

1.  Keyingi qadamga oʻtishdan oldin barcha xatolarni tuzating.
    </docs-step>

</docs-workflow>

SUMMARY: Bu darsda ilovangiz uchun yangi maʼlumot turi yaratuvchi interfeys yaratdingiz.
Bu yangi maʼlumot turi `HousingLocation` maʼlumotlari qayerda talab qilinishini koʻrsatish imkonini beradi.
Bu yangi maʼlumot turi shuningdek IDE'ingiz va TypeScript kompilyatoriga `HousingLocation` maʼlumotlari talab qilingan joyda ishlatilishini taʼminlash imkonini beradi.

Bu darsda yoritilgan mavzular haqida koʻproq maʼlumot olish uchun quyidagilarga qarang:

<docs-pill-row>
  <docs-pill href="cli/generate/interface" title="ng generate interface"/>
  <docs-pill href="cli/generate" title="ng generate"/>
</docs-pill-row>