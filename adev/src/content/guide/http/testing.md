# Soʻrovlarni testlash

Har qanday tashqi bogʻliqlik kabi, testlaringiz masofaviy server bilan oʻzaro aloqani simulyatsiya qila olishi uchun HTTP backend'ini mock qilishingiz shart. `@angular/common/http/testing` kutubxonasi ilova yuborgan soʻrovlarni ushlab olish, ular haqida tasdiqlar (assertions) qilish va backend'ingiz xatti-harakatini taqlid qilish uchun javoblarni mock qilish vositalarini taqdim etadi.

Test kutubxonasi ilova avval kodni bajarib, soʻrovlarni yuboradigan pattern uchun ishlab chiqilgan. Soʻngra test muayyan soʻrovlar yuborilgan yoki yuborilmaganligini kutadi, oʻsha soʻrovlar boʻyicha tasdiqlar bajaradi va nihoyat, har bir kutilgan soʻrovni "flush" qilish orqali javoblarni taqdim etadi.

Nihoyat, testlar ilova kutilmagan soʻrovlar yubormaganligini tekshirishi mumkin.

## Testlash uchun sozlash {#setup-for-testing}

`HttpClient`'dan foydalanishni testlashni boshlash uchun `TestBed`'ni sozlang va testingiz sozlamalariga `provideHttpClientTesting()`'ni kiriting. `HttpClient` Angular'ning test muhiti tomonidan taqdim etiladi va `provideHttpClientTesting()` uni haqiqiy tarmoq oʻrniga test backend'idan foydalanishga sozlaydi. U shuningdek test backend'i bilan ishlash, qaysi soʻrovlar yuborilganligi haqida kutilmalar oʻrnatish va oʻsha soʻrovlarga javoblarni flush qilish uchun foydalanadigan `HttpTestingController`'ni ham taqdim etadi. `HttpTestingController` sozlangandan keyin `TestBed`'dan inyeksiya qilinishi mumkin.

```ts
TestBed.configureTestingModule({
  providers: [
    // ... other test providers
    provideHttpClientTesting(),
  ],
});

const httpTesting = TestBed.inject(HttpTestingController);
```

Endi testlaringiz soʻrov yuborganda ular odatdagi backend oʻrniga test backend'iga boradi. Bu soʻrovlar haqida tasdiqlar qilish uchun `httpTesting`'dan foydalanishingiz mumkin.

### Testlarda `HttpClient`'ni sozlash {#configuring-httpclient-in-tests}

Agar testga interceptor'lar kabi `HttpClient` imkoniyatlarini sozlash kerak boʻlsa, `provideHttpClientTesting()`'dan oldin `provideHttpClient(...)`'ni kiriting.
IMPORTANT: `provideHttpClient()`'ni `provideHttpClientTesting()`'dan **oldin** taqdim etishni yodda tuting, chunki `provideHttpClientTesting()` `provideHttpClient()`'ning qismlarini qayta yozadi. Buni teskari tartibda qilish testlaringizni buzishi mumkin.

```ts
TestBed.configureTestingModule({
  providers: [provideHttpClient(withInterceptors([authInterceptor])), provideHttpClientTesting()],
});
```

## Soʻrovlarni kutish va ularga javob berish {#expecting-and-answering-requests}

Masalan, GET soʻrovi yuborilishini kutadigan va mock javob taqdim etadigan test yozishingiz mumkin:

```ts
TestBed.configureTestingModule({
  providers: [ConfigService, provideHttpClientTesting()],
});

const httpTesting = TestBed.inject(HttpTestingController);

// Load `ConfigService` and request the current configuration.
const service = TestBed.inject(ConfigService);
const config$ = service.getConfig<Config>();

// `firstValueFrom` subscribes to the `Observable`, which makes the HTTP request,
// and creates a `Promise` of the response.
const configPromise = firstValueFrom(config$);

// At this point, the request is pending, and we can assert it was made
// via the `HttpTestingController`:
const req = httpTesting.expectOne('/api/config', 'Request to load the configuration');

// We can assert various properties of the request if desired.
expect(req.request.method).toBe('GET');

// Flushing the request causes it to complete, delivering the result.
req.flush(DEFAULT_CONFIG);

// We can then assert that the response was successfully delivered by the `ConfigService`:
expect(await configPromise).toEqual(DEFAULT_CONFIG);

// Finally, we can assert that no other requests were made.
httpTesting.verify();
```

NOTE: Agar test berilgan mezonlarga mos keladigan birdan ortiq soʻrov yuborgan boʻlsa, `expectOne` muvaffaqiyatsiz boʻladi.

`req.method` boʻyicha tasdiqlashga muqobil sifatida, soʻrov metodini ham moslashtirish uchun `expectOne`'ning kengaytirilgan shaklidan foydalanishingiz mumkin:

```ts
const req = httpTesting.expectOne(
  {
    method: 'GET',
    url: '/api/config',
  },
  'Request to load the configuration',
);
```

HELPFUL: Kutilma API'lari soʻrovlarning toʻliq URL'i, jumladan har qanday query parametrlari boʻyicha moslashtiradi.

Oxirgi qadam — hech qanday soʻrov tugallanmagan holda qolmaganligini tekshirish — yetarlicha keng tarqalgan boʻlgani uchun uni `afterEach()` qadamiga koʻchirishingiz mumkin:

```ts
afterEach(() => {
  // Verify that none of the tests make any extra HTTP requests.
  TestBed.inject(HttpTestingController).verify();
});
```

## Bir vaqtda birdan ortiq soʻrovni qayta ishlash {#handling-more-than-one-request-at-once}

Agar testingizda takroriy soʻrovlarga javob berish kerak boʻlsa, `expectOne()` oʻrniga `match()` API'sidan foydalaning. U bir xil argumentlarni qabul qiladi, lekin mos keladigan soʻrovlar massivini qaytaradi. Qaytarilgandan keyin bu soʻrovlar kelgusi moslashtirishdan chiqariladi va ularni flush qilish hamda tekshirish uchun siz javobgar boʻlasiz.

```ts
const allGetRequests = httpTesting.match({method: 'GET'});
for (const req of allGetRequests) {
  // Handle responding to each request.
}
```

## Kengaytirilgan moslashtirish {#advanced-matching}

Barcha moslashtirish funksiyalari maxsus moslashtirish mantigʻi uchun predikat funksiyasini qabul qiladi:

```ts
// Look for one request that has a request body.
const requestsWithBody = httpTesting.expectOne((req) => req.body !== null);
```

`expectNone` funksiyasi berilgan mezonlarga hech qanday soʻrov mos kelmasligini tasdiqlaydi.

```ts
// Assert that no mutation requests have been issued.
httpTesting.expectNone((req) => req.method !== 'GET');
```

## Xatolarni qayta ishlashni testlash {#testing-error-handling}

HTTP soʻrovlari muvaffaqiyatsiz boʻlganda ilovangizning javoblarini testlashingiz kerak.

### Backend xatolari {#backend-errors}

Backend xatolarini qayta ishlashni testlash uchun (server muvaffaqiyatsiz status kodini qaytarganda), soʻrovlarni backend'ingiz soʻrov muvaffaqiyatsiz boʻlganda qaytaradigan javobni taqlid qiluvchi xato javobi bilan flush qiling.

```ts
const req = httpTesting.expectOne('/api/config');
req.flush('Failed!', {status: 500, statusText: 'Internal Server Error'});

// Assert that the application successfully handled the backend error.
```

### Tarmoq xatolari {#network-errors}

Soʻrovlar tarmoq xatolari sababli ham muvaffaqiyatsiz boʻlishi mumkin, ular `ProgressEvent` xatolari sifatida namoyon boʻladi. Ularni `error()` metodi bilan yetkazish mumkin:

```ts
const req = httpTesting.expectOne('/api/config');
req.error(new ProgressEvent('network error!'));

// Assert that the application successfully handled the network error.
```

## Interceptor'ni testlash {#testing-an-interceptor}

Interceptor'laringiz kerakli sharoitlarda ishlashini testlashingiz kerak.

Masalan, ilovadan servis tomonidan yaratilgan autentifikatsiya tokenini har bir chiquvchi soʻrovga qoʻshish talab qilinishi mumkin.
Bu xatti-harakatni interceptor yordamida taʼminlash mumkin:

```ts
export function authInterceptor(
  request: HttpRequest<unknown>,
  next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> {
  const authService = inject(AuthService);

  const clonedRequest = request.clone({
    headers: request.headers.append('X-Authentication-Token', authService.getAuthToken()),
  });
  return next(clonedRequest);
}
```

Bu interceptor uchun `TestBed` konfiguratsiyasi `withInterceptors` imkoniyatiga tayanishi kerak.

```ts
TestBed.configureTestingModule({
  providers: [
    AuthService,
    // Testing one interceptor at a time is recommended.
    provideHttpClient(withInterceptors([authInterceptor])),
    provideHttpClientTesting(),
  ],
});
```

`HttpTestingController` soʻrov nusxasini olishi mumkin, soʻngra soʻrov oʻzgartirilganligini tekshirish uchun uni koʻrib chiqish mumkin.

```ts
const service = TestBed.inject(AuthService);
const http = TestBed.inject(HttpClient);

// Make an HTTP request.
const response = firstValueFrom(http.get('/api/config'));

const req = httpTesting.expectOne('/api/config');

expect(req.request.headers.get('X-Authentication-Token')).toEqual(service.getAuthToken());
```

Shunga oʻxshash interceptor'ni klassga asoslangan interceptor'lar bilan ham amalga oshirish mumkin:

```ts
@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  private authService = inject(AuthService);

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const clonedRequest = request.clone({
      headers: request.headers.append('X-Authentication-Token', this.authService.getAuthToken()),
    });
    return next.handle(clonedRequest);
  }
}
```

Uni testlash uchun `TestBed` konfiguratsiyasi oʻrniga quyidagicha boʻlishi kerak:

```ts
TestBed.configureTestingModule({
  providers: [
    AuthService,
    provideHttpClient(withInterceptorsFromDi()),
    provideHttpClientTesting(),
    // We rely on the HTTP_INTERCEPTORS token to register the AuthInterceptor as an HttpInterceptor
    {provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true},
  ],
});
```
