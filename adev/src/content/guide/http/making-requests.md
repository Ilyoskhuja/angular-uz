# HTTP soʻrovlarini yuborish

`HttpClient` maʼlumotlarni yuklash hamda serverda oʻzgartirishlar (mutation) kiritish uchun soʻrov yuborishda ishlatiladigan turli HTTP fe'llariga (verbs) mos metodlarga ega. Har bir metod [RxJS `Observable`](https://rxjs.dev/guide/observable) qaytaradi, u obuna boʻlinganda soʻrovni yuboradi va server javob berganda natijalarni emit qiladi.

NOTE: `HttpClient` tomonidan yaratilgan `Observable`'larga istalgancha marta obuna boʻlish mumkin va har bir obuna uchun yangi backend soʻrovi yuboriladi.

Soʻrov metodiga uzatiladigan options obyekti orqali soʻrovning turli xususiyatlarini va qaytariladigan javob turini sozlash mumkin.

## JSON maʼlumotlarini olish {#fetching-json-data}

Backend'dan maʼlumot olish koʻpincha [`HttpClient.get()`](api/common/http/HttpClient#get) metodi yordamida GET soʻrovini yuborishni talab qiladi. Bu metod ikkita argument qabul qiladi: maʼlumot olinadigan endpoint URL satri va soʻrovni sozlash uchun _ixtiyoriy options_ obyekti.

Masalan, `HttpClient.get()` metodi yordamida faraziy API'dan konfiguratsiya maʼlumotlarini olish:

```ts
http.get<Config>('/api/config').subscribe((config) => {
  // process the configuration.
});
```

Server qaytaradigan maʼlumotlar `Config` turida boʻlishini koʻrsatuvchi generik tur argumentiga eʼtibor bering. Bu argument ixtiyoriy va agar uni tushirib qoldirsangiz, qaytarilgan maʼlumot `Object` turiga ega boʻladi.

TIP: Tuzilmasi noaniq va `undefined` yoki `null` qiymatlar boʻlishi mumkin boʻlgan maʼlumotlar bilan ishlashda javob turi sifatida `Object` oʻrniga `unknown` turidan foydalanishni koʻrib chiqing.

CRITICAL: Soʻrov metodlarining generik turi server qaytaradigan maʼlumotlar haqidagi tur **tasdigʻi** (assertion) hisoblanadi. `HttpClient` haqiqiy qaytarilgan maʼlumotning bu turga mos kelishini tekshirmaydi.

## Boshqa turdagi maʼlumotlarni olish {#fetching-other-types-of-data}

Sukut boʻyicha `HttpClient` serverlar JSON maʼlumot qaytaradi deb hisoblaydi. JSON boʻlmagan API bilan ishlashda soʻrov yuborayotganda `HttpClient`'ga qanday javob turini kutish kerakligini aytishingiz mumkin. Bu `responseType` varianti orqali amalga oshiriladi.

| **`responseType` qiymati** | **Qaytariladigan javob turi**                                                                                                             |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `'json'` (sukut boʻyicha) | Berilgan generik turdagi JSON maʼlumot                                                                                                   |
| `'text'`                 | satr (string) maʼlumot                                                                                                                    |
| `'arraybuffer'`          | Javobning xom baytlarini oʻz ichiga olgan [`ArrayBuffer`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer) |
| `'blob'`                 | [`Blob`](https://developer.mozilla.org/docs/Web/API/Blob) nusxasi                                                                         |

Masalan, `HttpClient`'dan `.jpeg` tasvirining xom baytlarini `ArrayBuffer`'ga yuklab olishni soʻrashingiz mumkin:

```ts
http.get('/images/dog.jpg', {responseType: 'arraybuffer'}).subscribe((buffer) => {
  console.log('The image is ' + buffer.byteLength + ' bytes large');
});
```

<docs-callout important title="`responseType` uchun literal qiymat">
`responseType` qiymati `HttpClient` qaytaradigan turga taʼsir qilgani uchun u `string` turida emas, literal turda boʻlishi shart.

Soʻrov metodiga uzatiladigan options obyekti literal obyekt boʻlsa, bu avtomatik sodir boʻladi, lekin soʻrov variantlarini oʻzgaruvchi yoki yordamchi metodga ajratib olayotgan boʻlsangiz, uni `responseType: 'text' as const` kabi aniq literal sifatida koʻrsatishingiz kerak boʻlishi mumkin.
</docs-callout>

## Server holatini oʻzgartirish {#mutating-server-state}

Oʻzgartirishlar kiritadigan server API'lari koʻpincha yangi holatni yoki kiritiladigan oʻzgarishni koʻrsatuvchi soʻrov tanasi (body) bilan POST soʻrovlarini yuborishni talab qiladi.

[`HttpClient.post()`](api/common/http/HttpClient#post) metodi `get()` kabi ishlaydi va options'dan oldin qoʻshimcha `body` argumentini qabul qiladi:

```ts
http.post<Config>('/api/config', newConfig).subscribe((config) => {
  console.log('Updated config:', config);
});
```

Soʻrovning `body` qismi sifatida koʻp turdagi qiymatlarni berish mumkin va `HttpClient` ularni tegishli tarzda seriyalashtiradi:

| **`body` turi**                                                                                                               | **Qanday seriyalashtiriladi**                        |
| ----------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| string                                                                                                                        | Oddiy matn                                           |
| number, boolean, massiv yoki oddiy obyekt                                                                                     | JSON                                                 |
| [`ArrayBuffer`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer)                       | buferdagi xom maʼlumot                               |
| [`Blob`](https://developer.mozilla.org/docs/Web/API/Blob)                                                                     | `Blob`'ning kontent turi bilan xom maʼlumot          |
| [`FormData`](https://developer.mozilla.org/docs/Web/API/FormData)                                                             | `multipart/form-data` koʻrinishida kodlangan maʼlumot |
| [`HttpParams`](api/common/http/HttpParams) yoki [`URLSearchParams`](https://developer.mozilla.org/docs/Web/API/URLSearchParams) | `application/x-www-form-urlencoded` formatidagi satr |

IMPORTANT: Soʻrov haqiqatda yuborilishi uchun oʻzgartirish soʻrovlarining `Observable`'lariga `.subscribe()` qilishni unutmang.

## URL parametrlarini oʻrnatish {#setting-url-parameters}

Soʻrov URL'iga kiritilishi kerak boʻlgan soʻrov parametrlarini `params` varianti yordamida koʻrsating.

URL parametrlarini sozlashning eng oddiy yoʻli — obyekt literalini uzatish:

```ts
http
  .get('/api/config', {
    params: {filter: 'all'},
  })
  .subscribe((config) => {
    // ...
  });
```

Yoki parametrlarni tuzish yoki seriyalashtirish ustidan koʻproq nazorat kerak boʻlsa, `HttpParams` nusxasini uzating.

IMPORTANT: `HttpParams` nusxalari _oʻzgarmas_ (immutable) va ularni bevosita oʻzgartirib boʻlmaydi. Oʻrniga `append()` kabi oʻzgartirish metodlari oʻzgarish qoʻllangan yangi `HttpParams` nusxasini qaytaradi.

```ts
const baseParams = new HttpParams().set('filter', 'all');

http
  .get('/api/config', {
    params: baseParams.set('details', 'enabled'),
  })
  .subscribe((config) => {
    // ...
  });
```

`HttpClient` parametrlarni URL'ga qanday kodlashini belgilaydigan maxsus `HttpParameterCodec` bilan `HttpParams` nusxasini yaratishingiz mumkin.

### Parametrlarni maxsus kodlash {#custom-parameter-encoding}

Sukut boʻyicha `HttpParams` parametr kalitlari va qiymatlarini kodlash va dekodlash uchun oʻrnatilgan [`HttpUrlEncodingCodec`](api/common/http/HttpUrlEncodingCodec)'dan foydalanadi.

Kodlash va dekodlash qanday qoʻllanishini sozlash uchun [`HttpParameterCodec`](api/common/http/HttpParameterCodec)'ning oʻz implementatsiyangizni taqdim etishingiz mumkin.

```ts
import {HttpClient, HttpParams, HttpParameterCodec} from '@angular/common/http';
import {inject} from '@angular/core';

export class CustomHttpParamEncoder implements HttpParameterCodec {
  encodeKey(key: string): string {
    return encodeURIComponent(key);
  }

  encodeValue(value: string): string {
    return encodeURIComponent(value);
  }

  decodeKey(key: string): string {
    return decodeURIComponent(key);
  }

  decodeValue(value: string): string {
    return decodeURIComponent(value);
  }
}

export class ApiService {
  private http = inject(HttpClient);

  search() {
    const params = new HttpParams({
      encoder: new CustomHttpParamEncoder(),
    })
      .set('email', 'dev+alerts@example.com')
      .set('q', 'a & b? c/d = e');

    return this.http.get('/api/items', {params});
  }
}
```

## Soʻrov sarlavhalarini oʻrnatish {#setting-request-headers}

Soʻrovga kiritilishi kerak boʻlgan soʻrov sarlavhalarini `headers` varianti yordamida koʻrsating.

Soʻrov sarlavhalarini sozlashning eng oddiy yoʻli — obyekt literalini uzatish:

```ts
http
  .get('/api/config', {
    headers: {
      'X-Debug-Level': 'verbose',
    },
  })
  .subscribe((config) => {
    // ...
  });
```

Yoki sarlavhalarni tuzish ustidan koʻproq nazorat kerak boʻlsa, `HttpHeaders` nusxasini uzating.

IMPORTANT: `HttpHeaders` nusxalari _oʻzgarmas_ (immutable) va ularni bevosita oʻzgartirib boʻlmaydi. Oʻrniga `append()` kabi oʻzgartirish metodlari oʻzgarish qoʻllangan yangi `HttpHeaders` nusxasini qaytaradi.

```ts
const baseHeaders = new HttpHeaders().set('X-Debug-Level', 'minimal');

http
  .get<Config>('/api/config', {
    headers: baseHeaders.set('X-Debug-Level', 'verbose'),
  })
  .subscribe((config) => {
    // ...
  });
```

## Server javobi hodisalari bilan ishlash {#interacting-with-the-server-response-events}

Qulaylik uchun `HttpClient` sukut boʻyicha server qaytargan maʼlumotning (javob tanasining) `Observable`'ini qaytaradi. Baʼzan haqiqiy javobni koʻrib chiqish, masalan, muayyan javob sarlavhalarini olish zarur boʻladi.

Javobning toʻliq oʻziga murojaat qilish uchun `observe` variantini `'response'` qiymatiga oʻrnating:

```ts
http.get<Config>('/api/config', {observe: 'response'}).subscribe((res) => {
  console.log('Response status:', res.status);
  console.log('Body:', res.body);
});
```

<docs-callout important title="`observe` uchun literal qiymat">
`observe` qiymati `HttpClient` qaytaradigan turga taʼsir qilgani uchun u `string` turida emas, literal turda boʻlishi shart.

Soʻrov metodiga uzatiladigan options obyekti literal obyekt boʻlsa, bu avtomatik sodir boʻladi, lekin soʻrov variantlarini oʻzgaruvchi yoki yordamchi metodga ajratib olayotgan boʻlsangiz, uni `observe: 'response' as const` kabi aniq literal sifatida koʻrsatishingiz kerak boʻlishi mumkin.
</docs-callout>

## Xom progress hodisalarini qabul qilish {#receiving-raw-progress-events}

Javob tanasi yoki javob obyektidan tashqari, `HttpClient` soʻrov hayot siklining muayyan lahzalariga mos keluvchi xom _hodisalar_ oqimini ham qaytarishi mumkin. Bu hodisalar soʻrov yuborilgan, javob sarlavhasi qaytarilgan va tana toʻliq qabul qilingan vaqtlarni oʻz ichiga oladi. Bu hodisalar shuningdek katta hajmli soʻrov yoki javob tanalari uchun yuklash va yuklab olish holatini bildiruvchi _progress hodisalarini_ ham oʻz ichiga olishi mumkin.

Progress hodisalari sukut boʻyicha oʻchirilgan (chunki ular unumdorlikka taʼsir qiladi), lekin ularni `reportUploadProgress` va `reportDownloadProgress` variantlari bilan yoqish mumkin.

NOTE: `HttpClient`'ning standart fetch backend'i _yuklash_ (upload) progress hodisalarini qoʻllab-quvvatlamaydi va `reportUploadProgress`'ni oʻrnatsangiz xato tashlaydi. Agar ilovangizga yuklash progress hodisalari kerak boʻlsa, `provideHttpClient(...)` ichida `HttpClient`'ni `withXhr()` bilan sozlang.

Hodisalar oqimini kuzatish uchun `observe` variantini `'events'` qiymatiga oʻrnating:

```ts
http
  .get('/api/download', {
    reportDownloadProgress: true,
    observe: 'events',
  })
  .subscribe((event) => {
    switch (event.type) {
      case HttpEventType.DownloadProgress:
        console.log('Downloaded ' + event.loaded + ' out of ' + event.total + ' bytes');
        break;
      case HttpEventType.Response:
        console.log('Finished downloading!');
        break;
    }
  });
```

<docs-callout important title="`observe` uchun literal qiymat">
`observe` qiymati `HttpClient` qaytaradigan turga taʼsir qilgani uchun u `string` turida emas, literal turda boʻlishi shart.

Soʻrov metodiga uzatiladigan options obyekti literal obyekt boʻlsa, bu avtomatik sodir boʻladi, lekin soʻrov variantlarini oʻzgaruvchi yoki yordamchi metodga ajratib olayotgan boʻlsangiz, uni `observe: 'events' as const` kabi aniq literal sifatida koʻrsatishingiz kerak boʻlishi mumkin.
</docs-callout>

Hodisalar oqimida qaytarilgan har bir `HttpEvent` hodisa nimani ifodalashini ajratib beruvchi `type` xususiyatiga ega:

| **`type` qiymati**               | **Hodisa maʼnosi**                                                                 |
| -------------------------------- | ---------------------------------------------------------------------------------- |
| `HttpEventType.Sent`             | Soʻrov serverga joʻnatildi                                                         |
| `HttpEventType.UploadProgress`   | Soʻrov tanasini yuklash jarayonini bildiruvchi `HttpUploadProgressEvent`           |
| `HttpEventType.ResponseHeader`   | Javobning bosh qismi, jumladan status va sarlavhalar qabul qilindi                 |
| `HttpEventType.DownloadProgress` | Javob tanasini yuklab olish jarayonini bildiruvchi `HttpDownloadProgressEvent`     |
| `HttpEventType.Response`         | Javob toʻliq, jumladan javob tanasi ham qabul qilindi                              |
| `HttpEventType.User`             | HTTP interceptor'dan kelgan maxsus hodisa.                                         |

## Soʻrov muvaffaqiyatsizligini qayta ishlash {#handling-request-failure}

HTTP soʻrovi uch xil yoʻl bilan muvaffaqiyatsiz boʻlishi mumkin:

- Tarmoq yoki ulanish xatosi soʻrovning backend serveriga yetib borishiga toʻsqinlik qilishi mumkin.
- Timeout varianti oʻrnatilgan boʻlsa, soʻrov oʻz vaqtida javob bermagan boʻlishi mumkin.
- Backend soʻrovni qabul qilishi, lekin uni qayta ishlay olmasligi va xato javobi qaytarishi mumkin.

`HttpClient` yuqoridagi barcha turdagi xatolarni `HttpErrorResponse` ichida ushlaydi va uni `Observable`'ning xato kanali orqali qaytaradi. Tarmoq va timeout xatolari `0` qiymatli `status` kodiga ega. Timeout'lar uchun `error` — `TimeoutError` nomli `DOMException`; tarmoq xatolari uchun u `fetch` tashlagan xato (yoki `withXhr()` ishlatilganda [`ProgressEvent`](https://developer.mozilla.org/docs/Web/API/ProgressEvent)). Backend xatolari backend qaytargan muvaffaqiyatsiz `status` kodiga va `error` sifatida xato javobiga ega. Xatoning sababini va xatoni bartaraf etish uchun tegishli harakatni aniqlash uchun javobni koʻrib chiqing.

[RxJS kutubxonasi](https://rxjs.dev/) xatolarni qayta ishlash uchun foydali boʻlishi mumkin bir nechta operatorlarni taklif qiladi.

Xato javobini UI uchun qiymatga aylantirish uchun `catchError` operatoridan foydalanishingiz mumkin. Bu qiymat UI'ga xato sahifasini yoki qiymatini koʻrsatishni aytishi va zarur boʻlsa xato sababini saqlab qolishi mumkin.

Baʼzan tarmoq uzilishlari kabi vaqtinchalik xatolar soʻrovning kutilmaganda muvaffaqiyatsiz boʻlishiga olib kelishi mumkin va soʻrovni shunchaki qayta urinish uning muvaffaqiyatli bajarilishiga imkon beradi. RxJS muayyan shartlar ostida muvaffaqiyatsiz `Observable`'ga avtomatik qayta obuna boʻladigan bir nechta _retry_ operatorlarini taqdim etadi. Masalan, `retry()` operatori koʻrsatilgan marta avtomatik qayta obuna boʻlishga urinadi.

### Timeout'lar {#timeouts}

Soʻrov uchun timeout oʻrnatish uchun boshqa soʻrov variantlari bilan birga `timeout` variantini millisekundlardagi songa oʻrnatishingiz mumkin. Agar backend soʻrovi koʻrsatilgan vaqt ichida yakunlanmasa, soʻrov bekor qilinadi va xato emit qilinadi.

NOTE: Timeout faqat backend HTTP soʻrovining oʻziga qoʻllanadi. Bu soʻrovni qayta ishlashning butun zanjiri uchun timeout emas. Shuning uchun bu variantga interceptor'lar kiritgan har qanday kechikish taʼsir qilmaydi.

```ts
http
  .get('/api/config', {
    timeout: 3000,
  })
  .subscribe({
    next: (config) => {
      console.log('Config fetched successfully:', config);
    },
    error: (err) => {
      // If the request times out, an error will have been emitted.
    },
  });
```

## Kengaytirilgan fetch variantlari {#advanced-fetch-options}

Angular'ning `HttpClient`'i unumdorlik va foydalanuvchi tajribasini yaxshilashi mumkin boʻlgan kengaytirilgan fetch API variantlarini qoʻllab-quvvatlaydi. Bu variantlar sukut boʻyicha ishlatiladigan fetch backend'idan foydalanilganda mavjud.

### Fetch variantlari {#fetch-options}

Quyidagi variantlar fetch backend'idan foydalanilganda soʻrov xatti-harakati ustidan nozik nazoratni taʼminlaydi.

#### Keep-alive ulanishlar {#keep-alive-connections}

`keepalive` varianti soʻrovga uni boshlagan sahifadan uzoqroq yashash imkonini beradi. Bu, ayniqsa, foydalanuvchi sahifadan chiqib ketganda ham yakunlanishi kerak boʻlgan analitika yoki jurnalga yozish (logging) soʻrovlari uchun foydali.

```ts
http
  .post('/api/analytics', analyticsData, {
    keepalive: true,
  })
  .subscribe();
```

#### HTTP keshlashni boshqarish {#http-caching-control}

`cache` varianti soʻrovning brauzerning HTTP keshi bilan qanday ishlashini boshqaradi, bu takroriy soʻrovlar uchun unumdorlikni sezilarli yaxshilashi mumkin.

```ts
//  Use cached response regardless of freshness
http
  .get('/api/config', {
    cache: 'force-cache',
  })
  .subscribe((config) => {
    // ...
  });

// Always fetch from network, bypass cache
http
  .get('/api/live-data', {
    cache: 'no-cache',
  })
  .subscribe((data) => {
    // ...
  });

// Use cached response only, fail if not in cache
http
  .get('/api/static-data', {
    cache: 'only-if-cached',
  })
  .subscribe((data) => {
    // ...
  });
```

#### Core Web Vitals uchun soʻrov ustuvorligi {#request-priority-for-core-web-vitals}

`priority` varianti soʻrovning nisbiy ahamiyatini koʻrsatish imkonini beradi va brauzerlarga yaxshiroq Core Web Vitals koʻrsatkichlari uchun resurslarni yuklashni optimallashtirishga yordam beradi.

```ts
// High priority for critical resources
http
  .get('/api/user-profile', {
    priority: 'high',
  })
  .subscribe((profile) => {
    // ...
  });

// Low priority for non-critical resources
http
  .get('/api/recommendations', {
    priority: 'low',
  })
  .subscribe((recommendations) => {
    // ...
  });

// Auto priority (default) lets the browser decide
http
  .get('/api/settings', {
    priority: 'auto',
  })
  .subscribe((settings) => {
    // ...
  });
```

Mavjud `priority` qiymatlari:

- `'high'`: Yuqori ustuvorlik, erta yuklanadi (masalan, muhim foydalanuvchi maʼlumotlari, ekranning yuqori qismidagi kontent)
- `'low'`: Past ustuvorlik, resurslar boʻsh boʻlganda yuklanadi (masalan, analitika, oldindan yuklanadigan maʼlumotlar)
- `'auto'`: Brauzer ustuvorlikni soʻrov kontekstiga qarab belgilaydi (sukut boʻyicha)

TIP: Largest Contentful Paint (LCP)ga taʼsir qiluvchi soʻrovlar uchun `priority: 'high'` va dastlabki foydalanuvchi tajribasiga taʼsir qilmaydigan soʻrovlar uchun `priority: 'low'` dan foydalaning.

#### Soʻrov rejimi {#request-mode}

`mode` varianti soʻrovning cross-origin soʻrovlarni qanday qayta ishlashini boshqaradi va javob turini belgilaydi.

```ts
// Same-origin requests only
http
  .get('/api/local-data', {
    mode: 'same-origin',
  })
  .subscribe((data) => {
    // ...
  });

// CORS-enabled cross-origin requests
http
  .get('https://api.external.com/data', {
    mode: 'cors',
  })
  .subscribe((data) => {
    // ...
  });

// No-CORS mode for simple cross-origin requests
http
  .get('https://external-api.com/public-data', {
    mode: 'no-cors',
  })
  .subscribe((data) => {
    // ...
  });
```

Mavjud `mode` qiymatlari:

- `'same-origin'`: Faqat same-origin soʻrovlarga ruxsat beradi, cross-origin soʻrovlar muvaffaqiyatsiz boʻladi
- `'cors'`: CORS bilan cross-origin soʻrovlarga ruxsat beradi (sukut boʻyicha)
- `'no-cors'`: CORS'siz oddiy cross-origin soʻrovlarga ruxsat beradi, javob opaque (yopiq) boʻladi

TIP: Brauzerda hech qachon cross-origin boʻlmasligi kerak boʻlgan nozik soʻrovlar uchun `mode: 'same-origin'` dan foydalaning.

IMPORTANT: Node.js'da SSR vaqtida `HttpClient` Node.js'ning [Undici'ga asoslangan Fetch implementatsiyasidan](https://nodejs.org/api/globals.html#fetch) foydalanadi. [Undici brauzerning CORS tekshiruvlarini amalga oshirmaydi](https://undici.nodejs.org/#cors), shuning uchun `mode: 'same-origin'` server tomonidagi soʻrovlarni cheklamaydi. Foydalanuvchi taʼsir qila oladigan URL'larni ruxsat etilganlar roʻyxati (allowlist) boʻyicha tekshiring.

#### Yoʻnaltirishlarni qayta ishlash {#redirect-handling}

`redirect` varianti serverdan kelgan yoʻnaltirish (redirect) javoblarini qanday qayta ishlashni belgilaydi.

```ts
// Follow redirects automatically (default behavior)
http
  .get('/api/resource', {
    redirect: 'follow',
  })
  .subscribe((data) => {
    // ...
  });

// Prevent automatic redirects
http
  .get('/api/resource', {
    redirect: 'manual',
  })
  .subscribe((response) => {
    // Handle redirect manually
  });

// Treat redirects as errors
http
  .get('/api/resource', {
    redirect: 'error',
  })
  .subscribe({
    next: (data) => {
      // Success response
    },
    error: (err) => {
      // Redirect responses will trigger this error handler
    },
  });
```

Mavjud `redirect` qiymatlari:

- `'follow'`: Yoʻnaltirishlarga avtomatik ergashadi (sukut boʻyicha)
- `'error'`: Yoʻnaltirishlarni xato sifatida qabul qiladi
- `'manual'`: Yoʻnaltirishlarga avtomatik ergashmaydi, yoʻnaltirish javobini qaytaradi

TIP: Yoʻnaltirishlarni maxsus mantiq bilan qayta ishlash kerak boʻlganda `redirect: 'manual'` dan foydalaning.

#### Hisob maʼlumotlarini (credentials) qayta ishlash {#credentials-handling}

`credentials` varianti cookie'lar, avtorizatsiya sarlavhalari va boshqa hisob maʼlumotlarining (credentials) cross-origin soʻrovlar bilan yuborilishini boshqaradi. Bu, ayniqsa, autentifikatsiya holatlari uchun muhim.

```ts
// Include credentials for cross-origin requests
http
  .get('https://api.example.com/protected-data', {
    credentials: 'include',
  })
  .subscribe((data) => {
    // ...
  });

// Never send credentials (default for cross-origin)
http
  .get('https://api.example.com/public-data', {
    credentials: 'omit',
  })
  .subscribe((data) => {
    // ...
  });

// Send credentials only for same-origin requests
http
  .get('/api/user-data', {
    credentials: 'same-origin',
  })
  .subscribe((data) => {
    // ...
  });

// withCredentials overrides credentials setting
http
  .get('https://api.example.com/data', {
    credentials: 'omit', // This will be ignored
    withCredentials: true, // This forces credentials: 'include'
  })
  .subscribe((data) => {
    // Request will include credentials despite credentials: 'omit'
  });

// Legacy approach (still supported)
http
  .get('https://api.example.com/data', {
    withCredentials: true,
  })
  .subscribe((data) => {
    // Equivalent to credentials: 'include'
  });
```

IMPORTANT: `withCredentials` varianti `credentials` variantidan ustun turadi. Agar ikkalasi ham koʻrsatilgan boʻlsa, `withCredentials: true` aniq koʻrsatilgan `credentials` qiymatidan qatʼi nazar har doim `credentials: 'include'` natijasini beradi.

Mavjud `credentials` qiymatlari:

- `'omit'`: Hisob maʼlumotlarini hech qachon yubormaydi
- `'same-origin'`: Hisob maʼlumotlarini faqat same-origin soʻrovlar uchun yuboradi (sukut boʻyicha)
- `'include'`: Hisob maʼlumotlarini har doim, hatto cross-origin soʻrovlar uchun ham yuboradi

TIP: CORS'ni qoʻllab-quvvatlaydigan boshqa domenga autentifikatsiya cookie'lari yoki sarlavhalarini yuborish kerak boʻlganda `credentials: 'include'` dan foydalaning. Chalkashlikning oldini olish uchun `credentials` va `withCredentials` variantlarini aralashtirib ishlatishdan qoching.

IMPORTANT: Node.js'da SSR vaqtida `credentials: 'include'` kiruvchi brauzer soʻrovidagi cookie'larni avtomatik uzatmaydi. `credentials` varianti siz aniq qoʻshgan `Cookie` yoki `Authorization` sarlavhalarini olib tashlamaydi. [Undici brauzerlar taqiqlaydigan baʼzi sarlavhalarga ruxsat beradi](https://undici.nodejs.org/#forbidden-and-safelisted-header-names), shuning uchun hisob maʼlumotlari sarlavhalarini faqat ishonchli origin'larga uzating.

#### Referrer {#referrer}

`referrer` varianti soʻrov bilan qanday referrer maʼlumoti yuborilishini boshqarish imkonini beradi. Bu maxfiylik va xavfsizlik nuqtai nazaridan muhim.

```ts
// Send a specific referrer URL
http
  .get('/api/data', {
    referrer: 'https://example.com/page',
  })
  .subscribe((data) => {
    // ...
  });

// Use the current page as referrer (default behavior)
http
  .get('/api/analytics', {
    referrer: 'about:client',
  })
  .subscribe((data) => {
    // ...
  });
```

`referrer` varianti quyidagilarni qabul qiladi:

- Yaroqli URL satri: Yuboriladigan muayyan referrer URL'ini oʻrnatadi
- Boʻsh satr `''`: Referrer maʼlumotini yubormaydi
- `'about:client'`: Standart referrer'dan (joriy sahifa URL'i) foydalanadi

TIP: Yoʻnaltiruvchi sahifa URL'ini oshkor qilishni istamagan nozik soʻrovlar uchun `referrer: ''` dan foydalaning.

#### Referrer siyosati {#referrer-policy}

`referrerPolicy` varianti HTTP soʻrovi bilan birga qancha referrer maʼlumoti — soʻrov yuborayotgan sahifaning URL'i — yuborilishini boshqaradi. Bu sozlama maxfiylikka ham, analitikaga ham taʼsir qiladi va maʼlumotlar koʻrinishi bilan xavfsizlik mulohazalari oʻrtasida muvozanat oʻrnatish imkonini beradi.

```ts
// Send no referrer information regardless of the current page
http
  .get('/api/data', {
    referrerPolicy: 'no-referrer',
  })
  .subscribe();

// Send origin only (e.g. https://example.com)
http
  .get('/api/analytics', {
    referrerPolicy: 'origin',
  })
  .subscribe();
```

`referrerPolicy` varianti quyidagilarni qabul qiladi:

- `'no-referrer'` `Referer` sarlavhasini hech qachon yubormaydi.
- `'no-referrer-when-downgrade'` Same-origin va xavfsiz (HTTPS→HTTPS) soʻrovlar uchun referrer'ni yuboradi, lekin xavfsiz origin'dan kamroq xavfsiz origin'ga (HTTPS→HTTP) oʻtishda uni tushirib qoldiradi.
- `'origin'` Referrer'ning faqat origin'ini (sxema, host, port) yuboradi, yoʻl (path) va query maʼlumotlarini tushirib qoldiradi.
- `'origin-when-cross-origin'` Same-origin soʻrovlar uchun toʻliq URL'ni, cross-origin soʻrovlar uchun esa faqat origin'ni yuboradi.
- `'same-origin'` Same-origin soʻrovlar uchun toʻliq URL'ni yuboradi, cross-origin soʻrovlar uchun referrer yubormaydi.
- `'strict-origin'` Faqat origin'ni va faqat protokol xavfsizlik darajasi pasaytirilmagan boʻlsa (masalan, HTTPS→HTTPS) yuboradi. Pasaytirishda referrer'ni tushirib qoldiradi.
- `'strict-origin-when-cross-origin'` Brauzerning standart xatti-harakati. Same-origin soʻrovlar uchun toʻliq URL'ni, pasaytirilmagan cross-origin soʻrovlar uchun origin'ni yuboradi va pasaytirishda referrer'ni tushirib qoldiradi.
- `'unsafe-url'` Har doim toʻliq URL'ni (yoʻl va query bilan) yuboradi. Bu nozik maʼlumotlarni oshkor qilishi mumkin va ehtiyotkorlik bilan ishlatilishi kerak.

TIP: Maxfiylik jihatidan nozik soʻrovlar uchun `'no-referrer'`, `'origin'` yoki `'strict-origin-when-cross-origin'` kabi konservativ qiymatlarni afzal koʻring.

#### Yaxlitlik (integrity) {#integrity}

`integrity` varianti kutilayotgan kontentning kriptografik xeshini berish orqali javobning oʻzgartirilmaganligini tekshirish imkonini beradi. Bu, ayniqsa, CDN'lardan skriptlar yoki boshqa resurslarni yuklashda foydali.

```ts
// Verify response integrity with SHA-256 hash
http
  .get('/api/script.js', {
    integrity: 'sha256-ABC123...',
    responseType: 'text',
  })
  .subscribe((script) => {
    // Script content is verified against the hash
  });
```

IMPORTANT: `integrity` varianti javob kontenti bilan berilgan xesh oʻrtasida aniq moslikni talab qiladi. Agar kontent mos kelmasa, soʻrov tarmoq xatosi bilan muvaffaqiyatsiz boʻladi.

CRITICAL: SSR vaqtida Fetch implementatsiyasi [Fetch standarti](https://fetch.spec.whatwg.org/#concept-main-fetch) talab qilganidek, javobni qaytarishdan oldin `integrity`'ni tekshirish uchun javob tanasini toʻliq oʻqiydi. Angular [`maxResponseBodySize`](/guide/ssr#configuring-the-response-body-size-limit) cheklovini faqat Fetch javob qaytargandan keyin qoʻllaydi, shuning uchun bu cheklov yaxlitlikni tekshirish vaqtida buferlangan maʼlumotlarni cheklamaydi.

TIP: Tashqi manbalardan muhim resurslarni yuklashda ularning oʻzgartirilmaganligini taʼminlash uchun subresource integrity'dan foydalaning. Xeshlarni `openssl` kabi vositalar yordamida yarating.

## HTTP `Observable`'lari {#http-observables}

`HttpClient`'dagi har bir soʻrov metodi soʻralgan javob turidagi `Observable`'ni tuzadi va qaytaradi. `HttpClient`'dan foydalanishda bu `Observable`'lar qanday ishlashini tushunish muhim.

`HttpClient` RxJS'da "sovuq" (cold) deb ataladigan `Observable`'larni hosil qiladi, yaʼni `Observable`'ga obuna boʻlinmaguncha haqiqiy soʻrov yuborilmaydi. Faqat shundan keyin soʻrov haqiqatda serverga joʻnatiladi. Bir xil `Observable`'ga bir necha marta obuna boʻlish bir nechta backend soʻrovini ishga tushiradi. Har bir obuna mustaqil.

TIP: `HttpClient` `Observable`'larini haqiqiy server soʻrovlarining _chizmalari_ (blueprints) sifatida tasavvur qilishingiz mumkin.

Obuna boʻlgandan soʻng, obunani bekor qilish bajarilayotgan soʻrovni toʻxtatadi. Bu `Observable`'ga `async` pipe orqali obuna boʻlingan boʻlsa juda foydali, chunki foydalanuvchi joriy sahifadan chiqib ketsa soʻrov avtomatik bekor qilinadi. Bundan tashqari, `Observable`'ni `switchMap` kabi RxJS kombinatori bilan ishlatsangiz, bu bekor qilish eskirgan soʻrovlarni tozalaydi.

Javob qaytgach, `HttpClient`'dan olingan `Observable`'lar odatda yakunlanadi (garchi interceptor'lar bunga taʼsir qilishi mumkin boʻlsa ham).

Avtomatik yakunlanish tufayli, `HttpClient` obunalari tozalanmasa ham, odatda xotira sizib chiqishi xavfi boʻlmaydi. Biroq, har qanday asinxron operatsiya kabi, ulardan foydalanayotgan komponent yoʻq qilinganda obunalarni tozalashni qatʼiy tavsiya qilamiz, chunki aks holda obuna callback'i ishga tushib, yoʻq qilingan komponent bilan ishlashga urinishda xatolarga duch kelishi mumkin.

TIP: `Observable`'larga obuna boʻlish uchun `async` pipe yoki `toSignal` operatsiyasidan foydalanish obunalarning toʻgʻri tozalanishini taʼminlaydi.

## Eng yaxshi amaliyotlar {#best-practices}

`HttpClient`'ni komponentlardan bevosita inyeksiya qilib ishlatish mumkin boʻlsa-da, umuman olganda maʼlumotlarga murojaat mantigʻini ajratib, inkapsulyatsiya qiluvchi qayta ishlatiladigan, inyeksiya qilinadigan servislar yaratishni tavsiya qilamiz. Masalan, bu `UserService` foydalanuvchi maʼlumotlarini uning id'si boʻyicha soʻrash mantigʻini inkapsulyatsiya qiladi:

```ts
@Service()
export class UserService {
  private http = inject(HttpClient);

  getUser(id: string): Observable<User> {
    return this.http.get<User>(`/api/user/${id}`);
  }
}
```

Komponent ichida maʼlumotlar uchun UI'ni faqat yuklash tugagandan keyin render qilish uchun `@if`'ni `async` pipe bilan birlashtirishingiz mumkin:

```angular-ts
import {AsyncPipe} from '@angular/common';

@Component({
  imports: [AsyncPipe],
  template: `
    @if (user$ | async; as user) {
      <p>Name: {{ user.name }}</p>
      <p>Biography: {{ user.biography }}</p>
    }
  `,
})
export class UserProfile {
  userId = input.required<string>();
  user$!: Observable<User>;

  private userService = inject(UserService);

  constructor() {
    effect(() => {
      this.user$ = this.userService.getUser(this.userId());
    });
  }
}
```
