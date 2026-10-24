# Ilovangizga HTTP aloqasini qoʻshish

Bu darslik ilovangizga HTTP va API'ni qanday integratsiya qilishni koʻrsatadi.

Shu paytgacha ilovangiz maʼlumotlarni Angular servisidagi statik massivdan oʻqir edi. Keyingi qadam — ilovangiz HTTP orqali aloqa qiladigan JSON serverdan foydalanish. HTTP soʻrovi serverdan olingan maʼlumotlar bilan ishlash tajribasini simulyatsiya qiladi.

<docs-video src="https://www.youtube.com/embed/5K10oYJ5Y-E?si=TiuNKx_teR9baO7k"/>

IMPORTANT: Darslikning bu qadami uchun lokal muhitingizdan foydalanishni tavsiya qilamiz.

## Nimalarni oʻrganasiz {#what-youll-learn}

Ilovangiz JSON serverdagi maʼlumotlardan foydalanadi

<docs-workflow>

<docs-step title="JSON serverni sozlang {#configure-the-json-server}">
JSON Server — soxta (mock) REST API'lar yaratish uchun ishlatiladigan ochiq kodli vosita. Siz undan hozirda housing servisida saqlanayotgan turar joy maʼlumotlarini taqdim etish uchun foydalanasiz.

1. Quyidagi buyruq yordamida npm'dan `json-server`'ni oʻrnating.

   ```bash
   npm install -g json-server
   ```

1. Loyihangizning ildiz katalogida `db.json` nomli fayl yarating. Bu yerda `json-server` uchun maʼlumotlarni saqlaysiz.

1. `db.json` faylini oching va quyidagi kodni faylga nusxalang

   ```json
   {
     "locations": [
       {
         "id": 0,
         "name": "Acme Fresh Start Housing",
         "city": "Chicago",
         "state": "IL",
         "photo": "https://angular.dev/assets/images/tutorials/common/bernard-hermant-CLKGGwIBTaY-unsplash.jpg",
         "availableUnits": 4,
         "wifi": true,
         "laundry": true
       },
       {
         "id": 1,
         "name": "A113 Transitional Housing",
         "city": "Santa Monica",
         "state": "CA",
         "photo": "https://angular.dev/assets/images/tutorials/common/brandon-griggs-wR11KBaB86U-unsplash.jpg",
         "availableUnits": 0,
         "wifi": false,
         "laundry": true
       },
       {
         "id": 2,
         "name": "Warm Beds Housing Support",
         "city": "Juneau",
         "state": "AK",
         "photo": "https://angular.dev/assets/images/tutorials/common/i-do-nothing-but-love-lAyXdl1-Wmc-unsplash.jpg",
         "availableUnits": 1,
         "wifi": false,
         "laundry": false
       },
       {
         "id": 3,
         "name": "Homesteady Housing",
         "city": "Chicago",
         "state": "IL",
         "photo": "https://angular.dev/assets/images/tutorials/common/ian-macdonald-W8z6aiwfi1E-unsplash.jpg",
         "availableUnits": 1,
         "wifi": true,
         "laundry": false
       },
       {
         "id": 4,
         "name": "Happy Homes Group",
         "city": "Gary",
         "state": "IN",
         "photo": "https://angular.dev/assets/images/tutorials/common/krzysztof-hepner-978RAXoXnH4-unsplash.jpg",
         "availableUnits": 1,
         "wifi": true,
         "laundry": false
       },
       {
         "id": 5,
         "name": "Hopeful Apartment Group",
         "city": "Oakland",
         "state": "CA",
         "photo": "https://angular.dev/assets/images/tutorials/common/r-architecture-JvQ0Q5IkeMM-unsplash.jpg",
         "availableUnits": 2,
         "wifi": true,
         "laundry": true
       },
       {
         "id": 6,
         "name": "Seriously Safe Towns",
         "city": "Oakland",
         "state": "CA",
         "photo": "https://angular.dev/assets/images/tutorials/common/phil-hearing-IYfp2Ixe9nM-unsplash.jpg",
         "availableUnits": 5,
         "wifi": true,
         "laundry": true
       },
       {
         "id": 7,
         "name": "Hopeful Housing Solutions",
         "city": "Oakland",
         "state": "CA",
         "photo": "https://angular.dev/assets/images/tutorials/common/r-architecture-GGupkreKwxA-unsplash.jpg",
         "availableUnits": 2,
         "wifi": true,
         "laundry": true
       },
       {
         "id": 8,
         "name": "Seriously Safe Towns",
         "city": "Oakland",
         "state": "CA",
         "photo": "https://angular.dev/assets/images/tutorials/common/saru-robert-9rP3mxf8qWI-unsplash.jpg",
         "availableUnits": 10,
         "wifi": false,
         "laundry": false
       },
       {
         "id": 9,
         "name": "Capital Safe Towns",
         "city": "Portland",
         "state": "OR",
         "photo": "https://angular.dev/assets/images/tutorials/common/webaliser-_TPTXZd9mOo-unsplash.jpg",
         "availableUnits": 6,
         "wifi": true,
         "laundry": true
       }
     ]
   }
   ```

1. Bu faylni saqlang.

1. Konfiguratsiyangizni sinash vaqti keldi. Buyruqlar qatorida, loyihangizning ildizida quyidagi buyruqlarni bajaring.

   ```bash
   json-server --watch db.json
   ```

1. Veb-brauzeringizda `http://localhost:3000/locations` manziliga oʻting va javobda `db.json` faylida saqlangan maʼlumotlar borligini tasdiqlang.

Konfiguratsiyangiz bilan muammo boʻlsa, [rasmiy hujjatlarda](https://www.npmjs.com/package/json-server) koʻproq tafsilotlarni topishingiz mumkin.
</docs-step>

<docs-step title="Servisni lokal massiv oʻrniga veb-serverdan foydalanadigan qilib yangilang {#update-service-to-use-web-server-instead-of-local-array}">
Maʼlumot manbai sozlandi, keyingi qadam — veb-ilovangizni unga ulanib, maʼlumotlardan foydalanadigan qilib yangilash.

1.  `src/app/housing.service.ts` faylida quyidagi oʻzgarishlarni kiriting:

1.  Kodni `housingLocationList` xususiyatini va maʼlumotlarni oʻz ichiga olgan massivni, shuningdek `baseUrl` xususiyatini olib tashlaydigan qilib yangilang.

1.  `url` nomli satr xususiyatini qoʻshing va uning qiymatini `'http://localhost:3000/locations'` ga oʻrnating

    <docs-code header="housing.service.ts fayliga url xususiyatini qoʻshish" path="adev/src/content/tutorials/first-app/steps/14-http/src-final/app/housing.service.ts" visibleLines="[6]"/>

    Bu kod faylning qolgan qismida xatolarga olib keladi, chunki u `housingLocationList` xususiyatiga bogʻliq. Keyin servis metodlarini yangilaymiz.

1.  `getAllHousingLocations` funksiyasini siz sozlagan veb-serverga chaqiruv qiladigan qilib yangilang.

     <docs-code header="housing.service.ts dagi getAllHousingLocations metodini yangilash" path="adev/src/content/tutorials/first-app/steps/14-http/src-final/app/housing.service.ts" visibleLines="[8,11]"/>

    Endi kod HTTP orqali **GET** soʻrovi yuborish uchun asinxron koddan foydalanadi.

    HELPFUL: Bu misolda kod `fetch`'dan foydalanadi. Murakkabroq holatlar uchun Angular taqdim etadigan `HttpClient`'dan foydalanishni koʻrib chiqing.

1.  `getHousingLocationById` funksiyasini siz sozlagan veb-serverga chaqiruv qiladigan qilib yangilang.

    HELPFUL: `fetch` URL'i endi mos `id` xususiyat qiymatiga ega joyni soʻrash uchun `id`'ni yoʻl segmenti sifatida (`${this.url}/${id}`) qoʻshayotganiga eʼtibor bering.

     <docs-code header="housing.service.ts dagi getHousingLocationById metodini yangilash" path="adev/src/content/tutorials/first-app/steps/14-http/src-final/app/housing.service.ts" visibleLines="[13,17]"/>

1.  Barcha yangilanishlar tugagach, yangilangan servisingiz quyidagi kodga mos boʻlishi kerak.

     <docs-code header="housing.service.ts faylining yakuniy versiyasi" path="adev/src/content/tutorials/first-app/steps/14-http/src-final/app/housing.service.ts" visibleLines="[1,23]" />

</docs-step>

<docs-step title="Komponentlarni housing servisiga asinxron chaqiruvlardan foydalanadigan qilib yangilang {#update-the-components-to-use-asynchronous-calls-to-the-housing-service}">
Server endi maʼlumotlarni HTTP soʻrovidan oʻqiyapti, lekin servisga tayanadigan komponentlarda endi xatolar bor, chunki ular servisning sinxron versiyasidan foydalanish uchun yozilgan edi.

1.  `src/app/home/home.ts` faylida `constructor`'ni `getAllHousingLocations` metodining yangi asinxron versiyasidan foydalanadigan qilib yangilang. Holatimiz uchun signallardan foydalanmaganimiz sababli, Angular'ga sinxronlashni talab qiluvchi oʻzgarish yuz berganini bildirishingiz kerak. Buning uchun `this.changeDetectorRef.markForCheck()`'ni chaqiring.

      <docs-code header="home.ts dagi constructor'ni yangilash" path="adev/src/content/tutorials/first-app/steps/14-http/src-final/app/home/home.ts" visibleLines="[30,38]"/>

1.  `src/app/details/details.ts` faylida `constructor`'ni `getHousingLocationById` metodining yangi asinxron versiyasidan foydalanadigan qilib yangilang. Avvalgidek, Angular'ga oʻzgarishlar haqida bildirish uchun `this.changeDetectorRef.markForCheck()`'ni ham chaqirishingiz kerak.

      <docs-code header="details.ts dagi constructor'ni yangilash" path="adev/src/content/tutorials/first-app/steps/14-http/src-final/app/details/details.ts" visibleLines="[60,66]"/>

1.  Kodingizni saqlang.

1.  Ilovani brauzerda oching va u hech qanday xatosiz ishlashini tasdiqlang.
    </docs-step>

</docs-workflow>

NOTE: Bu dars `fetch` brauzer API'siga tayanadi. Interceptor'lar qoʻllab-quvvatlanishi uchun [HTTP klient hujjatlariga](/guide/http) murojaat qiling

SUMMARY: Bu darsda siz ilovangizni lokal veb-serverdan (`json-server`) va maʼlumotlarni olish uchun asinxron servis metodlaridan foydalanadigan qilib yangiladingiz.

Tabriklaymiz! Siz bu darslikni muvaffaqiyatli yakunladingiz va yanada murakkab Angular ilovalarini yaratish boʻyicha sayohatingizni davom ettirishga tayyorsiz.

Koʻproq oʻrganmoqchi boʻlsangiz, Angular'ning boshqa dasturchi [darsliklari](tutorials) va [qoʻllanmalarini](overview) ham oʻtishni koʻrib chiqing.
