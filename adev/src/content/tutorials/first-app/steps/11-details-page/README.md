# Tafsilotlar sahifasini ilovaga integratsiya qilish

Bu dars tafsilotlar sahifasini ilovangizga qanday ulashni koʻrsatadi.

<docs-video src="https://www.youtube.com/embed/-jRxG84AzCI?si=CbqIpmRpwp5ZZDnu&amp;start=345"/>

IMPORTANT: Marshrutlashni oʻrganish uchun lokal muhitingizdan foydalanishni tavsiya qilamiz.

## Nimalarni oʻrganasiz {#what-youll-learn}

Bu dars oxirida ilovangiz tafsilotlar sahifasiga marshrutlashni qoʻllab-quvvatlaydi.

## Marshrut parametrlari bilan marshrutlash haqida konseptual koʻrinish {#conceptual-preview-of-routing-with-route-parameters}

Har bir turar joyning foydalanuvchi oʻsha element uchun tafsilotlar sahifasiga oʻtganda koʻrsatilishi kerak boʻlgan oʻziga xos tafsilotlari bor. Bu maqsadga erishish uchun marshrut parametrlaridan foydalanishingiz kerak boʻladi.

Marshrut parametrlari marshrut URL'ining bir qismi sifatida dinamik maʼlumotlarni kiritish imkonini beradi. Foydalanuvchi qaysi turar joyni bosganini aniqlash uchun `HousingLocation` turining `id` xususiyatidan foydalanasiz.

<docs-workflow>

<docs-step title="Dinamik navigatsiya uchun `routerLink`'dan foydalanish {#using-routerlink-for-dynamic-navigation}">
10-darsda siz `src/app/routes.ts` fayliga marshrut parametri `id`'ni aniqlovchi maxsus segmentni oʻz ichiga olgan ikkinchi marshrutni qoʻshdingiz:

```
'details/:id'
```

Bu holda `:id` dinamik boʻlib, kod marshrutni qanday soʻrashiga qarab oʻzgaradi.

1.  `src/app/housing-location/housing-location.ts` faylida `section` elementiga anchor tegini qoʻshing va `routerLink` direktivasini kiriting:

    <docs-code language="angular-ts" header="housing-location.ts fayliga routerLink direktivali anchor qoʻshish" path="adev/src/content/tutorials/first-app/steps/12-forms/src/app/housing-location/housing-location.ts" visibleLines="[18]"/>

    `routerLink` direktivasi Angular router'iga ilovada dinamik havolalar yaratish imkonini beradi. `routerLink`'ga berilgan qiymat — ikki yozuvli massiv: yoʻlning statik qismi va dinamik maʼlumotlar.

    `routerLink` shablonda ishlashi uchun '@angular/router'dan `RouterLink` uchun fayl darajasidagi import qoʻshing, soʻngra komponentning `imports` massivini `RouterLink`'ni oʻz ichiga oladigan qilib yangilang.

1.  Shu nuqtada ilovangizda marshrutlash ishlayotganini tasdiqlashingiz mumkin. Brauzerda bosh sahifani yangilang va biror turar joy uchun "Learn More" tugmasini bosing.

      <img alt="details page displaying the text 'details works!'" src="assets/images/tutorials/first-app/homes-app-lesson-11-step-1.png">

</docs-step>

<docs-step title="Marshrut parametrlarini oling {#get-route-parameters}">
Bu qadamda siz `Details`'da marshrut parametrini olasiz. Hozirda ilova `details works!` matnini koʻrsatadi. Keyin kodni marshrut parametrlari orqali uzatilgan `id` qiymatini koʻrsatadigan qilib yangilaysiz.

1.  `src/app/details/details.ts` faylida shablonni yangilab, `Details`'da ishlatishingiz kerak boʻladigan funksiyalar, klasslar va servislarni import qiling:

      <docs-code header="Fayl darajasidagi importlarni yangilash" path="adev/src/content/tutorials/first-app/steps/12-forms/src/app/details/details.ts" visibleLines="[1,4]"/>

1.  `@Component` dekoratorining `template` xususiyatini `housingLocationId` qiymatini koʻrsatadigan qilib yangilang:

         ```angular-ts
         template: `<p>details works! {{ housingLocationId }}</p>`,
         ```

1.  `Details` klassining tanasini quyidagi kod bilan yangilang:

         ```ts
         export class Details {
            route: ActivatedRoute = inject(ActivatedRoute);
            housingLocationId = -1;
            constructor() {
            this.housingLocationId = Number(this.route.snapshot.params['id']);
            }
         }
         ```

    Bu kod `Details`'ga joriy marshrut haqidagi maʼlumotlarga kirish imkonini beruvchi `ActivatedRoute` router imkoniyatidan foydalanish huquqini beradi. `constructor`'da kod marshrutdan olingan `id` parametrini satrdan (string) songa (number) oʻzgartiradi.

1.  Barcha oʻzgarishlarni saqlang.

1.  Brauzerda turar joylardan birining "Learn More" havolasini bosing va sahifada koʻrsatilgan raqamli qiymat maʼlumotlardagi oʻsha joyning `id` xususiyatiga mos kelishini tasdiqlang.
    </docs-step>

<docs-step title="`Details`'ni moslashtiring {#customize-the-details}">
Endi ilovada marshrutlash toʻgʻri ishlayotgan ekan, `Details` shablonini marshrut parametriga mos turar joyning muayyan maʼlumotlarini koʻrsatadigan qilib yangilash uchun qulay vaqt.

Maʼlumotlarga kirish uchun `HousingService`'ga chaqiruv qoʻshasiz.

1. Shablon kodini quyidagi kodga moslab yangilang:

   <docs-code language="angular-ts" header="src/app/details/details.ts da Details shablonini yangilash" path="adev/src/content/tutorials/first-app/steps/12-forms/src/app/details/details.ts" visibleLines="[8,29]"/>

   `housingLocation` xususiyatlariga ixtiyoriy zanjirlash (optional chaining) operatori `?` orqali murojaat qilinayotganiga eʼtibor bering. Bu `housingLocation` qiymati null yoki undefined boʻlsa, ilova ishdan chiqmasligini taʼminlaydi.

1. `Details` klassining tanasini quyidagi kodga moslab yangilang:

   <docs-code language="angular-ts" header="src/app/details/details.ts da Details klassini yangilash" path="adev/src/content/tutorials/first-app/steps/12-forms/src/app/details/details.ts" visibleLines="[32,41]"/>

   Endi komponentda tanlangan turar joyga asoslanib toʻgʻri maʼlumotni koʻrsatish uchun kod mavjud. `constructor` endi marshrut parametrini `getHousingLocationById` servis funksiyasiga argument sifatida uzatish uchun `HousingService`'ga chaqiruvni oʻz ichiga oladi.

1. Quyidagi stillarni `src/app/details/details.css` fayliga nusxalang:

   <docs-code header="Details uchun stillar qoʻshish" path="adev/src/content/tutorials/first-app/steps/12-forms/src/app/details/details.css" visibleLines="[1,72]"/>

   va oʻzgarishlaringizni saqlang

1. `Details`'da hozirgina yaratilgan `details.css` faylini stillar manbai sifatida ishlating:
   <docs-code language="angular-ts" header="details.ts ni yaratilgan css faylidan foydalanadigan qilib yangilash" path="adev/src/content/tutorials/first-app/steps/12-forms/src/app/details/details.ts" visibleLines="[30]"/>

1. Brauzerda sahifani yangilang va berilgan turar joy uchun "Learn More" havolasini bosganingizda tafsilotlar sahifasi tanlangan element maʼlumotlariga asoslanib toʻgʻri maʼlumotni koʻrsatishini tasdiqlang.

<img alt="Details page listing home info" src="assets/images/tutorials/first-app/homes-app-lesson-11-step-3.png">

</docs-step>

<docs-step title="`Home`'da navigatsiyani tekshiring {#check-navigation-in-the-home}">
Oldingi darsda siz `App` shablonini `routerLink`'ni oʻz ichiga oladigan qilib yangiladingiz. Bu kodni qoʻshish ilovangizni logotip bosilganda `Home`'ga qaytish imkonini beradigan qilib yangiladi.

1.  Kodingiz quyidagiga mos kelishini tasdiqlang:

      <docs-code language="angular-ts" header="app.ts dagi routerLink'ni tasdiqlash" path="adev/src/content/tutorials/first-app/steps/12-forms/src/app/app.ts" visibleLines="[8,19]"/>

    Kodingiz allaqachon yangilangan boʻlishi kerak, lekin ishonch hosil qilish uchun tekshiring.

    </docs-step>

</docs-workflow>

SUMMARY: Bu darsda siz tafsilotlar sahifalarini koʻrsatish uchun marshrutlash qoʻshdingiz.

Endi siz quyidagilarni bilasiz:

- marshrutga maʼlumot uzatish uchun marshrut parametrlaridan foydalanish
- dinamik maʼlumotlar asosida marshrut yaratish uchun `routerLink` direktivasidan foydalanish
- muayyan turar joy maʼlumotlarini koʻrsatish uchun `HousingService`'dan maʼlumot olishda marshrut parametridan foydalanish.

Hozirgacha juda ajoyib ish.

Bu darsda yoritilgan mavzular haqida koʻproq maʼlumot olish uchun quyidagilarga qarang:

<docs-pill-row>
  <docs-pill href="guide/routing/read-route-state#get-information-about-the-current-route-with-activatedroute" title="Marshrut parametrlari"/>
  <docs-pill href="guide/routing" title="Angular'da marshrutlash: umumiy koʻrinish"/>
  <docs-pill href="guide/routing/common-router-tasks" title="Keng tarqalgan marshrutlash vazifalari"/>
  <docs-pill href="https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Optional_chaining" title="Ixtiyoriy zanjirlash operatori"/>
</docs-pill-row>
