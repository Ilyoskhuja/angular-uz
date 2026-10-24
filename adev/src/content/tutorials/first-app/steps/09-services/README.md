# Angular servislari

Bu dars Angular servisini qanday yaratishni va uni ilovangizga qoʻshish uchun bogʻliqliklarni inyeksiya qilishdan qanday foydalanishni koʻrsatadi.

<docs-video src="https://www.youtube.com/embed/-jRxG84AzCI?si=rieGfJawp9xJ00Sz"/>

## Nimalarni oʻrganasiz {#what-youll-learn}

Ilovangizda unga maʼlumotlarni yetkazib beruvchi servis boʻladi.
Bu dars oxirida servis maʼlumotlarni lokal, statik maʼlumotlardan oʻqiydi.
Keyingi darslardan birida servisni maʼlumotlarni veb-servisdan oladigan qilib yangilaysiz.

## Servislar haqida konseptual koʻrinish {#conceptual-preview-of-services}

Bu darslik Angular servislari va bogʻliqliklarni inyeksiya qilish (dependency injection) bilan tanishtiradi.

### Angular servislari {#angular-services}

_Angular servislari_ ilovangizdagi bir nechta komponent tomonidan ishlatilishi mumkin boʻlgan Angular ilovasi maʼlumotlari va funksiyalarini ajratib olish imkonini beradi.
Bir nechta komponent tomonidan ishlatilishi uchun servis _inyeksiya qilinadigan (injectable)_ boʻlishi kerak.
Inyeksiya qilinadigan va komponent tomonidan ishlatiladigan servislar oʻsha komponentning bogʻliqliklariga aylanadi.
Komponent bu servislarga bogʻliq boʻladi va ularsiz ishlay olmaydi.

### Bogʻliqliklarni inyeksiya qilish {#dependency-injection}

_Bogʻliqliklarni inyeksiya qilish_ — ilova komponentlarining bogʻliqliklarini va boshqa komponentlar foydalana oladigan servislarni boshqaradigan mexanizm.

<docs-workflow>

<docs-step title="Ilovangiz uchun yangi servis yarating {#create-a-new-service-for-your-app}">
Bu qadam ilovangiz uchun inyeksiya qilinadigan servis yaratadi.

IDE'ingizning **Terminal** panelida:

1. Loyiha katalogingizda `first-app` katalogiga oʻting.
1. `first-app` katalogida yangi servis yaratish uchun quyidagi buyruqni bajaring.

   ```shell
   ng generate service housing --skip-tests
   ```

1. Ilovani build qilish va `http://localhost:4200` manzilida ishga tushirish (serve) uchun `ng serve`'ni bajaring.
1. Ilova xatosiz build boʻlishini tasdiqlang.
   Keyingi qadamga oʻtishdan oldin barcha xatolarni tuzating.
   </docs-step>

<docs-step title="Yangi servisga statik maʼlumotlar qoʻshing {#add-static-data-to-the-new-service}">
Bu qadam yangi servisingizga namunaviy maʼlumotlar qoʻshadi.
Keyingi darslardan birida statik maʼlumotlarni haqiqiy ilovadagidek maʼlumot olish uchun veb-interfeys bilan almashtirasiz.
Hozircha ilovangizning yangi servisi shu paytgacha `Home`'da lokal yaratilgan maʼlumotlardan foydalanadi.

IDE'ingizning **Edit** panelida:

1. `src/app/home/home.ts` faylidagi `Home`'dan `baseUrl` oʻzgaruvchisini va `housingLocationList` oʻzgaruvchisini massiv qiymati bilan birga nusxalang.
1. `src/app/housing.service.ts` faylida:
   1. `HousingService` klassi ichiga oldingi qadamda `Home`'dan nusxalagan oʻzgaruvchilarni joylashtiring.
   1. `HousingService` klassi ichiga, hozirgina nusxalagan maʼlumotlardan keyin, quyidagi funksiyalarni joylashtiring.
      Bu funksiyalar bogʻliqliklarga servis maʼlumotlariga kirish imkonini beradi.

      <docs-code header="src/app/housing.service.ts dagi servis funksiyalari" path="adev/src/content/tutorials/first-app/steps/10-routing/src/app/housing.service.ts" visibleLines="[110,116]"/>

      Bu funksiyalar sizga kelgusi darsda kerak boʻladi. Hozircha bu funksiyalar id boʻyicha muayyan `HousingLocation`'ni yoki butun roʻyxatni qaytarishini tushunish kifoya.

   1. `HousingLocation` uchun fayl darajasidagi import qoʻshing.

      <docs-code header="src/app/housing.service.ts fayliga HousingLocation turini import qilish" path="adev/src/content/tutorials/first-app/steps/10-routing/src/app/housing.service.ts" visibleLines="[2]"/>

1. Ilova xatosiz build boʻlishini tasdiqlang.
   Keyingi qadamga oʻtishdan oldin barcha xatolarni tuzating.
   </docs-step>

<docs-step title="Yangi servisni `Home`'ga inyeksiya qiling {#inject-the-new-service-into-home}">
Bu qadam yangi servisni ilovangizning `Home`'iga inyeksiya qiladi, shunda u ilova maʼlumotlarini servisdan oʻqiy oladi.
Keyingi darslardan birida statik maʼlumotlarni haqiqiy ilovadagidek maʼlumot olish uchun jonli maʼlumot manbai bilan almashtirasiz.

IDE'ingizning **Edit** panelida, `src/app/home/home.ts` faylida:

1.  `src/app/home/home.ts` faylining yuqori qismida `@angular/core`'dan import qilinadigan elementlarga `inject`'ni qoʻshing. Bu `inject` funksiyasini `Home` klassiga import qiladi.

      <docs-code language="angular-ts" header="src/app/home/home.ts faylini yangilash" path="adev/src/content/tutorials/first-app/steps/10-routing/src/app/home/home.ts" visibleLines="[1]"/>

1.  `HousingService` uchun yangi fayl darajasidagi import qoʻshing:

      <docs-code language="angular-ts" header="src/app/home/home.ts fayliga import qoʻshish" path="adev/src/content/tutorials/first-app/steps/10-routing/src/app/home/home.ts" visibleLines="[4]"/>

1.  `Home`'dan `baseUrl` oʻzgaruvchisini oʻchiring, `housingLocationList` massivi yozuvlarini oʻchiring va `housingLocationList`'ga boʻsh massiv (`[]`) qiymatini bering. Bir necha qadamdan keyin kodni maʼlumotlarni `HousingService`'dan oladigan qilib yangilaysiz.

1.  `Home`'da yangi servisni inyeksiya qilish va ilova maʼlumotlarini initsializatsiya qilish uchun quyidagi kodni qoʻshing. `constructor` — bu komponent yaratilganda ishga tushadigan birinchi funksiya. `constructor`'dagi kod `housingLocationList`'ga `getAllHousingLocations` chaqiruvidan qaytgan qiymatni beradi.

      <docs-code language="angular-ts" header="src/app/home/home.ts da maʼlumotlarni servisdan initsializatsiya qilish" path="adev/src/content/tutorials/first-app/steps/10-routing/src/app/home/home.ts" visibleLines="[23,30]"/>

1.  `src/app/home/home.ts` fayliga kiritilgan oʻzgarishlarni saqlang va ilovangiz xatosiz build boʻlishini tasdiqlang.
    Keyingi qadamga oʻtishdan oldin barcha xatolarni tuzating.
    </docs-step>

</docs-workflow>

SUMMARY: Bu darsda siz ilovangizga Angular servisini qoʻshdingiz va uni `Home` klassiga inyeksiya qildingiz.
Bu ilovangizning maʼlumotlarni qanday olishini alohida boʻlimga ajratadi.
Hozircha yangi servis maʼlumotlarini statik maʼlumotlar massividan oladi.
Keyingi darslardan birida servisni maʼlumotlarini API endpoint'idan oladigan qilib refaktoring qilasiz.

Bu darsda yoritilgan mavzular haqida koʻproq maʼlumot olish uchun quyidagilarga qarang:

<docs-pill-row>
  <docs-pill href="guide/di/creating-and-using-services" title="Inyeksiya qilinadigan servis yaratish"/>
  <docs-pill href="guide/di" title="Angular'da bogʻliqliklarni inyeksiya qilish"/>
  <docs-pill href="cli/generate/service" title="ng generate service"/>
  <docs-pill href="cli/generate" title="ng generate"/>
</docs-pill-row>
