# Salom, dunyo

Bu birinchi dars boshlangʻich nuqta boʻlib xizmat qiladi — ushbu darslikdagi har bir dars toʻliq Angular ilovasini yaratish uchun unga yangi imkoniyatlar qoʻshib boradi. Bu darsda biz ilovani mashhur "Hello World" matnini koʻrsatadigan qilib yangilaymiz.

<docs-video src="https://www.youtube.com/embed/UnOwDuliqZA?si=uML-cDRbrxmYdD_9"/>

## Nimalarni oʻrganasiz {#what-youll-learn}

Agar ilovangiz brauzerda muvaffaqiyatli ishga tushib, bajarilgan kontentni xatosiz koʻrsatsa, bu dasturlash muhitingiz va IDE'ingiz Angular ilovasini yaratishni boshlash uchun toʻgʻri sozlanganini tasdiqlaydi.

NOTE: Agar oʻrnatilgan muharrirda ishlayotgan boʻlsangiz, [toʻrtinchi qadamga](#create-hello-world) oʻting.
Brauzerdagi oʻyin maydonchasida (playground) ishlaganda ilovani ishga tushirish uchun `ng serve` bajarish shart emas. `ng generate` kabi boshqa buyruqlarni oʻng tomoningizdagi konsol oynasida bajarish mumkin.

<docs-workflow>

<docs-step title="Standart ilovani yuklab oling">
Kod muharririning yuqori oʻng panelidagi "Download" belgisini bosishdan boshlang. Bu ushbu darslikning manba kodini oʻz ichiga olgan `.zip` faylini yuklab oladi. Uni lokal Terminal va IDE'ingizda oching, soʻng standart ilovani sinab koʻrishga oʻting.

Darslikning istalgan qadamida bu belgini bosib, oʻsha qadamning manba kodini yuklab olishingiz va shu yerdan boshlashingiz mumkin.
</docs-step>

<docs-step title="Standart ilovani sinab koʻring">
Bu qadamda, standart boshlangʻich ilovani yuklab olganingizdan soʻng, standart Angular ilovasini build qilasiz.
Bu dasturlash muhitingizda darslikni davom ettirish uchun kerakli hamma narsa mavjudligini tasdiqlaydi.

IDE'ingizning **Terminal** panelida:

1. Loyiha katalogingizda `first-app` katalogiga oʻting.
1. Ilovani ishga tushirish uchun zarur boʻlgan bogʻliqliklarni oʻrnatish uchun quyidagi buyruqni bajaring.

   ```shell
   npm install
   ```

1. Standart ilovani build qilish va ishga tushirish (serve) uchun quyidagi buyruqni bajaring.

   ```shell
   ng serve
   ```

   Ilova xatosiz build boʻlishi kerak.

1. Dasturlash kompyuteringizdagi veb-brauzerda `http://localhost:4200` manzilini oching.
1. Brauzerda standart veb-sayt koʻrinishini tasdiqlang.
1. Keyingi qadamlarni bajarayotganingizda `ng serve`'ni ishlab turgan holda qoldirishingiz mumkin.
   </docs-step>

<docs-step title="Loyihadagi fayllarni koʻrib chiqing">
Bu qadamda standart Angular ilovasini tashkil etuvchi fayllar bilan tanishasiz.

IDE'ingizning **Explorer** panelida:

1. Loyiha katalogingizda `first-app` katalogiga oʻting.
1. Quyidagi fayllarni koʻrish uchun `src` katalogini oching.
   1. Fayl koʻrgichida (file explorer) Angular ilovasi fayllarini (`/src`) toping.
      1. `index.html` — ilovaning yuqori darajadagi HTML shabloni.
      1. `styles.css` — ilovaning yuqori darajadagi stillar jadvali.
      1. `main.ts` — ilova ishga tushadigan joy.
      1. `favicon.ico` — har qanday veb-saytda boʻlgani kabi, ilovaning belgisi (ikonkasi).
   1. Fayl koʻrgichida Angular ilovasining komponent fayllarini (`/app`) toping.
      1. `app.ts` — `app-root` komponentini tavsiflovchi manba fayli.
         Bu ilovadagi yuqori darajadagi Angular komponenti. Komponent — Angular ilovasining asosiy qurilish bloki.
         Komponent tavsifi komponentning kodi, HTML shabloni va stillarini oʻz ichiga oladi; ular shu faylda yoki alohida fayllarda tavsiflanishi mumkin.

         Bu ilovada stillar alohida faylda, komponentning kodi va HTML shabloni esa shu faylda joylashgan.

      1. `app.css` — bu komponentning stillar jadvali.
      1. Yangi komponentlar shu katalogga qoʻshiladi.

   1. Fayl koʻrgichida ilova ishlatadigan rasmlarni oʻz ichiga olgan rasmlar katalogini (`/public`) toping.
   1. Fayl koʻrgichida Angular ilovasini build qilish va ishga tushirish uchun zarur boʻlgan, lekin siz odatda bevosita ishlamaydigan fayllar va kataloglarni toping.
      1. `.angular` — Angular ilovasini build qilish uchun zarur fayllarni oʻz ichiga oladi.
      1. `.e2e` — ilovani testlash uchun ishlatiladigan fayllarni oʻz ichiga oladi.
      1. `.node_modules` — ilova foydalanadigan node.js paketlarini oʻz ichiga oladi.
      1. `angular.json` — Angular ilovasini ilova build qiluvchi vositalarga tavsiflaydi.
      1. `package.json` — tayyor ilovani ishga tushirish uchun `npm` (node paket menejeri) tomonidan ishlatiladi.
      1. `tsconfig.*` — ilova konfiguratsiyasini TypeScript kompilyatoriga tavsiflovchi fayllar.

Angular ilovasi loyihasini tashkil etuvchi fayllarni koʻrib chiqqach, keyingi qadamga oʻting.
</docs-step>

<docs-step title="`Hello World` yarating">
Bu qadamda koʻrsatiladigan kontentni oʻzgartirish uchun Angular loyihasi fayllarini yangilaysiz.

IDE'ingizda:

1. `first-app/src/index.html` faylini oching.
   NOTE: Bu qadam va keyingisi faqat lokal muhitingiz uchun!

1. `index.html` faylida ilova sarlavhasini yangilash uchun `<title>` elementini quyidagi kod bilan almashtiring.

   <docs-code header="src/index.html faylida almashtiring" path="adev/src/content/tutorials/first-app/steps/02-Home/src/index.html" visibleLines="[5]"/>

   Soʻng `index.html` faylida hozir qilgan oʻzgarishlaringizni saqlang.

1. Keyin `first-app/src/app/app.ts` faylini oching.
1. `app.ts` faylida, `@Component` taʼrifida, ilova komponentidagi matnni oʻzgartirish uchun `template` qatorini quyidagi kod bilan almashtiring.

   <docs-code language="angular-ts" header="src/app/app.ts faylida almashtiring" path="adev/src/content/tutorials/first-app/steps/02-Home/src/app/app.ts" visibleLines="[6]"/>

1. `app.ts` faylida, `App` klassi taʼrifida, komponent sarlavhasini oʻzgartirish uchun `title` qatorini quyidagi kod bilan almashtiring.

   <docs-code header="src/app/app.ts faylida almashtiring" path="adev/src/content/tutorials/first-app/steps/02-Home/src/app/app.ts" visibleLines="[10]"/>

   Soʻng `app.ts` faylida qilgan oʻzgarishlaringizni saqlang.

1. Agar 1-qadamdagi `ng serve` buyrugʻini toʻxtatgan boʻlsangiz, IDE'ingizning **Terminal** oynasida `ng serve`'ni qayta ishga tushiring.
1. Brauzeringizni ochib, `localhost:4200` manziliga oʻting va ilova xatosiz build boʻlib, sarlavhada _Homes_, ilova tanasida esa _Hello world_ koʻrsatilishini tasdiqlang:
   <img alt="browser frame of page displaying the text 'Hello World'" src="assets/images/tutorials/first-app/homes-app-lesson-01-browser.png">
   </docs-step>

</docs-workflow>

SUMMARY: Bu darsda standart Angular ilovasini _Hello world_ koʻrsatadigan qilib yangiladingiz.
Bu jarayonda ilovangizni testlash uchun lokal ishga tushiruvchi `ng serve` buyrugʻi bilan tanishdingiz.

Bu darsda yoritilgan mavzular haqida koʻproq maʼlumot olish uchun quyidagilarga qarang:

<docs-pill-row>
  <docs-pill href="guide/components" title="Angular komponentlari"/>
  <docs-pill href="tools/cli" title="Angular CLI bilan ilovalar yaratish"/>
</docs-pill-row>