# `httpResource` bilan reaktiv maʼlumot olish

`httpResource` — bu `HttpClient` atrofidagi reaktiv oʻram boʻlib, sizga soʻrov holati va javobni signallar koʻrinishida beradi. Shunday qilib, bu signallarni `computed`, `effect`, `linkedSignal` yoki boshqa har qanday reaktiv API bilan ishlatishingiz mumkin. `HttpClient` asosida qurilgani uchun `httpResource` interceptor'lar kabi barcha bir xil imkoniyatlarni qoʻllab-quvvatlaydi.

Angular'ning `resource` patterni haqida koʻproq bilish uchun [`resource` bilan asinxron reaktivlik](/guide/signals/resource) boʻlimiga qarang.

## `httpResource`'dan foydalanish {#using-httpresource}

TIP: `httpResource` global mavjud `HttpClient`'dan foydalanadi. `provideHttpClient(...)`'ni faqat interceptor'lar yoki XSRF variantlari kabi HTTP imkoniyatlarini sozlash kerak boʻlganda ishlating. Batafsil maʼlumot uchun [HttpClient'ni sozlash](/guide/http/setup) boʻlimiga qarang.

HTTP resursini url qaytarish orqali aniqlashingiz mumkin:

```ts
userId = input.required<string>();

user = httpResource(() => `/api/user/${userId()}`); // A reactive function as argument
```

`httpResource` reaktiv, yaʼni u bogʻliq boʻlgan signallardan biri (masalan, `userId`) oʻzgarganda resurs yangi http soʻrovini yuboradi.
Agar soʻrov allaqachon kutilayotgan boʻlsa, resurs yangisini yuborishdan oldin tugallanmagan soʻrovni bekor qiladi.

HELPFUL: `httpResource` `HttpClient`'dan farq qiladi, chunki u soʻrovni _darhol_ (eagerly) boshlaydi. Aksincha, `HttpClient` soʻrovlarni faqat qaytarilgan `Observable`'ga obuna boʻlingandan keyin boshlaydi.

Murakkabroq soʻrovlar uchun `HttpClient` qabul qiladigan soʻrovga oʻxshash soʻrov obyektini aniqlashingiz mumkin.
Soʻrov obyektining reaktiv boʻlishi kerak boʻlgan har bir xususiyati signal orqali tuzilishi kerak.

```ts
user = httpResource(() => ({
  url: `/api/user/${userId()}`,
  method: 'GET',
  headers: {
    'X-Special': 'true',
  },
  params: {
    'fast': 'yes',
  },
  reportProgress: true,
  transferCache: true,
  keepalive: true,
  mode: 'cors',
  redirect: 'error',
  priority: 'high',
  cache: 'force-cache',
  credentials: 'include',
  referrer: 'no-referrer',
  integrity: 'sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GhEXAMPLEKEY=',
  referrerPolicy: 'no-referrer',
}));
```

TIP: `httpResource`'ni `POST` yoki `PUT` kabi _oʻzgartirishlar_ (mutations) uchun ishlatishdan qoching. Oʻrniga asosidagi `HttpClient` API'laridan bevosita foydalanishni afzal koʻring.

`httpResource` signallarini shablonda qaysi elementlar koʻrsatilishini boshqarish uchun ishlatish mumkin.

```angular-html
@if (user.hasValue()) {
  <user-details [user]="user.value()" />
} @else if (user.error()) {
  <div>Could not load user information</div>
} @else if (user.isLoading()) {
  <div>Loading user info...</div>
}
```

HELPFUL: Xato holatidagi `resource`'ning `value` signalini oʻqish ish vaqtida xato tashlaydi. `value`'ni oʻqishni `hasValue()` bilan himoyalash tavsiya etiladi.

### Javob turlari {#response-types}

Sukut boʻyicha `httpResource` javobni JSON sifatida qaytaradi va tahlil qiladi. Biroq, `httpResource`'dagi qoʻshimcha funksiyalar yordamida boshqa qaytarish turini koʻrsatishingiz mumkin:

```ts
httpResource.text(() => ({ … })); // returns a string in value()

httpResource.blob(() => ({ … })); // returns a Blob object in value()

httpResource.arrayBuffer(() => ({ … })); // returns an ArrayBuffer in value()
```

### Yuklab olish jarayonini kuzatish {#tracking-download-progress}

Javobni yuklab olish jarayonini kuzatish uchun soʻrov obyektida `reportProgress: true` oʻrnating. Eng soʻnggi `HttpProgressEvent` resursning `progress` signali orqali mavjud:

```ts
file = httpResource.blob(() => ({
  url: `/api/files/${fileId()}`,
  reportProgress: true,
}));

downloaded = computed(() => this.file.progress()?.loaded ?? 0);
```

NOTE: `reportProgress` `reportUploadProgress` va `reportDownloadProgress` foydasiga eskirgan `HttpClient`'dan farqli oʻlaroq, `httpResource` yagona `reportProgress` variantini saqlab qoladi. U faqat yuklab olish progress hodisalarini yoqadi.

## Javobni tahlil qilish va validatsiya {#response-parsing-and-validation}

Maʼlumotlarni olishda javoblarni oldindan belgilangan sxema boʻyicha, koʻpincha [Zod](https://zod.dev) yoki [Valibot](https://valibot.dev) kabi mashhur ochiq kodli kutubxonalar yordamida tekshirishni istashingiz mumkin. Bunday validatsiya kutubxonalarini `parse` variantini koʻrsatish orqali `httpResource` bilan integratsiya qilishingiz mumkin. `parse` funksiyasining qaytarish turi resursning `value` turini belgilaydi.

Quyidagi misol [StarWars API](https://swapi.info/)'dan kelgan javobni tahlil qilish va tekshirish uchun Zod'dan foydalanadi. Soʻngra resurs Zod tahlilining chiqish turi bilan bir xil tiplanadi.

```ts
const starWarsPersonSchema = z.object({
  name: z.string(),
  height: z.number({coerce: true}),
  edited: z.string().datetime(),
  films: z.array(z.string()),
});

export class CharacterViewer {
  id = signal(1);

  swPersonResource = httpResource(() => `https://swapi.info/api/people/${this.id()}`, {
    parse: starWarsPersonSchema.parse,
  });
}
```

## httpResource'ni testlash {#testing-an-httpresource}

`httpResource` `HttpClient` atrofidagi oʻram boʻlgani uchun `httpResource`'ni `HttpClient` bilan bir xil API'lar yordamida testlashingiz mumkin. Batafsil maʼlumot uchun [HttpClient'ni testlash](/guide/http/testing) boʻlimiga qarang.

Quyidagi misolda `httpResource`'dan foydalanadigan kod uchun unit test koʻrsatilgan.

```ts
TestBed.configureTestingModule({
  providers: [provideHttpClientTesting()],
});

const id = signal(0);
const mockBackend = TestBed.inject(HttpTestingController);
const response = httpResource(() => `/data/${id()}`, {injector: TestBed.inject(Injector)});
TestBed.tick(); // Triggers the effect
const firstRequest = mockBackend.expectOne('/data/0');
firstRequest.flush(0);

// Ensures the values are propagated to the httpResource
await TestBed.inject(ApplicationRef).whenStable();

expect(response.value()).toEqual(0);
```
